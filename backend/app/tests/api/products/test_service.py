import pytest
from sqlalchemy import select

from app.api.products.models import DBProduct
from app.api.products.schemas import ProductCreate, ProductUpdate
from app.api.products.service import (
    ProductNotFoundError,
    db_create_product,
    db_delete_product,
    db_find_product,
    db_read_product,
    db_read_products,
    db_update_product,
)


def test_db_find_product(db_session, product) -> None:
    db_product = db_find_product(db_session, product.id)

    assert isinstance(db_product, DBProduct)
    assert db_product.id == product.id
    assert db_product.name == product.name


def test_db_find_product_not_found(db_session) -> None:
    with pytest.raises(ProductNotFoundError, match="Product not found"):
        db_find_product(db_session, 999)


def test_db_read_product(db_session, product) -> None:
    db_product = db_read_product(db_session, product.id)

    assert isinstance(db_product, DBProduct)
    assert db_product.id == product.id
    assert db_product.name == product.name


def test_db_read_product_not_found(db_session) -> None:
    with pytest.raises(ProductNotFoundError, match="Product not found"):
        db_read_product(db_session, 999)


def test_db_read_products(db_session) -> None:
    products_data = [
        DBProduct(name="test product 1"),
        DBProduct(name="test product 2"),
        DBProduct(name="test product 3"),
    ]
    for product in products_data:
        db_session.add(product)
    db_session.commit()

    db_products = db_read_products(db_session)

    assert isinstance(db_products, list)
    assert len(db_products) == len(products_data)

    for db_product, product in zip(db_products, products_data, strict=False):
        assert isinstance(db_product, DBProduct)
        assert db_product.id == product.id
        assert db_product.name == product.name


def test_db_read_products_not_found(db_session) -> None:
    db_products = db_read_products(db_session)

    assert isinstance(db_products, list)
    assert len(db_products) == 0


def test_db_create_product(db_session) -> None:
    product = ProductCreate(name="test create product")
    db_product = db_create_product(db_session, product)

    assert isinstance(db_product, DBProduct)
    assert db_product.id is not None
    assert db_product.name == product.name


def test_db_update_product(db_session) -> None:
    original_product = DBProduct(name="original name")
    db_session.add(original_product)
    db_session.commit()

    new_product = ProductUpdate(name="replaced name")
    replaced_product = db_update_product(db_session, original_product.id, new_product)

    assert replaced_product.id == original_product.id
    assert replaced_product.name == new_product.name

    result = db_session.execute(
        select(DBProduct).where(DBProduct.id == original_product.id)
    )
    db_product = result.scalar_one()
    assert db_product.name == new_product.name


def test_db_update_product_not_found(db_session) -> None:
    new_product = ProductUpdate(name="replaced name")
    with pytest.raises(ProductNotFoundError, match="Product not found"):
        db_update_product(db_session, 999, new_product)


def test_db_delete_product(db_session) -> None:
    product = DBProduct(name="test delete product")
    db_session.add(product)
    db_session.commit()

    db_delete_product(db_session, product.id)
    result = db_session.execute(select(DBProduct).where(DBProduct.id == product.id))
    assert result.first() is None


def test_db_delete_product_not_found(db_session) -> None:
    with pytest.raises(ProductNotFoundError, match="Product not found"):
        db_delete_product(db_session, 999)


@pytest.mark.parametrize("invalid_id", [-1, 0, 999999])
def test_db_find_product_invalid_ids(db_session, invalid_id) -> None:
    with pytest.raises(ProductNotFoundError, match="Product not found"):
        db_find_product(db_session, invalid_id)
