from fastapi import APIRouter, HTTPException, status

from app.api.core.db import DbSession

from .models import DBProduct
from .schemas import Product, ProductCreate
from .service import (
    ProductNotFoundError,
    db_create_product,
    db_delete_product,
    db_find_product,
    db_read_product,
    db_read_products,
)


router = APIRouter(prefix="/products", tags=["products"])


@router.get("/")
def read_products(db: DbSession) -> list[Product]:
    products = db_read_products(db)
    return [Product.model_validate(product) for product in products]


@router.get("/{product_id}")
def read_product(db: DbSession, product_id: int) -> Product:
    try:
        product = db_read_product(db, product_id)
    except ProductNotFoundError as err:
        raise HTTPException(status_code=404, detail="Product not found") from err
    return product


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
