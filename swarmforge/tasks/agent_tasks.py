"""
Agent-related Celery tasks.
"""
from __future__ import annotations

import logging
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def run_agent_task(agent_name: str, task: str, context: dict = None):
    """Execute a task on a specific agent."""
    logger.info(f"Running task on agent '{agent_name}': {task[:100]}")
    # In production, this would load the agent from DB and execute
    return {
        "agent": agent_name,
        "task": task,
        "status": "completed",
        "result": f"Task '{task[:50]}...' processed by {agent_name}",
    }


@shared_task
def cleanup_old_tasks():
    """Clean up old completed/failed tasks."""
    logger.info("Running task cleanup")
    return {"cleaned": 0}


@shared_task
def health_check_agents():
    """Periodic health check for all agents."""
    logger.info("Running agent health check")
    return {"healthy": True, "agents_checked": 0}
