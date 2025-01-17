



# fruits/mongodb.py
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DATABASE_NAME = "tshirts_ecom"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

