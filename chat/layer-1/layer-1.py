import json
import random
import time
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['my-kafka:9092']
)

transaction_id = 1

print("Layer 1 (Producer) avviato...", flush=True)

while True:
    try:
        payload = {
            "transaction_id": transaction_id,
            "valore": random.randint(1, 100)
        }
        payload_bytes = json.dumps(payload).encode('utf-8')
        future = producer.send('topic-layer-1', value=payload_bytes)
        record_metadata = future.get(timeout=10) 
        
        print(f"Layer 1 inviato a topic-layer-1: {payload}", flush=True)
        transaction_id += 1
    except Exception as e:
        print(f"ERRORE LAYER 1: {e}", flush=True)
        
    time.sleep(5)