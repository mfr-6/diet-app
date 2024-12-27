from .models import DBProduct
from app.api.core.db import DbSession

def read_product(db_session: DbSession, product_id: int) -> DBProduct:
    return db_session.query(DBProduct).filter(DBProduct.id == product_id).first()

def read_products(db_session: DbSession) -> list[DBProduct]:
    return db_session.query(DBProduct).all()
