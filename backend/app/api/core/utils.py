from app.api.core.db import db
from app.api.products.models import Product

def create_tables() -> None:
    with db:
        db.create_tables([Product])