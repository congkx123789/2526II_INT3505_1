import os
from pymongo import MongoClient

def get_db():
    """
    Returns a MongoDB database instance.
    The connection string is read from the MONGO_URI environment variable.
    """
    mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(mongo_uri)
    # Use 'product_db' as the database name
    db = client["product_db"]
    return db
