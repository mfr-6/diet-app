from .models import DBProduct
from app.api.core.db import DbSession

def read_product(db_session: DbSession, product_id: int) -> DBProduct:
    product = db_session.query(DBProduct).filter(DBProduct.id == product_id).first()
    return product

def read_products(db_session: DbSession) -> list[DBProduct]:
    products = db_session.query(DBProduct).all()
    return products

