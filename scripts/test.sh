#!/bin/bash
set -e
pytest tests/ -v --cov=swarmforge --cov-report=html
echo "Tests complete. See htmlcov/index.html"
