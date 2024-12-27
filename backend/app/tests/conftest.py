from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


from app.api.core.db import Base, get_db_session
from app.api.products.models import DBProduct  # noqa: F401

from sqlalchemy_utils import drop_database, database_exists
from .database import TEST_DB_URL, test_engine, TestSessionLocal

from .factories import (
    ProductFactory
)

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
    #TestSessionLocal.configure(bind=test_engine)
    yield
    drop_database(TEST_DB_URL)

@pytest.fixture(scope="function")
def db_session(db) -> Generator[Session, None, None]:
    """
    Creates a new database session for each test
    with a rollback at the end of the test.

    Rollback is not working because SAVEPOINT is not working properly in pysqlite
    https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#savepoint-support

    https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#serializable-isolation-savepoints-transactional-ddl
    """
    #connection = test_engine.connect()
    #transaction = connection.begin()
    #session = TestSessionLocal(bind=connection)

    session = TestSessionLocal()
    session.begin_nested()
    yield session
    session.rollback()
    
    #session.close()
    #transaction.rollback()
    #connection.close()

# @pytest.fixture(scope="module")
# def test_client(db_session: Session) -> Generator[TestClient, None, None]:
#     def override_get_db_session() -> Generator[Session, None, None]:
#         try:
#             yield db_session
#         finally:
#             db_session.close()

#     from app.main import app

#     app.dependency_overrides[get_db_session] = override_get_db_session
#     with TestClient(app) as client:
#         yield client

@pytest.fixture
def product(db_session: Session) -> DBProduct:  # noqa: ARG001
    return ProductFactory()

@pytest.fixture
def products(db_session: Session) -> list[DBProduct]:  # noqa: ARG001
    return [ProductFactory() for _ in range(2)]
