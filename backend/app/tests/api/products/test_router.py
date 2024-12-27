# import random

# from fastapi.testclient import TestClient


# def test_read_products(test_client: TestClient) -> None:
#     response = test_client.get("/api/v1/products/")
#     assert response.status_code == 200
#     assert response.json() == [
#         {"name": "apple", "price": 1.0},
#         {"name": "banana", "price": 0.5},
#     ]


# def test_read_product(test_client: TestClient) -> None:
#     test_product_id = random.randint(1, 100)
#     response = test_client.get(f"/api/v1/products/{test_product_id}")
#     assert response.status_code == 200
#     assert response.json() == {"id": test_product_id, "name": "apple", "price": 1.0}


# def test_create_product(test_client: TestClient) -> None:
#     response = test_client.post("/api/v1/products/")
#     assert response.status_code == 201
#     assert response.json() == {"name": "created product"}


# def test_delete_product(test_client: TestClient) -> None:
#     test_product_id = random.randint(1, 100)
#     response = test_client.delete(f"/api/v1/products/{test_product_id}")
#     assert response.status_code == 200
#     assert response.json() == {"id": test_product_id, "name": "deleted product"}
