import json
import random
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'topic-layer-2', 
    bootstrap_servers=['my-kafka:9092'],
    group_id='group-layer-3',
    auto_offset_reset='earliest',
    metadata_max_age_ms=1000,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

stati_possibili = ["fraud", "valid", "unknown"]
print("Layer 3 (Consumer finale) avviato...", flush=True)

for message in consumer:
    dati = message.value
    dati["stato_layer3"] = random.choice(stati_possibili)
    dati["layer_finale"] = 3
    print(f"Layer 3 Ricevuto definitivo da topic-layer-2: {dati}", flush=True)