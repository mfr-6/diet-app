import pytest

from app.api.products.models import DBProduct
from app.api.products.schemas import ProductCreate, ProductReplace
from app.api.products.service import (
    ProductNotFoundError,
    db_create_product,
    db_delete_product,
    db_find_product,
    db_read_product,
    db_read_products,
    db_replace_product,
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


def test_db_read_products(db_session, products) -> None:
    db_products = db_read_products(db_session)

    assert isinstance(db_products, list)
    assert len(db_products) == len(products)

    for db_product, product in zip(db_products, products, strict=False):
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


def test_db_replace_product(db_session, product) -> None:
    new_product = ProductReplace(name="replaced name")
    replaced_product = db_replace_product(db_session, product.id, new_product)

    assert replaced_product.id == product.id
    assert replaced_product.name == new_product.name


def test_db_update_product_not_found(db_session) -> None:
    new_product = ProductReplace(name="replaced name")
    with pytest.raises(ProductNotFoundError, match="Product not found"):
        db_replace_product(db_session, 999, new_product)


def test_db_delete_product(db_session) -> None:
    product = ProductCreate(name="test delete product")
    db_product = db_create_product(db_session, product)
    assert db_product.id is not None

    db_delete_product(db_session, db_product.id)
    with pytest.raises(ProductNotFoundError, match="Product not found"):
        db_read_product(db_session, db_product.id)


def test_db_delete_product_not_found(db_session) -> None:
    with pytest.raises(ProductNotFoundError, match="Product not found"):
        db_delete_product(db_session, 999)
