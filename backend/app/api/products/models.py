from app.api.core.db import BaseModel
from peewee import CharField

class Product(BaseModel):
    name = CharField()
