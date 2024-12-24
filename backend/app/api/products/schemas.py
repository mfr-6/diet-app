from pydantic import BaseModel

class ProductIn(BaseModel):
    name: str