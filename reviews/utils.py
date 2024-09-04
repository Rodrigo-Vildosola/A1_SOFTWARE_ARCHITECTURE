from bson.objectid import ObjectId
from .mongo import Mongo
import os
from django.conf import settings


# MongoDB connection
db = Mongo().database
collection = db['object']


def handle_uploaded_file(f):
    upload_path = os.path.join(settings.MEDIA_ROOT, f.name)
    with open(upload_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return os.path.join(settings.MEDIA_URL, f.name)  # Return the media URL to store in MongoDB


def search_books(query, page=1, limit=10):
    skip = (page - 1) * limit
    regex_query = {"$regex": query, "$options": "i"}

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
                "id": "$books._id",
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

    search_results = collection.aggregate(pipeline)
    
    
    return list(search_results)
