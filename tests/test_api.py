"""
Tests for the FastAPI application.
"""
import pytest
from httpx import AsyncClient, ASGITransport
from swarmforge.api.main import app


@pytest.mark.asyncio
async def test_root():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/")
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "SwarmForge"
        assert data["version"] == "0.1.0"


@pytest.mark.asyncio
async def test_health():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_health_live():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/health/live")
        assert resp.status_code == 200


@pytest.mark.asyncio
async def test_health_ready():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/health/ready")
        assert resp.status_code == 200


@pytest.mark.asyncio
async def test_list_agents_empty():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/agents/")
        assert resp.status_code == 200
        assert resp.json() == []


@pytest.mark.asyncio
async def test_create_agent():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/v1/agents/", json={
            "name": "test-api-agent",
            "role": "worker",
            "description": "API test agent",
            "capabilities": ["test"],
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "test-api-agent"


@pytest.mark.asyncio
async def test_list_swarms_empty():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/swarms/")
        assert resp.status_code == 200


@pytest.mark.asyncio
async def test_list_tools():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/tools/")
        assert resp.status_code == 200


@pytest.mark.asyncio
async def test_openapi_schema():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/openapi.json")
        assert resp.status_code == 200
        schema = resp.json()
        assert "paths" in schema
        assert "/api/v1/agents/" in schema["paths"]
