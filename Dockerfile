FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .
COPY tests/ ./tests/

RUN mkdir -p data

EXPOSE 8501

ENV API_URL=http://localhost:5000

CMD ["sh", "-c", "python api.py & streamlit run main.py --server.port=8501 --server.address=0.0.0.0"]
```

Also add this to Railway **Variables** tab:
- `PORT` = `8501`

Then in Railway **Settings → Deploy**, set the start command to:
```
sh -c "python api.py & streamlit run main.py --server.port=8501 --server.address=0.0.0.0"