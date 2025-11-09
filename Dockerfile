FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
COPY frontend ./frontend
COPY prompt.md .

RUN mkdir -p /app/uploads /app/outputs

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5001

# Use PORT environment variable (Render requires port 10000)
# Defaults to 5001 for local development
CMD gunicorn --bind 0.0.0.0:${PORT:-5001} --workers 2 --timeout 120 backend.api.app:app