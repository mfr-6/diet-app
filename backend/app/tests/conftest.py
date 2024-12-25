import pytest
from collections.abc import Generator
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def test_client() -> Generator[TestClient, None, None]:
    from app.main import app

    client = TestClient(app)
    yield client
