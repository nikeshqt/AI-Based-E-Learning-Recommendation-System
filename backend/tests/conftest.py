import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """TestClient fixture for FastAPI endpoints."""
    with TestClient(app) as test_client:
        yield test_client
