from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    username: str
    name: str
    email: str
    disabled: bool
    role: str


class UserDB(User):
    password: str
