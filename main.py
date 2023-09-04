from fastapi import FastAPI
from routes.user import user
from routes.products import product
from routes.client import client
from routes.jwt_auth import auth

from fastapi.responses import FileResponse
import os



#Global APP
app = FastAPI()

@app.get("/")
async def root():
    return "Hello, I'm FastAPI"

#Routes
app.include_router(user)
app.include_router(product)
app.include_router(client)
app.include_router(auth)

