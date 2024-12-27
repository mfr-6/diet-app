from .database import TestSessionLocal
from factory import Sequence
from factory.alchemy import SQLAlchemyModelFactory

from app.api.products.models import DBProduct

class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = TestSessionLocal()
        sqlalchemy_session_persistence = "commit"

class ProductFactory(BaseFactory):
    """Diet API Product Factory"""
    name = Sequence(lambda n: f"Product-{n}")
    class Meta:
        """Factory Configuration"""
        model = DBProduct

