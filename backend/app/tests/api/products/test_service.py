from app.api.products.models import DBProduct
from app.api.products.service import read_product, read_products


def test_read_product(db_session, product) -> None:
    test_product = read_product(db_session, product.id)

    assert isinstance(test_product, DBProduct)
    assert test_product.id == product.id
    assert test_product.name == product.name

def test_read_product_not_found(db_session) -> None:
    test_product = read_product(db_session, 999)

    assert test_product is None

def test_read_products(db_session, products) -> None:
    test_products = read_products(db_session)

    assert isinstance(test_products, list)
    assert len(test_products) == len(products)

    for test_product, product in zip(test_products, products, strict=False):
        assert isinstance(test_product, DBProduct)
        assert test_product.id == product.id
        assert test_product.name == product.name
