# 🐝 SwarmForge — Multi-Agent Swarm Orchestration Platform

<div align="center">

**Build, deploy, and monitor AI agent swarms at scale.**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![CI](https://img.shields.io/badge/CI-passing-brightgreen)]()
[![Docker](https://img.shields.io/badge/docker-ready-blue)]()

*In the era of GPT-6 (10T parameters), single-agent systems are obsolete. SwarmForge orchestrates teams of specialized AI agents working in parallel, hierarchical, or mesh topologies — with provider-agnostic LLM backends, streaming handoffs, and full observability.*

</div>

---

## 🎯 Why SwarmForge?

The AI world just changed. **OpenAI's GPT-6 (Astra)** with 10 trillion parameters is breaking the pretraining wall. **Kimi K2.5 Agent Swarms** prove that multiple specialized agents outperform any single model. **CrewAI, LangGraph, AutoGen** — the multi-agent paradigm is the new standard.

SwarmForge is the **production-grade orchestration layer** that makes multi-agent systems:
- **Pluggable** — swap OpenAI/Anthropic/DeepSeek/Google in one line
- **Scalable** — from 2 agents on a laptop to 200 agents on K8s
- **Observable** — Prometheus metrics, OpenTelemetry tracing, structured logging
- **Safe** — sandboxed execution, API key management, rate limiting

## 🏗️ Architecture

```
                    ┌─────────────────────────────────┐
                    │        SwarmForge API            │
                    │     (FastAPI + WebSocket)        │
                    └──────────┬──────────────────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
     ┌────────────┐   ┌────────────┐   ┌────────────┐
     │  Swarm A   │   │  Swarm B   │   │  Swarm C   │
     │ (Parallel) │   │(Hierarchy) │   │  (Mesh)    │
     └─────┬──────┘   └─────┬──────┘   └─────┬──────┘
           │                │                │
    ┌──────┼──────┐  ┌──────┼──────┐  ┌──────┼──────┐
    ▼      ▼      ▼  ▼      ▼      ▼  ▼      ▼      ▼
  Agent  Agent  Agent  Orchestrator  Agent  Agent  Agent
  (GPT) (Claude)(DS)   (Reviewer)   (Code) (Data) (Search)
           │                │                │
           └────────────────┼────────────────┘
                            ▼
              ┌─────────────────────────┐
              │    Handoff Protocol     │
              │  (Context + Artifacts)  │
              └─────────────────────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │  Redis   │ │PostgreSQL│ │Prometheus│
        │ (Cache)  │ │ (State)  │ │(Metrics) │
        └──────────┘ └──────────┘ └──────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Redis (for task queue)
- PostgreSQL (optional, for persistence)

### Install

```bash
git clone https://github.com/huzjie/swarmforge.git
cd swarmforge
pip install -e .
```

### Configure

```bash
cp .env.example .env
# Edit .env with your API keys
```

Minimal config:
```env
SWARMFORGE_OPENAI_API_KEY=sk-your-key
SWARMFORGE_DATABASE_URL=sqlite+aiosqlite:///swarmforge.db
SWARMFORGE_REDIS_URL=redis://localhost:6379/0
```

### Start the server

```bash
# Development
swarmforge serve start --reload

# Production
uvicorn swarmforge.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Create agents and run a swarm

```python
from swarmforge.core.agent import Agent, AgentConfig, AgentRole
from swarmforge.core.swarm import Swarm, SwarmConfig, SwarmTopology

# Create specialized agents
researcher = Agent(AgentConfig(
    name="researcher", role=AgentRole.RESEARCHER,
    capabilities=["web_search", "summarization"],
    model="gpt-4", provider="openai",
))

coder = Agent(AgentConfig(
    name="coder", role=AgentRole.CODER,
    capabilities=["code_generation", "code_review"],
    model="claude-sonnet-4-20250514", provider="anthropic",
))

reviewer = Agent(AgentConfig(
    name="reviewer", role=AgentRole.REVIEWER,
    capabilities=["quality_check", "fact_verification"],
))

# Create a swarm
swarm = Swarm(SwarmConfig(
    name="dev-team",
    topology=SwarmTopology.SEQUENTIAL,
))

swarm.add_agent(researcher)
swarm.add_agent(coder)
swarm.add_agent(reviewer)

# Run a task
result = await swarm.run("Build a REST API for a todo app")
print(f"Status: {result.status}, Results: {len(result.results)}")
```

### CLI

```bash
# Create agent
swarmforge agent create --name analyst --role researcher --model gpt-4

# Create swarm
swarmforge swarm create --name analytics-team --topology parallel --agents analyst,coder

# Run task
swarmforge run swarm analytics-team "Analyze Q3 sales data and generate report"
```

## 🐳 Docker

```bash
# Start full stack (API + Worker + Redis + PostgreSQL + Prometheus + Grafana)
docker-compose up -d

# Check health
curl http://localhost:8000/health
```

## ☸️ Kubernetes

```bash
kubectl apply -f deploy/k8s/deployment.yaml
kubectl apply -f deploy/k8s/ingress.yaml
kubectl apply -f deploy/k8s/hpa.yaml
```

## 📊 Monitoring

- **Prometheus** metrics at `/metrics`
- **Grafana** dashboard at `http://localhost:3000` (admin/admin)
- **OpenTelemetry** tracing (optional)

Key metrics:
- `swarmforge_agent_runs_total` — agent execution count
- `swarmforge_agent_run_duration_seconds` — agent latency histogram
- `swarmforge_swarm_runs_total` — swarm execution count
- `swarmforge_api_request_duration_seconds` — API latency

## 🔧 Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `SWARMFORGE_ENV` | `development` | Environment |
| `SWARMFORGE_OPENAI_API_KEY` | — | OpenAI API key |
| `SWARMFORGE_ANTHROPIC_API_KEY` | — | Anthropic API key |
| `SWARMFORGE_DEEPSEEK_API_KEY` | — | DeepSeek API key |
| `SWARMFORGE_LLM_DEFAULT_PROVIDER` | `openai` | Default LLM provider |
| `SWARMFORGE_MAX_CONCURRENT_AGENTS` | `50` | Max parallel agents |
| `SWARMFORGE_AGENT_TIMEOUT_SECONDS` | `300` | Agent timeout |

## 📚 API Reference

Full OpenAPI docs at `/docs` after starting the server.

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/api/v1/agents/` | Create agent |
| `GET` | `/api/v1/agents/` | List agents |
| `POST` | `/api/v1/agents/{name}/run` | Run agent task |
| `POST` | `/api/v1/swarms/` | Create swarm |
| `GET` | `/api/v1/swarms/` | List swarms |
| `POST` | `/api/v1/swarms/{name}/run` | Run swarm task |
| `POST` | `/api/v1/tasks/` | Submit task |
| `GET` | `/api/v1/tools/` | List tools |

## 🔒 Security

- API key authentication via `X-API-Key` header
- Sandboxed code execution
- Rate limiting (configurable)
- JWT token support
- PII-safe logging

## 🧪 Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v --cov=swarmforge

# Format code
black swarmforge/ tests/
ruff check --fix swarmforge/ tests/

# Type checking
mypy swarmforge/
```

## 📁 Project Structure

```
swarmforge/
├── core/               # Agent runtime, swarm engine, handoff, memory
│   ├── agent.py        # Individual agent with ReAct loop
│   ├── swarm.py        # Multi-agent orchestration (5 topologies)
│   ├── handoff.py      # Agent-to-agent context passing
│   ├── memory.py       # Conversation + long-term memory
│   └── tool.py         # Type-safe tool definitions
├── providers/          # LLM provider abstraction
│   ├── openai_provider.py
│   ├── anthropic_provider.py
│   ├── deepseek_provider.py
│   └── google_provider.py
├── api/                # FastAPI REST API
│   ├── main.py         # Application entry point
│   ├── middleware.py    # Logging, rate limiting
│   └── routes/         # Agent, Swarm, Task, Tool endpoints
├── db/                 # Database models + Alembic migrations
├── tasks/              # Celery background tasks
├── cli/                # Typer CLI
├── monitoring/         # Prometheus + OpenTelemetry
├── security/           # Auth + sandbox
├── deploy/             # K8s, Helm, Prometheus configs
└── tests/              # Comprehensive test suite
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 License

Apache 2.0 — see [LICENSE](LICENSE).

---

<div align="center">

**⭐ Star this repo if you find it useful! ⭐**

*Built by [AI Daily Agent](https://github.com/huzjie/ai-daily-agent) — August 10, 2026*

</div>
