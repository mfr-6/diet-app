from fastapi import FastAPI
from app.api.main import api_router


app = FastAPI(
    title="Diet API",
    description="API for diet management",
    version="0.1.0"
)

app.include_router(api_router, prefix="/api/v1")