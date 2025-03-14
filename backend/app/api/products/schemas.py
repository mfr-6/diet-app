from pydantic import BaseModel, ConfigDict

# https://docs.pydantic.dev/latest/concepts/models/#arbitrary-class-instances


class Product(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class ProductCreate(BaseModel):
    name: str


class ProductUpdate(BaseModel):
    name: str
