from sqlalchemy import Column, Integer, String, create_engine, select, event
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Script that tests the rollback functionality in SQLite.
# For some reason event listeners are not working as expected from SQLalchemy 2.0 and upwards.

Base = declarative_base()


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r})"

test_db_url = "sqlite+pysqlite:///:memory:"

engine = create_engine(test_db_url, future=True, echo=False)

Base.metadata.create_all(bind=engine)

@event.listens_for(engine, "connect")
def do_connect(dbapi_connection, connection_record):
    # disable pysqlite's emitting of the BEGIN statement entirely.
    # also stops it from emitting COMMIT before any DDL.
    dbapi_connection.isolation_level = None

@event.listens_for(engine, "begin")
def do_begin(conn):
    # emit our own BEGIN
    conn.exec_driver_sql("BEGIN")

TestSession = sessionmaker()
#TestSession.configure(bind=engine)

connection = engine.connect()
transaction = connection.begin()
session = TestSession(bind=connection, join_transaction_mode="create_savepoint")

#s = session.begin_nested()

#session = TestSession()
#s=session.begin_nested()

test_user = User(name="John")
print(f"PRE_ADD: {session.in_transaction()}")
session.add(test_user)
print(f"AFTER_ADD: {session.in_transaction()}")
session.commit()
print(f"AFTER_COMMIT: {session.in_transaction()}")

print(f"DB content after commit: {session.execute(select(User)).scalar()}")
# DB content after commit: User(id=1, name='John')

transaction.rollback()  # not working as expected

print(f"DB content after rollback: {session.execute(select(User)).scalar()}")
# DB content after rollback: User(id=1, name='John')
session.close()
connection.close()
# with Session(engine) as session:

#     #session.begin_nested()

#     test_user = User(name="John")
#     print(f"PRE_ADD: {session.in_transaction()}")
#     session.add(test_user)
#     print(f"AFTER_ADD: {session.in_transaction()}")
#     session.commit()
#     print(f"AFTER_COMMIT: {session.in_transaction()}")

#     print(f"DB content after commit: {session.execute(select(User)).scalar()}")
#     # DB content after commit: User(id=1, name='John')

#     session.rollback()  # not working as expected
#     print(f"DB content after rollback: {session.execute(select(User)).scalar()}")
#     # DB content after rollback: User(id=1, name='John')