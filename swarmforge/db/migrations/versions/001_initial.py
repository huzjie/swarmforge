"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-08-10
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "agents",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(128), unique=True, nullable=False, index=True),
        sa.Column("role", sa.String(32), nullable=False, default="worker"),
        sa.Column("description", sa.Text),
        sa.Column("system_prompt", sa.Text),
        sa.Column("model", sa.String(64), default="gpt-4"),
        sa.Column("provider", sa.String(32), default="openai"),
        sa.Column("temperature", sa.Float, default=0.7),
        sa.Column("max_tokens", sa.Integer, default=4096),
        sa.Column("capabilities", sa.JSON),
        sa.Column("tools", sa.JSON),
        sa.Column("max_iterations", sa.Integer, default=10),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
    )

    op.create_table(
        "swarms",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("name", sa.String(128), unique=True, nullable=False, index=True),
        sa.Column("topology", sa.String(32), default="parallel"),
        sa.Column("max_concurrent", sa.Integer, default=10),
        sa.Column("timeout_seconds", sa.Integer, default=600),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
    )

    op.create_table(
        "swarm_agents",
        sa.Column("swarm_id", sa.String(36), sa.ForeignKey("swarms.id"), primary_key=True),
        sa.Column("agent_id", sa.String(36), sa.ForeignKey("agents.id"), primary_key=True),
    )

    op.create_table(
        "tasks",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("task", sa.Text, nullable=False),
        sa.Column("swarm_id", sa.String(36), sa.ForeignKey("swarms.id")),
        sa.Column("agent_id", sa.String(36), sa.ForeignKey("agents.id")),
        sa.Column("priority", sa.Integer, default=0),
        sa.Column("status", sa.String(32), default="pending", index=True),
        sa.Column("result", sa.JSON),
        sa.Column("error", sa.Text),
        sa.Column("metadata", sa.JSON),
        sa.Column("tokens_used", sa.Integer, default=0),
        sa.Column("latency_ms", sa.Float, default=0.0),
        sa.Column("created_at", sa.DateTime),
        sa.Column("completed_at", sa.DateTime),
    )

    op.create_table(
        "execution_logs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("task_id", sa.String(36), sa.ForeignKey("tasks.id")),
        sa.Column("agent_name", sa.String(128)),
        sa.Column("event_type", sa.String(64), index=True),
        sa.Column("message", sa.Text),
        sa.Column("metadata", sa.JSON),
        sa.Column("tokens_used", sa.Integer, default=0),
        sa.Column("latency_ms", sa.Float, default=0.0),
        sa.Column("created_at", sa.DateTime),
    )

    op.create_table(
        "api_keys",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("key_hash", sa.String(256), unique=True, nullable=False),
        sa.Column("name", sa.String(128)),
        sa.Column("permissions", sa.JSON),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("last_used_at", sa.DateTime),
        sa.Column("created_at", sa.DateTime),
        sa.Column("expires_at", sa.DateTime),
    )


def downgrade() -> None:
    op.drop_table("api_keys")
    op.drop_table("execution_logs")
    op.drop_table("tasks")
    op.drop_table("swarm_agents")
    op.drop_table("swarms")
    op.drop_table("agents")
