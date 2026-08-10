"""
SwarmForge API Server — FastAPI application entry point.
"""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from swarmforge.config import settings
from swarmforge.api.routes import health, agents, swarms, tasks, tools
from swarmforge.api.middleware import LoggingMiddleware, RateLimitMiddleware
from swarmforge.monitoring.metrics import setup_metrics


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan — startup/shutdown events."""
    # Startup
    import logging
    logger = logging.getLogger("swarmforge")
    logger.info(f"SwarmForge API starting (env={settings.env})")

    # Initialize metrics
    if settings.prometheus_enabled:
        setup_metrics(app)

    yield

    # Shutdown
    logger.info("SwarmForge API shutting down")


app = FastAPI(
    title="SwarmForge API",
    description="Multi-Agent Swarm Orchestration Platform",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)

# Routes
app.include_router(health.router, tags=["Health"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["Agents"])
app.include_router(swarms.router, prefix="/api/v1/swarms", tags=["Swarms"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["Tasks"])
app.include_router(tools.router, prefix="/api/v1/tools", tags=["Tools"])


@app.get("/", include_in_schema=False)
async def root():
    return {
        "name": "SwarmForge",
        "version": "0.1.0",
        "description": "Multi-Agent Swarm Orchestration Platform",
        "docs": "/docs",
    }
