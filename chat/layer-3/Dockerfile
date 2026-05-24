FROM python:3.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir -U pip setuptools wheel
RUN pip install --no-cache-dir kafka-python-ng psycopg2

COPY layer-3.py .

CMD ["python3", "-u", "layer-3.py"]