from kafka import KafkaProducer
import time

producer = KafkaProducer(bootstrap_servers=['my-kafka:9092'])
while True:
    producer.send('test-topic', b'Ciao dal producer!')
    print("Messaggio inviato!")
    time.sleep(5)