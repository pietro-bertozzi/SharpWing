import json
import random
import time
import psycopg2
from kafka import KafkaConsumer

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
            print(f"PostgreSQL non ancora pronto, riprovo tra 2 secondi... ({e})", flush=True)
            time.sleep(2)

conn = connetti_db()
cursor = conn.cursor()

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

consumer = KafkaConsumer(
    'topic-layer-2', 
    bootstrap_servers=['my-kafka:9092'],
    group_id='group-layer-3',
    auto_offset_reset='earliest',
    metadata_max_age_ms=1000,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

stati_possibili = ["fraud", "valid", "unknown"]
print("Layer 3 (Consumer + SQL Writer) avviato...", flush=True)

for message in consumer:
    try:
        dati = message.value
        dati["stato_layer3"] = random.choice(stati_possibili)
        dati["layer_finale"] = 3
        
        query = """
            INSERT INTO transazioni (transaction_id, valore, stato_layer2, layer_intermedio, stato_layer3, layer_finale)
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        valores = (
            dati["transaction_id"],
            dati["valore"],
            dati["stato_layer2"],
            dati["layer_intermedio"],
            dati["stato_layer3"],
            dati["layer_finale"]
        )
        
        cursor.execute(query, valores)
        conn.commit()
        print(f"Layer 3 - Salvato in SQL (Postgres): {dati}", flush=True)
    except Exception as e:
        print(f"ERRORE LAYER 3 DURANTE IL SALVATAGGIO SQL: {e}", flush=True)
        conn.rollback()