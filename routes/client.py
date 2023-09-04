from fastapi import APIRouter, HTTPException, Depends, status
from config.db import conn, clients_collection
from schemas.client import clientEntity
from models.client import Client
from passlib.hash import sha256_crypt
from bson import ObjectId
from starlette.status import *
from routes.jwt_auth import check_read, check_write, check_admin

#App Users
client = APIRouter(tags=["Clients"])



@client.get("/clients", dependencies=[Depends(check_read)])
async def get_all_clients():

    clients_cursor = clients_collection.find()
    
    clients = [clientEntity(client) for client in clients_cursor]
    if clients == []:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Clients not found")
    
    return clients


@client.post("/client", dependencies=[Depends(check_write)], status_code=status.HTTP_201_CREATED)
async def create_client(client: Client):

    all_clients = conn.local.clients.find()
    one_client = conn.local.clients.find_one({"name": client.name})

    if one_client in all_clients:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Client already exists")
    
    new_client = dict(client)

    id = conn.local.clients.insert_one(new_client).inserted_id
    client = conn.local.clients.find_one({"_id": id})
    return clientEntity(client)


@client.get("/client/{id}", dependencies=[Depends(check_read)])
async def find_client(id: str):

    all_clients = conn.local.clients.find()
    one_client = conn.local.clients.find_one({"_id": ObjectId(id)})

    if not one_client in all_clients:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Client not found")
    
    return clientEntity(conn.local.clients.find_one({"_id": ObjectId(id)}))


@client.put("/client/{id}", dependencies=[Depends(check_write)])
async def update_client(id: str, client: Client):

    all_clients = conn.local.clients.find()
    one_client = conn.local.clients.find_one({"_id": ObjectId(id)})

    if not one_client in all_clients:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Client not found")
    
    client_dict = dict(client)

    update_client = conn.local.clients.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(client_dict)}, return_document=True)

    return clientEntity(update_client)


@client.delete("/client/{id}", dependencies=[Depends(check_write)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(id: str):

    clientEntity(conn.local.clients.find_one_and_delete({"_id": ObjectId(id)}))