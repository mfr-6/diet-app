from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/")
def read_products() -> list[dict[str, str]]:
    return [{"name": "apple", "price": 1.0}, {"name": "banana", "price": 0.5}]

@router.get("/{product_id}")
def read_product(product_id: int) -> dict[str, str]:
    return {"name": "apple", "price": 1.0}

@router.post("/")
def create_product() -> dict[str, str]:
    return {"name": "created product"}

@router.delete("/{product_id}")
def delete_product(product_id: int) -> dict[str, str]:
    return {"name": "deleted product"}