"""
Execution sandbox for safe agent code execution.
"""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from typing import Optional


class Sandbox:
    """Secure execution sandbox for agent-generated code."""

    def __init__(self, timeout: int = 30, max_memory_mb: int = 256):
        self.timeout = timeout
        self.max_memory_mb = max_memory_mb

    def execute_python(self, code: str) -> dict:
        """Execute Python code in a subprocess sandbox."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as f:
            f.write(code)
            tmp_path = f.name

        try:
            result = subprocess.run(
                ["python", "-u", tmp_path],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=tempfile.gettempdir(),
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"Execution timed out after {self.timeout}s"}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def execute_shell(self, command: str) -> dict:
        """Execute a shell command in a sandbox."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=tempfile.gettempdir(),
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"Execution timed out after {self.timeout}s"}
        except Exception as e:
            return {"success": False, "error": str(e)}
