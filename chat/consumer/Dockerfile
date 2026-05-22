FROM python:3.9-slim
RUN pip install kafka-python
COPY consumer.py /app/consumer.py
CMD ["python3", "-u", "/app/consumer.py"]