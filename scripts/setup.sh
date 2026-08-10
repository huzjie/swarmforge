#!/bin/bash
set -e
echo "Setting up SwarmForge..."
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
cp .env.example .env 2>/dev/null || true
echo "Setup complete! Edit .env with your API keys."
