"""Azure_blob storage backend."""
from pathlib import Path
from typing import Optional, BinaryIO

class Azure_blobStorage:
    def __init__(self, **kwargs):
        self.config = kwargs

    async def upload(self, key: str, data: bytes) -> str:
        return key

    async def download(self, key: str) -> Optional[bytes]:
        return None

    async def delete(self, key: str) -> bool:
        return True

    async def exists(self, key: str) -> bool:
        return False
