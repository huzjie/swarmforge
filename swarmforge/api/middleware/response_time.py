"""response time middleware for SwarmForge API."""
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
import time

class response timeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        return response
