from collections.abc import AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from src.main import get_app


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """Set the backend for the anyio plugin."""
    return "asyncio"


@pytest.fixture
def app() -> FastAPI:
    """Provide the FastAPI app instance (session-wide)."""
    return get_app()


@pytest.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Provide a test client for the FastAPI app."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
