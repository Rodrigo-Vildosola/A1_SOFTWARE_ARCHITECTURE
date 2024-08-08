from bson.objectid import ObjectId
from reviews.mongo import Mongo

db = Mongo().database
reviews_collection = db['reviews']
books_collection = db['books']

def get_all_reviews():
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
                "review": 1,
                "score": 1,
                "number_of_upvotes": 1,
                "book_name": "$book_info.name"
            }
        }
    ]
    return list(reviews_collection.aggregate(pipeline))

def get_review_by_id(review_id):
    pipeline = [
        {
            "$match": { "_id": ObjectId(review_id) }
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
                "review": 1,
                "score": 1,
                "number_of_upvotes": 1,
                "book_name": "$book_info.name"
            }
        }
    ]
    return reviews_collection.aggregate(pipeline).next()
