from fastapi import APIRouter

from app.api.products import routes as products_routes

api_router = APIRouter()
api_router.include_router(products_routes.router)
