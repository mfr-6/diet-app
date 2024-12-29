from unittest.mock import patch

from app.api.products.models import DBProduct
from app.api.products.service import ProductNotFoundError


def test_read_products_when_products_present(test_client) -> None:
    test_products = [
        DBProduct(id=1, name="Test-Product1"),
        DBProduct(id=2, name="Test-Product2"),
    ]

    with patch(
        "app.api.products.routes.db_read_products", return_value=test_products
    ) as mock_db_read_products:
        response = test_client.get("/api/v1/products/")
        # TODO: assert_called_once_with() -> find a way to access db: DbSession
        mock_db_read_products.assert_called_once()

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Test-Product1"},
        {"id": 2, "name": "Test-Product2"},
    ]


def test_read_products_when_products_missing(test_client) -> None:
    test_products = []

    with patch(
        "app.api.products.routes.db_read_products", return_value=test_products
    ) as mock_db_read_products:
        response = test_client.get("/api/v1/products/")
        # TODO: assert_called_once_with() -> find a way to access db: DbSession
        mock_db_read_products.assert_called_once()

    assert response.status_code == 200
    assert response.json() == []


def test_read_product_when_product_present(test_client) -> None:
    test_product_id = 666
    test_product = DBProduct(id=test_product_id, name="So tasty product")

    with patch(
        "app.api.products.routes.db_read_product", return_value=test_product
    ) as mock_db_read_product:
        response = test_client.get(f"/api/v1/products/{test_product_id}")
        # TODO: assert_called_once_with() -> find a way to access db: DbSession
        mock_db_read_product.assert_called_once()

    assert response.status_code == 200
    assert response.json() == {"id": test_product_id, "name": "So tasty product"}


def test_read_product_when_product_missing(test_client) -> None:
    with patch(
        "app.api.products.routes.db_read_product",
        side_effect=ProductNotFoundError("Product not found"),
    ) as mock_db_read_product:
        response = test_client.get("/api/v1/products/666")
        # TODO: assert_called_once_with() -> find a way to access db: DbSession
        mock_db_read_product.assert_called_once()

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_create_product(test_client) -> None:
    product_body = {"name": "Test Product 666"}
    test_product = DBProduct(id=5, name="Test Product 666")

    with patch(
        "app.api.products.routes.db_create_product", return_value=test_product
    ) as mock_db_create_product:
        response = test_client.post("/api/v1/products/", json=product_body)
        # TODO: assert_called_once_with() -> find a way to access db: DbSession
        mock_db_create_product.assert_called_once()

    assert response.status_code == 201
    assert response.json() == {"id": 5, "name": "Test Product 666"}


def test_create_product_wrong_body(test_client) -> None:
    wrong_body = {"sample": "body"}

    response = test_client.post("/api/v1/products", json=wrong_body)

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "name"],
                "msg": "Field required",
                "input": {"sample": "body"},
            }
        ]
    }


def test_create_product_no_body(test_client) -> None:
    response = test_client.post("/api/v1/products")

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {"type": "missing", "loc": ["body"], "msg": "Field required", "input": None}
        ]
    }


def test_delete_product_when_product_present(test_client) -> None:
    with patch(
        "app.api.products.routes.db_delete_product", return_value=None
    ) as mock_db_delete_product:
        response = test_client.delete("/api/v1/products/5")
        # TODO: assert_called_once_with() -> find a way to access db: DbSession
        mock_db_delete_product.assert_called_once()

    assert response.status_code == 204
    assert response.text == ""


def test_update_product_when_target_product_present(test_client) -> None:
    product_id = 3
    product_body = {"name": "Updated name"}
    updated_product = DBProduct(id=3, name="Updated name")

    with patch(
        "app.api.products.routes.db_update_product", return_value=updated_product
    ) as mock_db_update_product:
        response = test_client.put(f"/api/v1/products/{product_id}", json=product_body)
        mock_db_update_product.assert_called_once()

    assert response.status_code == 201
    assert response.json() == {"id": product_id, "name": "Updated name"}


def test_update_product_wrong_body(test_client) -> None:
    wrong_body = {"sample": "body"}

    response = test_client.put("/api/v1/products/666", json=wrong_body)

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "name"],
                "msg": "Field required",
                "input": {"sample": "body"},
            }
        ]
    }


def test_update_product_no_body(test_client) -> None:
    response = test_client.put("/api/v1/products/666")

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {"type": "missing", "loc": ["body"], "msg": "Field required", "input": None}
        ]
    }


def test_update_product_when_target_product_missing(test_client) -> None:
    product_id = 3
    product_body = {"name": "Updated name"}

    with patch(
        "app.api.products.routes.db_update_product",
        side_effect=ProductNotFoundError("Product not found"),
    ) as mock_db_update_product:
        response = test_client.put(f"/api/v1/products/{product_id}", json=product_body)
        mock_db_update_product.assert_called_once()

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_delete_product_when_product_missing(test_client) -> None:
    with patch(
        "app.api.products.routes.db_delete_product",
        side_effect=ProductNotFoundError("Product not found"),
    ) as mock_db_delete_product:
        response = test_client.delete("/api/v1/products/666")
        # TODO: assert_called_once_with() -> find a way to access db: DbSession
        mock_db_delete_product.assert_called_once()

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}
