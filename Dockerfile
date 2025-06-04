# syntax=docker/dockerfile:1

# --- Build stage ---
FROM python:3.11-slim AS builder
WORKDIR /build
COPY requirements.txt ./
RUN pip install --user --no-cache-dir -r requirements.txt

# --- Final stage ---
FROM python:3.11-slim AS final
WORKDIR /app
# Копируем только необходимые файлы и зависимости из builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY app/ ./app
COPY config/ ./config
COPY logs/ ./logs
COPY .env ./
COPY requirements.txt ./

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
