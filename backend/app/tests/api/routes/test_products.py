from fastapi.testclient import TestClient

def test_read_products(test_client: TestClient) -> None:
    response = test_client.get("/products/")
    assert response.status_code == 200
    assert response.json() == [{"name": "apple", "price": 1.0}, {"name": "banana", "price": 0.5}]

def test_read_product(test_client: TestClient) -> None:
    response = test_client.get("/products/1")
    assert response.status_code == 200
    assert response.json() == {"name": "apple", "price": 1.0}

def test_create_product(test_client: TestClient) -> None:
    response = test_client.post("/products/")
    assert response.status_code == 200
    assert response.json() == {"name": "created product"}

def test_delete_product(test_client: TestClient) -> None:
    response = test_client.delete("/products/1")
    assert response.status_code == 200
    assert response.json() == {"name": "deleted product"}