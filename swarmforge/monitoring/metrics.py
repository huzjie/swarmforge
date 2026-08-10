"""
Prometheus metrics for SwarmForge.
"""
from __future__ import annotations

from prometheus_client import Counter, Histogram, Gauge, generate_latest, REGISTRY
from fastapi import FastAPI, Request, Response


# Agent metrics
agent_runs_total = Counter(
    "swarmforge_agent_runs_total",
    "Total number of agent runs",
    ["agent_name", "status"],
)

agent_run_duration_seconds = Histogram(
    "swarmforge_agent_run_duration_seconds",
    "Agent run duration in seconds",
    ["agent_name"],
    buckets=[0.1, 0.5, 1, 2, 5, 10, 30, 60, 120, 300],
)

agent_tokens_total = Counter(
    "swarmforge_agent_tokens_total",
    "Total tokens consumed by agents",
    ["agent_name", "type"],  # type: prompt, completion
)

# Swarm metrics
swarm_runs_total = Counter(
    "swarmforge_swarm_runs_total",
    "Total number of swarm runs",
    ["swarm_name", "topology", "status"],
)

swarm_active_agents = Gauge(
    "swarmforge_swarm_active_agents",
    "Number of active agents in a swarm",
    ["swarm_name"],
)

# API metrics
api_requests_total = Counter(
    "swarmforge_api_requests_total",
    "Total API requests",
    ["method", "endpoint", "status_code"],
)

api_request_duration_seconds = Histogram(
    "swarmforge_api_request_duration_seconds",
    "API request duration",
    ["method", "endpoint"],
)


def setup_metrics(app: FastAPI) -> None:
    """Set up Prometheus metrics endpoint."""

    @app.get("/metrics", include_in_schema=False)
    async def metrics():
        return Response(content=generate_latest(REGISTRY), media_type="text/plain")

    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next):
        import time
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start

        api_requests_total.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code,
        ).inc()

        api_request_duration_seconds.labels(
            method=request.method,
            endpoint=request.url.path,
        ).observe(duration)

        return response
