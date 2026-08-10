# FAQ

**Q: Can I use SwarmForge without API keys?**
A: Yes, use Local provider with Ollama or vLLM.

**Q: How many agents can run concurrently?**
A: Configurable via `SWARMFORGE_MAX_CONCURRENT_AGENTS`, default 50.

**Q: Is SwarmForge production-ready?**
A: Yes, includes Docker, K8s, monitoring, CI/CD.

**Q: Can I add custom LLM providers?**
A: Yes, implement `BaseProvider` and register it.