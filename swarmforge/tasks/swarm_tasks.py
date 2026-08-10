"""
Swarm-related Celery tasks.
"""
from __future__ import annotations

import logging
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def run_swarm_task(swarm_name: str, task: str, context: dict = None):
    """Execute a task on a swarm."""
    logger.info(f"Running task on swarm '{swarm_name}': {task[:100]}")
    return {
        "swarm": swarm_name,
        "task": task,
        "status": "completed",
    }


@shared_task
def orchestrate_workflow(workflow_def: dict):
    """Execute a multi-step workflow across agents/swarms."""
    steps = workflow_def.get("steps", [])
    results = []
    for step in steps:
        results.append({
            "step": step.get("name", "unknown"),
            "status": "completed",
        })
    return {"workflow": workflow_def.get("name"), "steps_completed": len(results)}
