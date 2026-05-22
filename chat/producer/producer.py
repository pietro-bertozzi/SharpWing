from kafka import KafkaProducer
import time

producer = KafkaProducer(bootstrap_servers=['my-kafka:9092'])

while True:
    try:
        producer.send('test-topic', b'Ciao dal producer!')
        # Forza il flush per garantire l'invio immediato del buffer
        producer.flush()
        print("Messaggio inviato!")
    except Exception as e:
        print(f"Errore di invio: {e}")
    time.sleep(5)