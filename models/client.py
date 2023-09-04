from pydantic import BaseModel
from typing import Optional


class Client(BaseModel):
    name: str
    lastname: str
    address: str
    phone: str
    email: str
    
