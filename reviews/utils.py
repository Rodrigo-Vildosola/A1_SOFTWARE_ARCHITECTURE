from bson.objectid import ObjectId
from .mongo import Mongo

# MongoDB connection
db = Mongo().database
authors_collection = db['object']

def search_books(query, page=1, limit=10):
    skip = (page - 1) * limit
    regex_query = {"$regex": query, "$options": "i"}  # Case-insensitive regex

    pipeline = [
        {
            "$unwind": "$books"
        },
        {
            "$match": {
                "$or": [
                    {"books.name": regex_query},
                    {"books.summary": regex_query}
                ]
            }
        },
        {
            "$project": {
                "_id": "$books._id",
                "name": "$books.name",
                "summary": "$books.summary",
                "date_of_publication": "$books.date_of_publication",
                "author_id": "$_id",
                "author_name": "$name"
            }
        },
        {
            "$skip": skip
        },
        {
            "$limit": limit
        }
    ]

    search_results = authors_collection.aggregate(pipeline)
    
    
    return list(search_results)
