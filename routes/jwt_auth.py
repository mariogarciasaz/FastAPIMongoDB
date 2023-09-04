from functools import wraps
from typing import Callable
from fastapi import APIRouter, Depends, HTTPException, status, Form
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.hash import sha256_crypt
from datetime import datetime, timedelta
from models.user import User, UserDB
from config.db import conn, users_collection


ALGORYTHM = "HS256"
ACCESS_TOKEN_DURATION = 10
SECRET = "201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc58ea230b"

auth = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = sha256_crypt



def search_user_db(username: str):
    users_db = conn.local.user.find({"username": username})
    
    # Convertir el Cursor en una lista de resultados
    users_list = list(users_db)
    
    # Buscar el usuario en la lista de resultados
    for user_data in users_list:
        if user_data["username"] == username:
            return UserDB(**user_data)


def search_user(username: str):
    users_db = conn.local.user.find({"username": username})
    if username in users_db:
        return User(**users_db[username])
    



async def auth_user(token: str = Depends(oauth2)):
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORYTHM]).get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials", headers={"WWW-Authenticate": "Bearer"})
        
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials", headers={"WWW-Authenticate": "Bearer"})
    return search_user_db(username)



async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return {
            "username": user.username,
            "name": user.name,
            "email": user.email,
            "disabled": user.disabled,
            "role": user.role
}


@auth.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    users_db = conn.local.user.find({"username": form.username})

    if not users_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user")
    
    user = search_user_db(form.username)



    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password")
    

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)

    access_token = {"sub": user.username, "exp": expire}


    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORYTHM), "token_type": "bearer"}



@auth.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user


#Roles
async def check_admin(user: User = Depends(current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permissions")
    

async def check_write(user: User = Depends(current_user)):
    if user["role"] != "write" and user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permissions")
    

async def check_read(user: User = Depends(current_user)):
    if user["role"] != "read" and user["role"] != "admin" and user["role"] != "write":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permissions")