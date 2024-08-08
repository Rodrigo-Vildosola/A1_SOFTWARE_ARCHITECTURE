from bson.objectid import ObjectId
from reviews.mongo import Mongo

db = Mongo().database
sales_collection = db['sales']
books_collection = db['books']

def get_all_sales():
    pipeline = [
        {
            "$lookup": {
                "from": "books",
                "localField": "book_id",
                "foreignField": "_id",
                "as": "book_info"
            }
        },
        {
            "$unwind": "$book_info"
        },
        {
            "$project": {
                "_id": 1,
                "book_id": 1,
                "year": 1,
                "sales": 1,
                "book_name": "$book_info.name"
            }
        }
    ]
    return list(sales_collection.aggregate(pipeline))

def get_sale_by_id(sale_id):
    pipeline = [
        {
            "$match": { "_id": ObjectId(sale_id) }
        },
        {
            "$lookup": {
                "from": "books",
                "localField": "book_id",
                "foreignField": "_id",
                "as": "book_info"
            }
        },
        {
            "$unwind": "$book_info"
        },
        {
            "$project": {
                "_id": 1,
                "book_id": 1,
                "year": 1,
                "sales": 1,
                "book_name": "$book_info.name"
            }
        }
    ]
    return sales_collection.aggregate(pipeline).next()
