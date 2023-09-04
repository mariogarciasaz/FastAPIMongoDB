from pymongo import MongoClient

# conn = MongoClient("mongodb://localhost:27017/")
conn = MongoClient("mongodb+srv://mariogarciasaz:Drogofunko1@cluster0.iiwnqgw.mongodb.net/?retryWrites=true&w=majority").test
db = conn["local"]

users_collection = db["user"]
products_collection = db["product"]
clients_collection = db["clients"]
