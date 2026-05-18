FROM python:3.11-slim

# Nainstaluj Chrome + ChromeDriver
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV CHROMIUM_FLAGS="--no-sandbox --disable-dev-shm-usage --headless"

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Build (from project root):
#   docker build -f backend/Dockerfile -t equitygauge-backend .
# Run with persistent tickers.yaml:
#   docker run -p 8000:8000 -v $(pwd)/backend/tickers.yaml:/app/backend/tickers.yaml equitygauge-backend
