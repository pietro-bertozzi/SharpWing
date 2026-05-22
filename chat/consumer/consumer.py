from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'test-topic', 
    bootstrap_servers=['my-kafka:9092'],
    group_id='my-group',
    auto_offset_reset='earliest'
)

for message in consumer:
    print(f"Ricevuto: {message.value.decode('utf-8')}")