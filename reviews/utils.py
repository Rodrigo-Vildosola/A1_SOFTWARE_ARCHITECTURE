from bson.objectid import ObjectId
from .mongo import Mongo
from .redis import redis_client
import os
from django.conf import settings
import json
import hashlib


# MongoDB connection
db = Mongo().database
collection = db['object']

CACHE_EXPIRATION = 600

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def generate_cache_key(base_name, *args, **kwargs):
    """
    Generate a unique cache key using a base name, positional arguments, and keyword arguments.

    :param base_name: A string that represents the base of the cache key (e.g., the function name or category).
    :param args: Positional arguments that will be included in the cache key.
    :param kwargs: Keyword arguments that will be included in the cache key.
    :return: A unique cache key as a string.
    """
    # Ensure that kwargs are sorted by key to avoid different keys for the same logical data
    kwargs_sorted = json.dumps(kwargs, sort_keys=True)

    # Concatenate base name, positional arguments, and keyword arguments into a single string
    key_string = f"{base_name}:{str(args)}:{kwargs_sorted}"

    # Use hashlib to generate an MD5 hash of the resulting key string
    return hashlib.md5(key_string.encode()).hexdigest()


def cache_set(key, data, expiration=CACHE_EXPIRATION):
    """Helper function to set cache with a serialized value."""
    redis_client.setex(key, expiration, json.dumps(data, cls=JSONEncoder))


def cache_get(key):
    """Helper function to get cache and deserialize value."""
    cached_data = redis_client.get(key)
    if cached_data:
        return json.loads(cached_data)
    return None

def handle_uploaded_file(f):
    # Ensure the media directory exists
    media_dir = settings.MEDIA_ROOT
    if not os.path.exists(media_dir):
        os.makedirs(media_dir)

    # Save the uploaded file
    upload_path = os.path.join(media_dir, f.name)
    print(upload_path)
    with open(upload_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    print("Uploaded image: ", os.path.join(settings.MEDIA_URL, f.name))
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
