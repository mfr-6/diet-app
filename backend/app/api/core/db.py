from typing import Generator, Annotated
from fastapi import Depends
from peewee import SqliteDatabase, Model

DATABASE = 'diet.db'
db = SqliteDatabase(DATABASE)

class BaseModel(Model):
    class Meta:
        database = db

def get_session() -> Generator[SqliteDatabase, None, None]:
    try:
        db.connect()
        yield db
    finally:
        db.close()

DbSession = Annotated[SqliteDatabase, Depends(get_session)]
    