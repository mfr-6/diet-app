from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/")
def read_products():
    return [{"name": "apple", "price": 1.0}, {"name": "banana", "price": 0.5}]

@router.get("/{product_id}")
def read_product(product_id: int):
    return {"name": "apple", "price": 1.0}

@router.post("/")
def create_product():
    return {"name": "created product"}

@router.delete("/{product_id}")
def delete_product(product_id: int):
    return {"name": "deleted product"}