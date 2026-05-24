import json
import random
from kafka import KafkaConsumer, KafkaProducer

consumer = KafkaConsumer(
    'topic-layer-1', 
    bootstrap_servers=['my-kafka:9092'],
    group_id='group-layer-2',
    auto_offset_reset='earliest',
    metadata_max_age_ms=1000,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers=['my-kafka:9092']
)

stati_possibili = ["fraud", "valid", "unknown"]
print("Layer 2 (Consumer + Producer) avviato...", flush=True)

for message in consumer:
    try:
        dati = message.value
        # Applica la logica del vecchio consumer
        dati["stato_layer2"] = random.choice(stati_possibili)
        dati["layer_intermedio"] = 2
        print(f"Layer 2 elaborato da topic-layer-1: {dati}", flush=True)
        
        # Rilancia il messaggio arricchito nel secondo topic
        payload_bytes = json.dumps(dati).encode('utf-8')
        producer.send('topic-layer-2', value=payload_bytes)
    except Exception as e:
        print(f"ERRORE LAYER 2: {e}", flush=True)