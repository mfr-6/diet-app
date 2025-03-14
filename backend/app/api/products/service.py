from sqlalchemy import select

from app.api.core.db import DbSession

from .models import DBProduct
from .schemas import ProductCreate, ProductUpdate


class ProductNotFoundError(Exception):
    pass


def db_find_product(db_session: DbSession, product_id: int) -> DBProduct:
    product = db_session.get(DBProduct, product_id)
    if product is None:
        msg = "Product not found"
        raise ProductNotFoundError(msg)
    return product


def db_read_product(db_session: DbSession, product_id: int) -> DBProduct:
    return db_find_product(db_session, product_id)


def db_read_products(db_session: DbSession) -> list[DBProduct]:
    statement = select(DBProduct)
    return db_session.execute(statement).scalars().all()


def db_create_product(db_session: DbSession, product: ProductCreate) -> DBProduct:
    db_product = DBProduct(**product.model_dump())
    db_session.add(db_product)
    db_session.commit()

    return db_product


def db_update_product(
    db_session: DbSession, product_id: int, product: ProductUpdate
) -> DBProduct:
    db_product = db_read_product(db_session, product_id)
    new_product = DBProduct(id=product_id, **product.model_dump())

    db_session.delete(db_product)
    db_session.add(new_product)
    db_session.commit()

    return new_product


def db_delete_product(db_session: DbSession, product_id: int) -> None:
    db_product = db_find_product(db_session, product_id)
    db_session.delete(db_product)
    db_session.commit()
