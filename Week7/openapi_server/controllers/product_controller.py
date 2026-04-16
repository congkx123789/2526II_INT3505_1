import connexion
from typing import Dict, List, Tuple, Union
from bson import ObjectId

from openapi_server.models.product import Product  # noqa: E501
from openapi_server.models.product_input import ProductInput  # noqa: E501
from openapi_server import util
from openapi_server.database import get_db

db = get_db()
products_col = db["products"]

def serialize_product(doc):
    """Helper to convert MongoDB document to Product model."""
    doc['id'] = str(doc.pop('_id'))
    return Product.from_dict(doc)

def add_product(body):  # noqa: E501
    """Create a new product"""
    if connexion.request.is_json:
        data = connexion.request.get_json()
        product_input = ProductInput.from_dict(data)
        
        # Insert into MongoDB
        result = products_col.insert_one(data)
        data['_id'] = result.inserted_id
        
        return serialize_product(data), 201
    return 'Invalid data', 400


def delete_product(id_):  # noqa: E501
    """Delete a product"""
    try:
        result = products_col.delete_one({'_id': ObjectId(id_)})
        if result.deleted_count == 0:
            return 'Product not found', 404
        return None, 204
    except Exception:
        return 'Invalid ID format', 400


def get_product_by_id(id_):  # noqa: E501
    """Get a product by ID"""
    try:
        doc = products_col.find_one({'_id': ObjectId(id_)})
        if not doc:
            return 'Product not found', 404
        return serialize_product(doc), 200
    except Exception:
        return 'Invalid ID format', 400


def get_products():  # noqa: E501
    """Get all products"""
    cursor = products_col.find({})
    products = [serialize_product(doc) for doc in cursor]
    return products, 200


def update_product(id_, body):  # noqa: E501
    """Update a product"""
    if connexion.request.is_json:
        try:
            data = connexion.request.get_json()
            # Ensure we don't try to update the ID
            if 'id' in data:
                del data['id']
                
            result = products_col.update_one(
                {'_id': ObjectId(id_)},
                {'$set': data}
            )
            
            if result.matched_count == 0:
                return 'Product not found', 404
                
            doc = products_col.find_one({'_id': ObjectId(id_)})
            return serialize_product(doc), 200
        except Exception:
            return 'Invalid ID format or data', 400
    return 'Invalid data', 400
