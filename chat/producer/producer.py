import json
import random
import time
from kafka import KafkaProducer  # Corretto l'import

# Inizializzazione del producer che mancava
producer = KafkaProducer(
    bootstrap_servers=['my-kafka:9092']
)

transaction_id = 1  # Inizializzazione della variabile

print("Producer avviato...")
while True:
    try:
        payload = {
            "transaction_id": transaction_id,
            "valore": random.randint(1, 100)
        }
        
        payload_bytes = json.dumps(payload).encode('utf-8')
        
        future = producer.send('test-topic', value=payload_bytes)
        record_metadata = future.get(timeout=10) 
        
        print(f"Inviato con successo alla partition {record_metadata.partition} con offset {record_metadata.offset}: {payload}")
        transaction_id += 1
    except Exception as e:
        print(f"ERRORE REALE DI KAFKA: {e}")
        
    time.sleep(5)