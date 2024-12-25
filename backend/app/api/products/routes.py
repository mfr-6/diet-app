from fastapi import APIRouter, HTTPException, status

from app.api.core.db import DbSession

from .models import DBProduct
from .schemas import Product, ProductCreate

# from sqlalchemy import select

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/")
def read_products(db: DbSession) -> list[Product]:
    # https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html
    # statement = select(Product)
    # products = db.execute(statement).all()
    # products = db.get(Product)
    products = db.query(DBProduct).all()
    return [Product.model_validate(product) for product in products]
    # return [
    #     {
    #         "name": "apple",
    #         "price": 1.0
    #     },
    #     {
    #         "name": "banana",
    #         "price": 0.5
    #     }
    # ]


@router.get("/{product_id}")
def read_product(db: DbSession, product_id: int) -> Product:
    product = db.get(DBProduct, product_id)
    return Product.model_validate(product)
    # return {
    #     "id": product_id,
    #     "name": "apple",
    #     "price": 1.0
    # }


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(db: DbSession, product: ProductCreate) -> Product:
    product = DBProduct(**product.model_dump())

    db.add(product)
    db.commit()
    db.refresh(product)

    return Product.model_validate(product)

    # {"id": product.id, "name": product.name}


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(db: DbSession, product_id: int) -> dict:
    product = db.get(DBProduct, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()

    return {}
