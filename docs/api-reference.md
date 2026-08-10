# API Reference

Full OpenAPI docs available at `/docs` when server is running.

## Authentication
API key via `X-API-Key` header.

## Endpoints
- `POST /api/v1/agents/` - Create agent
- `POST /api/v1/agents/{name}/run` - Execute agent task
- `POST /api/v1/swarms/` - Create swarm
- `POST /api/v1/swarms/{name}/run` - Execute swarm task
- `GET /api/v1/tools/` - List available tools