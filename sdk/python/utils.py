"""SwarmForge Python SDK - utils."""
class SwarmForgeUtils:
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = None):
        self.base_url = base_url
        self.api_key = api_key
