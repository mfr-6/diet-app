from app.api.core.db import DbSession

from .models import DBProduct


def read_product(db_session: DbSession, product_id: int) -> DBProduct:
    return db_session.query(DBProduct).filter(DBProduct.id == product_id).first()

def read_products(db_session: DbSession) -> list[DBProduct]:
    return db_session.query(DBProduct).all()

