FROM python:3.9-slim
RUN pip install kafka-python
COPY producer.py /app/producer.py
CMD ["python3", "-u", "/app/producer.py"]