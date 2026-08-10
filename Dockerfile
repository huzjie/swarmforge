# SwarmForge — Multi-Agent Swarm Orchestration Platform
FROM python:3.14-slim AS builder

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY swarmforge/ swarmforge/

RUN pip install --no-cache-dir -e .

FROM python:3.14-slim AS runtime
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd -r swarmforge && useradd -r -g swarmforge swarmforge

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

RUN mkdir -p /app/data /app/logs && chown -R swarmforge:swarmforge /app
USER swarmforge

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV SWARMFORGE_ENV=production

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "swarmforge.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
