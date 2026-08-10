"""
Celery application for background task processing.
"""
from __future__ import annotations

from celery import Celery
from swarmforge.config import settings

app = Celery(
    "swarmforge",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["swarmforge.tasks.agent_tasks", "swarmforge.tasks.swarm_tasks"],
)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=settings.agent_timeout_seconds,
    task_soft_time_limit=settings.agent_timeout_seconds - 30,
    worker_max_tasks_per_child=200,
    worker_prefetch_multiplier=1,
    beat_schedule={
        "cleanup-old-tasks": {
            "task": "swarmforge.tasks.agent_tasks.cleanup_old_tasks",
            "schedule": 3600.0,  # every hour
        },
        "health-check-agents": {
            "task": "swarmforge.tasks.agent_tasks.health_check_agents",
            "schedule": 300.0,  # every 5 minutes
        },
    },
)
