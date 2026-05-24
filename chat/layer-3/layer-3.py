import json
import random
import time
import psycopg2
import redis
from kafka import KafkaConsumer

# Configurazione parametri PostgreSQL
db_params = {
    "host": "postgres-service",
    "database": "pipeline_db",
    "user": "pietro_user",
    "password": "super_password_123",
    "port": "5432"
}

def connetti_db():
    while True:
        try:
            conn = psycopg2.connect(**db_params)
            print("Connessione a PostgreSQL riuscita!", flush=True)
            return conn
        except Exception as e:
            print(f"PostgreSQL non ancora pronto, riprovo... ({e})", flush=True)
            time.sleep(2)

conn = connetti_db()
cursor = conn.cursor()

# Creazione tabella SQL
cursor.execute("""
    CREATE TABLE IF NOT EXISTS transazioni (
        id SERIAL PRIMARY KEY,
        transaction_id INT NOT NULL,
        valore INT NOT NULL,
        stato_layer2 VARCHAR(50),
        layer_intermedio INT,
        stato_layer3 VARCHAR(50),
        layer_finale INT
    );
""")
conn.commit()

# Connessione alla cache Redis locale
try:
    r = redis.Redis(host='redis-service', port=6379, db=0, decode_responses=True)
    print("Connessione a Redis riuscita!", flush=True)
except Exception as e:
    print(f"Errore connessione Redis: {e}", flush=True)

consumer = KafkaConsumer(
    'topic-layer-2', 
    bootstrap_servers=['my-kafka:9092'],
    group_id='group-layer-3',
    auto_offset_reset='earliest',
    metadata_max_age_ms=1000,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

stati_possibili = ["fraud", "valid", "unknown"]
print("Layer 3 (Consumer + Cache Redis + SQL Writer) avviato...", flush=True)

for message in consumer:
    try:
        dati = message.value
        t_id = dati["transaction_id"]
        
        # --- LOGICA DI CACHING ---
        # Controlliamo se la transazione è già presente nella cache locale di Redis
        cache_hit = r.get(f"tx:{t_id}")
        
        if cache_hit:
            print(f"Layer 3 - [CACHE HIT] La transazione {t_id} è già passata di qui recentemente!", flush=True)
            continue # Salta il salvataggio su Postgres se è un duplicato presente in cache
            
        # Cache Miss: elaboriamo il dato e lo salviamo sia in cache che nel DB
        dati["stato_layer3"] = random.choice(stati_possibili)
        dati["layer_finale"] = 3
        
        # Scrittura su Redis con un TTL (scadenza) di 60 secondi
        r.set(f"tx:{t_id}", json.dumps(dati), ex=60)
        print(f"Layer 3 - [CACHE MISS] Salvata chiave 'tx:{t_id}' su Redis (TTL 60s)", flush=True)
        
        # Scrittura su PostgreSQL
        query = """
            INSERT INTO transazioni (transaction_id, valore, stato_layer2, layer_intermedio, stato_layer3, layer_finale)
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        valores = (t_id, dati["valore"], dati["stato_layer2"], dati["layer_intermedio"], dati["stato_layer3"], dati["layer_finale"])
        
        cursor.execute(query, valores)
        conn.commit()
        print(f"Layer 3 - Salvato in SQL (Postgres): {dati}", flush=True)
        
    except Exception as e:
        print(f"ERRORE LAYER 3: {e}", flush=True)
        conn.rollback()