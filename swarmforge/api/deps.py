"""
SwarmForge API Dependencies — FastAPI dependency injection.
"""
from __future__ import annotations

from typing import Optional

from fastapi import Depends, Header, HTTPException, status

from swarmforge.config import settings


async def verify_api_key(
    x_api_key: Optional[str] = Header(None, alias=settings.api_key_header),
) -> str:
    """Verify API key from header (if configured)."""
    # In development mode, skip auth
    if settings.env == "development" or settings.debug:
        return "dev-user"

    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required",
        )
    # In production, validate against stored keys
    return x_api_key


def get_pagination(page: int = 1, size: int = 20) -> tuple[int, int]:
    """Pagination dependency."""
    page = max(1, page)
    size = min(max(1, size), 100)
    return page, size
