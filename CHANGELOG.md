# Changelog

## [0.1.0] - 2026-08-10

### Added
- Initial release of SwarmForge
- Core agent runtime with ReAct loop
- Multi-agent swarm orchestration (5 topologies: sequential, parallel, hierarchical, mesh, broadcast)
- Handoff protocol with 4 strategies (round-robin, capability-match, load-balanced, broadcast)
- Conversation and long-term memory systems
- Type-safe tool system with OpenAI/Anthropic schema generation
- 4 LLM providers: OpenAI, Anthropic, DeepSeek, Google
- FastAPI REST API with agent/swarm/task/tool endpoints
- Typer CLI for command-line management
- Celery background task processing
- SQLAlchemy models with Alembic migrations
- Prometheus metrics and OpenTelemetry tracing
- Docker + Docker Compose support
- Kubernetes deployment manifests (Deployment, Service, Ingress, HPA)
- GitHub Actions CI/CD
- Comprehensive test suite
- Full documentation
