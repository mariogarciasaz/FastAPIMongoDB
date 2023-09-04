from fastapi import APIRouter, HTTPException, Depends, status
from config.db import conn, users_collection
from schemas.user import userEntity
from models.user import User, UserDB
from passlib.hash import sha256_crypt
from bson import ObjectId
from starlette.status import *
from routes.jwt_auth import check_admin


#App Users
user = APIRouter(tags=["Users"])


@user.get("/users", dependencies=[Depends(check_admin)])
async def get_all_users():

    users_cursor = users_collection.find()
    
    users = [userEntity(user) for user in users_cursor]

    if users == []:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Users not found")


    return users

@user.post("/user", dependencies=[Depends(check_admin)], status_code=status.HTTP_201_CREATED)
async def create_user(user: UserDB):
    
    
    all_users = conn.local.user.find()
    one_user = conn.local.user.find_one({"name": user.name})

    if one_user in all_users:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="User already exists")

    new_user = dict(user)
    new_user["password"] = sha256_crypt.encrypt(new_user["password"])
    id = conn.local.user.insert_one(new_user).inserted_id
    user = conn.local.user.find_one({"_id": id})
    return userEntity(user)


@user.get("/user/{id}", dependencies=[Depends(check_admin)])
async def find_user(id: str):

    all_users = conn.local.user.find()
    one_user = conn.local.user.find_one({"_id": ObjectId(id)})
    if not one_user in all_users:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    
    return userEntity(conn.local.user.find_one({"_id": ObjectId(id)}))

@user.put("/user/{id}", dependencies=[Depends(check_admin)])
async def update_user(id: str, user: User):

    all_users = conn.local.user.find()
    one_user = conn.local.user.find_one({"_id": ObjectId(id)})
    if not one_user in all_users:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

    user_dict = dict(user)
    user_dict["password"] = sha256_crypt.encrypt(user_dict["password"])


    update_user = conn.local.user.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user_dict)}, return_document=True)
    return userEntity(update_user)



@user.delete("/user/{id}", dependencies=[Depends(check_admin)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    
    userEntity(conn.local.user.find_one_and_delete({"_id": ObjectId(id)}))