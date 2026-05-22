from kafka import KafkaConsumer
consumer = KafkaConsumer('test-topic', bootstrap_servers=['my-kafka:9092'])
for message in consumer:
    print(f"Ricevuto: {message.value.decode('utf-8')}")