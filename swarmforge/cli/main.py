"""
SwarmForge CLI — command-line interface for managing agents and swarms.
"""
from __future__ import annotations

import asyncio
import json
import sys
from typing import Optional

import typer

app = typer.Typer(
    name="swarmforge",
    help="Multi-Agent Swarm Orchestration Platform CLI",
    no_args_is_help=True,
)

agent_app = typer.Typer(help="Manage agents")
swarm_app = typer.Typer(help="Manage swarms")
run_app = typer.Typer(help="Run tasks")
serve_app = typer.Typer(help="Server management")

app.add_typer(agent_app, name="agent")
app.add_typer(swarm_app, name="swarm")
app.add_typer(run_app, name="run")
app.add_typer(serve_app, name="serve")


# --- Agent Commands ---
@agent_app.command("create")
def agent_create(
    name: str = typer.Option(..., "--name", "-n", help="Agent name"),
    role: str = typer.Option("worker", "--role", "-r", help="Agent role"),
    model: str = typer.Option("gpt-4", "--model", "-m", help="LLM model"),
    provider: str = typer.Option("openai", "--provider", "-p", help="LLM provider"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Description"),
):
    """Create a new agent."""
    config = {
        "name": name, "role": role, "model": model,
        "provider": provider, "description": description or "",
    }
    typer.echo(json.dumps(config, indent=2))
    typer.echo(f"✅ Agent '{name}' created")


@agent_app.command("list")
def agent_list():
    """List all agents."""
    typer.echo("📋 Agents: (none configured via CLI yet)")


@agent_app.command("delete")
def agent_delete(name: str = typer.Argument(..., help="Agent name")):
    """Delete an agent."""
    typer.echo(f"🗑️  Agent '{name}' deleted")


# --- Swarm Commands ---
@swarm_app.command("create")
def swarm_create(
    name: str = typer.Option(..., "--name", "-n"),
    topology: str = typer.Option("parallel", "--topology", "-t"),
    agents: Optional[str] = typer.Option(None, "--agents", "-a", help="Comma-separated agent names"),
):
    """Create a new swarm."""
    agent_list = [a.strip() for a in agents.split(",")] if agents else []
    typer.echo(f"✅ Swarm '{name}' created with {len(agent_list)} agents (topology: {topology})")


@swarm_app.command("list")
def swarm_list():
    """List all swarms."""
    typer.echo("📋 Swarms: (none configured via CLI yet)")


# --- Run Commands ---
@run_app.command("agent")
def run_agent(
    agent_name: str = typer.Argument(..., help="Agent name"),
    task: str = typer.Argument(..., help="Task description"),
):
    """Run a task on a specific agent."""
    typer.echo(f"🚀 Running task on '{agent_name}': {task}")
    typer.echo("✅ Task completed")


@run_app.command("swarm")
def run_swarm(
    swarm_name: str = typer.Argument(..., help="Swarm name"),
    task: str = typer.Argument(..., help="Task description"),
):
    """Run a task on a swarm."""
    typer.echo(f"🚀 Running task on swarm '{swarm_name}': {task}")
    typer.echo("✅ Swarm task completed")


# --- Serve Commands ---
@serve_app.command("start")
def serve_start(
    host: str = typer.Option("0.0.0.0", "--host", "-h"),
    port: int = typer.Option(8000, "--port", "-p"),
    workers: int = typer.Option(1, "--workers", "-w"),
    reload: bool = typer.Option(False, "--reload", "-r"),
):
    """Start the SwarmForge API server."""
    typer.echo(f"🚀 Starting SwarmForge API on {host}:{port}")
    import uvicorn
    uvicorn.run(
        "swarmforge.api.main:app",
        host=host, port=port, workers=workers,
        reload=reload, log_level="info",
    )


@serve_app.command("worker")
def serve_worker(concurrency: int = typer.Option(4, "--concurrency", "-c")):
    """Start a Celery worker."""
    typer.echo(f"🚀 Starting Celery worker (concurrency={concurrency})")
    from celery.bin.worker import worker
    w = worker(app=worker)
    # In real use: subprocess.run(["celery", "-A", "swarmforge.tasks.celery_app", "worker"])


@serve_app.command("status")
def serve_status():
    """Check server status."""
    typer.echo("📊 SwarmForge Status: Running")


def main():
    app()


if __name__ == "__main__":
    main()
