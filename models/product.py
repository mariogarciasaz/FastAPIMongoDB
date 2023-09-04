from pydantic import BaseModel
from typing import Optional


class Product(BaseModel):
    name: str
    category: str
    price: float
    stock: float
