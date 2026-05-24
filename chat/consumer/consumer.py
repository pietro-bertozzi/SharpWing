import json
import random
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'test-topic', 
    bootstrap_servers=['my-kafka:9092'],
    group_id='my-group',
    auto_offset_reset='earliest',
    metadata_max_age_ms=1000,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

stati_possibili = ["fraud", "valid", "unknown"]

print("Consumer avviato e in ascolto...")
for message in consumer:
    dati = message.value
    dati["stato"] = random.choice(stati_possibili)
    dati["layer"] = 2
    print(f"Ricevuto e arricchito: {dati}")