from fastapi import APIRouter, HTTPException, status

from app.api.core.db import DbSession

from .schemas import Product, ProductCreate, ProductUpdate
from .service import (
    ProductNotFoundError,
    db_create_product,
    db_delete_product,
    db_read_product,
    db_read_products,
    db_update_product,
)

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", status_code=status.HTTP_200_OK)
def read_products(db: DbSession) -> list[Product]:
    db_products = db_read_products(db)
    return [Product.model_validate(product) for product in db_products]


@router.get("/{product_id}", status_code=status.HTTP_200_OK)
def read_product(db: DbSession, product_id: int) -> Product:
    try:
        db_product = db_read_product(db, product_id)
    except ProductNotFoundError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        ) from err
    return Product.model_validate(db_product)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(db: DbSession, product: ProductCreate) -> Product:
    db_product = db_create_product(db, product)
    return Product.model_validate(db_product)


@router.put("/{product_id}", status_code=status.HTTP_201_CREATED)
def update_product(db: DbSession, product_id: int, product: ProductUpdate) -> Product:
    try:
        updated_product = db_update_product(db, product_id, product)
    except ProductNotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        ) from ex

    return Product.model_validate(updated_product)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(db: DbSession, product_id: int) -> None:
    try:
        db_delete_product(db, product_id)
    except ProductNotFoundError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        ) from ex
