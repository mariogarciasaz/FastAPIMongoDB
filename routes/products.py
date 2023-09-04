from fastapi import APIRouter, HTTPException, Depends, status
from config.db import conn, products_collection
from schemas.product import productEntity
from models.product import Product
from passlib.hash import sha256_crypt
from bson import ObjectId
from starlette.status import *
from routes.jwt_auth import check_read, check_write, check_admin, current_user


product = APIRouter(tags=["Products"])



@product.get("/products", dependencies=[Depends(check_read)])
async def get_all_products():


    products_cursor = products_collection.find()
    
    products = [productEntity(product) for product in products_cursor]

    if products == []:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Products not found")


    return products

@product.post("/product", dependencies=[Depends(check_write)], status_code=status.HTTP_201_CREATED)
async def create_product(product: Product):

    all_products = conn.local.product.find()
    one_product = conn.local.product.find_one({"name": product.name})
    if one_product in all_products:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Product already exists")

    new_product = dict(product)

    id = conn.local.product.insert_one(new_product).inserted_id
    product = conn.local.product.find_one({"_id": id})
    return productEntity(product)


@product.get("/product/{id}", dependencies=[Depends(check_read)])
async def find_product(id: str):

    all_products = conn.local.product.find()
    one_product = conn.local.product.find_one({"_id": ObjectId(id)})
    if not one_product in all_products:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Product not found")
    
    return productEntity(conn.local.product.find_one({"_id": ObjectId(id)}))

@product.put("/product/{id}", dependencies=[Depends(check_write) or Depends(check_admin)])
async def update_product(id: str, product: Product):

    all_products = conn.local.product.find()
    one_product = conn.local.product.find_one({"_id": ObjectId(id)})
    if not one_product in all_products:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Product not found")

    product_dict = dict(product)
    


    update_product = conn.local.product.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(product_dict)}, return_document=True)
    return productEntity(update_product)



@product.delete("/product/{id}", dependencies=[Depends(check_write)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: str):

    productEntity(conn.local.product.find_one_and_delete({"_id": ObjectId(id)}))