



import pymongo
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Adjust the URI if needed

# Select the database and collection
db = client['fruits']  # Replace 'fruits' with your actual database name
collection = db['fruitss']  # Replace 'fruits' with your actual collection name

# Function to fetch all fruit data
def get_fruits():
    return list(collection.find())