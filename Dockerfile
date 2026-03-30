FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    chromium chromium-driver curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
COPY tests/ ./tests/

RUN mkdir -p data

EXPOSE 5000 8501

CMD ["sh", "-c", "python api.py & streamlit run main.py --server.port=8501 --server.address=0.0.0.0"]