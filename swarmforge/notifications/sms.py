"""Sms notification channel."""
from dataclasses import dataclass
from typing import Optional

@dataclass
class SmsConfig:
    enabled: bool = False
    webhook_url: Optional[str] = None

class SmsNotifier:
    def __init__(self, config: SmsConfig):
        self.config = config

    async def send(self, title: str, message: str) -> bool:
        if not self.config.enabled:
            return False
        # Implementation would send to sms
        return True
