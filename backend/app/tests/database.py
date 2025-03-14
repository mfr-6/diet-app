from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import StaticPool

TEST_DB_URL = "sqlite:///test_db.db"
test_engine = create_engine(
    TEST_DB_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)

# Refs:
# https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#savepoint-support
# https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#serializable-isolation-savepoints-transactional-ddl
# https://github.com/sqlalchemy/sqlalchemy/discussions/7723
# https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites


@event.listens_for(test_engine, "connect")
def do_connect(dbapi_connection, connection_record):  # noqa: ANN001, ANN201, ARG001
    # disable pysqlite's emitting of the BEGIN statement entirely.
    # also stops it from emitting COMMIT before any DDL.
    dbapi_connection.isolation_level = None


@event.listens_for(test_engine, "begin")
def do_begin(conn):  # noqa: ANN001, ANN201
    # emit our own BEGIN
    conn.exec_driver_sql("BEGIN")


TestSessionLocal = scoped_session(sessionmaker())
