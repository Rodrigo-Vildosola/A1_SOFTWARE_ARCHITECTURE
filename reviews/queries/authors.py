
from bson.objectid import ObjectId
from reviews.mongo import Mongo

# MongoDB connection
db = Mongo().database
books_collection = db['books']
authors_collection = db['authors']
reviews_collection = db['reviews']
sales_collection = db['sales']

def get_books_by_author(author_id):
    return list(books_collection.find({"author_id": ObjectId(author_id)}))
