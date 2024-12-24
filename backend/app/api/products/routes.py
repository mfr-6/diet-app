from fastapi import APIRouter, status
from playhouse.shortcuts import model_to_dict
from app.api.core.db import DbSession
from .models import Product
from .schemas import ProductIn

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/")
def read_products(db: DbSession):
    products = Product.select()
    return [ model_to_dict(product) for product in products ]
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
def read_product(product_id: int):#, db: DbSession) -> dict:
    product = Product.select().where(Product.id == product_id).get()
    return model_to_dict(product)
    # return {
    #     "id": product_id,
    #     "name": "apple",
    #     "price": 1.0
    # }

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(product_req: ProductIn, db: DbSession) -> dict:
    with db.atomic():
        product = Product.create(
            name=product_req.name
        )
        product.save()
    return model_to_dict(product)#{"id": product.id, "name": product.name}

@router.delete("/{product_id}")
def delete_product(product_id: int, db: DbSession) -> dict:
    query = Product.delete().where(Product.id == product_id)
    query.execute()
    return {}

#TODO: Migrate to SQLAlchemy