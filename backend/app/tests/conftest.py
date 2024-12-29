from collections.abc import Generator
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, drop_database

from app.api.core.db import Base, get_db_session
from app.api.products.models import DBProduct

from .database import TEST_DB_URL, TestSessionLocal, test_engine
from .factories import ProductFactory

# https://pytest-with-eric.com/pytest-advanced/pytest-fastapi-testing/
# + inspired by setup done in Netflix Dispatch API


@pytest.fixture(scope="session")
def db() -> Generator[None, None, None]:
    """
    Creates a new database session for the whole test session.
    """
    if database_exists(TEST_DB_URL):
        drop_database(TEST_DB_URL)

    Base.metadata.create_all(bind=test_engine)
    TestSessionLocal.configure(bind=test_engine)
    yield
    drop_database(TEST_DB_URL)


@pytest.fixture(scope="function")
def db_session(db) -> Generator[Session, None, None]:  # noqa: ARG001, ANN001
    """
    Creates a new database session for each test
    with a rollback at the end of the test.

    Refs:
    https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
    """
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(
        bind=connection, join_transaction_mode="create_savepoint"
    )
    yield session
    transaction.rollback()
    TestSessionLocal.remove()


@pytest.fixture(scope="module")
def mock_db_session() -> Generator[Mock, None, None]:
    yield Mock()


@pytest.fixture(scope="module")
def test_client(mock_db_session: Mock) -> Generator[TestClient, None, None]:
    def override_get_db_session() -> Generator[Session, None, None]:
        try:
            yield mock_db_session
        finally:
            mock_db_session.close()

    from app.main import app

    app.dependency_overrides[get_db_session] = override_get_db_session
    with TestClient(app) as client:
        yield client


@pytest.fixture
def product(db_session: Session) -> DBProduct:  # noqa: ARG001
    return ProductFactory()


@pytest.fixture
def products(db_session: Session) -> list[DBProduct]:  # noqa: ARG001
    return [ProductFactory() for _ in range(3)]
