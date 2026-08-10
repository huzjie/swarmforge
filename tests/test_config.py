"""Tests for configuration."""
import pytest
from swarmforge.config import Settings

class TestSettings:
    def test_default_settings(self):
        s = Settings()
        assert s.env == "development"
        assert s.llm_default_provider == "openai"
        assert s.max_concurrent_agents == 50

    def test_env_prefix(self):
        import os
        os.environ["SWARMFORGE_DEBUG"] = "true"
        s = Settings()
        assert s.debug is True
        del os.environ["SWARMFORGE_DEBUG"]
