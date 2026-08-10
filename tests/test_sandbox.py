"""Tests for execution sandbox."""
import pytest
from swarmforge.security.sandbox import Sandbox

class TestSandbox:
    def test_execute_python_simple(self):
        sandbox = Sandbox()
        result = sandbox.execute_python("print('hello')")
        assert result["success"] is True

    def test_execute_python_error(self):
        sandbox = Sandbox()
        result = sandbox.execute_python("raise ValueError('test error')")
        assert result["success"] is False

    def test_execute_python_timeout(self):
        sandbox = Sandbox(timeout=1)
        result = sandbox.execute_python("import time; time.sleep(10)")
        assert result["success"] is False
        assert "timed out" in result.get("error", "").lower()

    def test_execute_shell(self):
        sandbox = Sandbox()
        result = sandbox.execute_shell("echo hello")
        assert result["success"] is True
