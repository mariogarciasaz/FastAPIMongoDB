from pymongo import MongoClient

conn = MongoClient("mongodb://localhost:27017/")
db = conn["local"]

users_collection = db["user"]
products_collection = db["product"]
clients_collection = db["clients"]
