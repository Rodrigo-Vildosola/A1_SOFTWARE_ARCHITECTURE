from reviews.mongo import Mongo
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError

# Initialize database and collection
db = Mongo().database
collection = db['object']

def get_all_sales():
    try:
        pipeline = [
            {"$unwind": "$books"},
            {"$unwind": "$books.sales"},
            {
                "$project": {
                    "_id": "$books.sales._id",
                    "author_name": "$name",
                    "book_id": "$books._id",
                    "book_name": "$books.name",
                    "year": "$books.sales.year",
                    "sales": "$books.sales.sales"
                }
            }
        ]
        return list(collection.aggregate(pipeline))
    except PyMongoError as e:
        print(f"An error occurred: {e}")
        return []

def get_sale_by_id(sale_id):
    try:
        sale_id = ObjectId(sale_id)
        pipeline = [
            {"$unwind": "$books"},
            {"$unwind": "$books.sales"},
            {"$match": {"books.sales._id": sale_id}},
            {
                "$project": {
                    "author_name": "$name",
                    "book_name": "$books.name",
                    "book_id": "$books._id",
                    "year": "$books.sales.year",
                    "sales": "$books.sales.sales"
                }
            }
        ]
        result = list(collection.aggregate(pipeline))
        return result[0] if result else "Sale not found"
    except PyMongoError as e:
        print(f"An error occurred: {e}")
        return "An error occurred"

def create_sale(book_id, sale):
    try:
        sale["_id"] = ObjectId()
        collection.update_one(
            {'books._id': ObjectId(book_id)},
            {'$push': {'books.$.sales': sale}}
        )
        return sale
    except PyMongoError as e:
        print(f"An error occurred: {e}")
        return "An error occurred"

def update_sale(sale_id, updated_sale):
    try:
        collection.update_one(
            {'books.sales._id': ObjectId(sale_id)},
            {'$set': {
                "books.$[book].sales.$[sale].year": updated_sale["year"],
                "books.$[book].sales.$[sale].sales": updated_sale["sales"]
            }},
            array_filters=[
                {"book.sales._id": ObjectId(sale_id)},
                {"sale._id": ObjectId(sale_id)}
            ]
        )
    except PyMongoError as e:
        print(f"An error occurred: {e}")
        return "An error occurred"

def delete_sale(sale_id):
    try:
        collection.update_one(
            {'books.sales._id': ObjectId(sale_id)},
            {'$pull': {'books.$[book].sales': {'_id': ObjectId(sale_id)}}},
            array_filters=[
                {"book.sales._id": ObjectId(sale_id)}
            ]
        )
    except PyMongoError as e:
        print(f"An error occurred: {e}")
        return "An error occurred"
