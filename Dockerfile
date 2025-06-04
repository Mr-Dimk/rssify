# syntax=docker/dockerfile:1

# --- Build stage ---
FROM python:3.11.9-slim-bookworm AS builder
WORKDIR /build
COPY requirements.txt ./
RUN apt-get update && apt-get upgrade -y && apt-get install -y gcc build-essential && \
    pip install --user --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc build-essential && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# --- Final stage ---
FROM python:3.11.9-slim-bookworm AS final
WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY app/ ./app
COPY config/ ./config
COPY logs/ ./logs
COPY .env ./
COPY requirements.txt ./
# EXCLUDE redundant COPY app/templates and app/static (already in app/)

# Безопасный пользователь
RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
