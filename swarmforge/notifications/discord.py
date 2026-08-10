"""Discord notification channel."""
from dataclasses import dataclass
from typing import Optional

@dataclass
class DiscordConfig:
    enabled: bool = False
    webhook_url: Optional[str] = None

class DiscordNotifier:
    def __init__(self, config: DiscordConfig):
        self.config = config

    async def send(self, title: str, message: str) -> bool:
        if not self.config.enabled:
            return False
        # Implementation would send to discord
        return True
