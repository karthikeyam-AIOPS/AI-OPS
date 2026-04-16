# --- Build stage ---
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# --- Runtime stage ---
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY ai_ops/ ./ai_ops/

# Non-root user for security
RUN useradd --no-create-home --shell /bin/false appuser \
    && mkdir -p /app/.cache/huggingface \
    && chown -R appuser:appuser /app
USER appuser

# Redirect Hugging Face and Transformers cache to a writable path.
# /home/appuser does not exist (--no-create-home), so the default
# ~/.cache/huggingface would cause a PermissionError at model download time.
ENV HF_HOME=/app/.cache/huggingface \
    TRANSFORMERS_CACHE=/app/.cache/huggingface \
    HF_DATASETS_CACHE=/app/.cache/huggingface/datasets

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "ai_ops.ragapi:app", "--host", "0.0.0.0", "--port", "8000"]
