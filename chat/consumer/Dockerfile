# Esempio per il Consumer (valido identico anche per il Producer cambiando i file)
FROM python:3.9-slim

# Installa i tool di sistema necessari per evitare fallimenti con pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Aggiorna pip e setuptools prima di installare la libreria di Kafka
RUN pip install --no-cache-dir -U pip setuptools wheel
RUN pip install --no-cache-dir kafka-python-ng

COPY consumer.py .

CMD ["python3", "-u", "consumer.py"]