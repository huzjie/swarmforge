# Architecture

SwarmForge follows a modular microservices architecture:

- **Core**: Agent runtime, Swarm orchestration, Handoff protocol, Memory
- **Providers**: OpenAI, Anthropic, DeepSeek, Google, Azure, Together, Groq, Local
- **API**: FastAPI REST + WebSocket for real-time streaming
- **DB**: PostgreSQL (async) with SQLAlchemy + Alembic
- **Tasks**: Celery for background processing
- **Monitoring**: Prometheus + Grafana + OpenTelemetry