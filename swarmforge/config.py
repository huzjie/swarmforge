"""
SwarmForge Configuration — pydantic-settings based config with .env support.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="SWARMFORGE_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Environment ---
    env: str = "development"
    debug: bool = False
    log_level: str = "INFO"

    # --- Security ---
    secret_key: str = "change-me-in-production-use-a-random-string"
    api_key_header: str = "X-API-Key"

    # --- Database ---
    database_url: str = "postgresql+asyncpg://swarmforge:swarmforge@localhost:5432/swarmforge"
    database_pool_size: int = 20
    database_max_overflow: int = 10

    # --- Redis ---
    redis_url: str = "redis://localhost:6379/0"

    # --- LLM Providers ---
    llm_default_provider: str = "openai"
    openai_api_key: Optional[str] = None
    openai_base_url: str = "https://api.openai.com/v1"
    anthropic_api_key: Optional[str] = None
    deepseek_api_key: Optional[str] = None
    deepseek_base_url: str = "https://api.deepseek.com/v1"
    google_api_key: Optional[str] = None
    azure_openai_api_key: Optional[str] = None
    azure_openai_endpoint: Optional[str] = None

    # --- Agent Execution ---
    max_concurrent_agents: int = 50
    agent_timeout_seconds: int = 300
    max_retries: int = 3
    execution_sandbox_enabled: bool = True

    # --- Rate Limiting ---
    rate_limit_requests: int = 100
    rate_limit_period_seconds: int = 60

    # --- Monitoring ---
    prometheus_enabled: bool = True
    otel_enabled: bool = False
    otel_endpoint: str = "http://localhost:4317"

    # --- CORS ---
    cors_origins: str = "*"

    # --- Storage ---
    artifact_storage_path: str = "./data/artifacts"
    max_artifact_size_mb: int = 100

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str) -> List[str]:
        if v == "*":
            return ["*"]
        return [o.strip() for o in v.split(",")]


settings = Settings()
