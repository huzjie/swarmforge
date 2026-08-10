# Contributing to SwarmForge

## Development Setup

```bash
git clone https://github.com/huzjie/swarmforge.git
cd swarmforge
pip install -e ".[dev]"
pre-commit install
```

## Code Style

- Black for formatting (line length 100)
- Ruff for linting
- MyPy for type checking
- Pytest for testing

## Pull Request Process

1. Fork and create a feature branch
2. Add tests for new functionality
3. Ensure CI passes
4. Update docs if needed
5. Submit PR with description

## Commit Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `test:` tests
- `refactor:` code restructuring
- `chore:` maintenance
