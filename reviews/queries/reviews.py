from bson.objectid import ObjectId
from pymongo.errors import PyMongoError
from reviews.utils import collection, generate_cache_key, cache_set, cache_get
from reviews.redis import redis_client  


def get_all_reviews(page=1, name_filter=''):
    cache_key = generate_cache_key("reviews", page, name_filter)
    cached_data = cache_get(cache_key)
    if cached_data:
        print(f'----------------- Returning cached data: reviews page {page} -----------------')
        return cached_data
    
    try:
        pipeline = [
            {"$unwind": "$books"},
            {"$unwind": "$books.reviews"},
            {
                "$match": {
                    "$or": [
                        {"books.name": {"$regex": name_filter, "$options": "i"}},
                        {"books.reviews.review": {"$regex": name_filter, "$options": "i"}}
                    ]
                }
            },
            {
                "$project": {
                    "_id": "$books.reviews._id",
                    "author_name": "$name",
                    "book_id": "$books._id",
                    "book_name": "$books.name",
                    "review": "$books.reviews.review",
                    "score": "$books.reviews.score",
                    "number_of_upvotes": "$books.reviews.number_of_upvotes"
                }
            },
            {"$sort": {"book_name": 1}}, 
            {"$skip": (page - 1) * 20},   
            {"$limit": 20}
        ]

        total_reviews_pipeline = [
            {"$unwind": "$books"},
            {"$unwind": "$books.reviews"},
            {
                "$match": {
                    "$or": [
                        {"books.name": {"$regex": name_filter, "$options": "i"}},
                        {"books.reviews.review": {"$regex": name_filter, "$options": "i"}}
                    ]
                }
            },
            {"$count": "total"}
        ]

        reviews = list(collection.aggregate(pipeline))
        
        total_reviews_count = next(collection.aggregate(total_reviews_pipeline), {}).get('total', 0)
        cache_set(cache_key, (reviews, total_reviews_count))
        return reviews, total_reviews_count
    except PyMongoError as e:
        print(f"An error occurred: {e}")
        return [], 0
  

def get_review_by_id(review_id):
    cache_key = generate_cache_key("reviews", review_id)
    cached_data = cache_get(cache_key)
    if cached_data:
        print(f'----------------- Returning cached data: review {review_id} -----------------')
        return cached_data
    
    try:
        review_id = ObjectId(review_id)
        pipeline = [
            {"$unwind": "$books"},
            {"$unwind": "$books.reviews"},
            {"$match": {"books.reviews._id": review_id}},
            {
                "$project": {
                    "author_name": "$name",
                    "book_name": "$books.name",
                    "book_id": "$books._id",
                    "review": "$books.reviews.review",
                    "score": "$books.reviews.score",
                    "number_of_upvotes": "$books.reviews.number_of_upvotes"
                }
            }
        ]
        result = list(collection.aggregate(pipeline))
        cache_set(cache_key, result[0] if result else "Review not found")
        return result[0] if result else "Review not found"
    except PyMongoError as e:
        print(f"An error occurred: {e}")
        return "An error occurred"

def create_review(book_id, review):
    try:
        review["_id"] = ObjectId()
        collection.update_one(
            {'books._id': ObjectId(book_id)},
            {'$push': {'books.$.reviews': review}}
        )
        return review
    except PyMongoError as e:
        print(f"An error occurred: {e}")
        return "An error occurred"

def update_review(review_id, updated_review):
    try:
        collection.update_one(
            {'books.reviews._id': ObjectId(review_id)},
            {'$set': {
                "books.$[book].reviews.$[review].review": updated_review["review"],
                "books.$[book].reviews.$[review].score": updated_review["score"],
                "books.$[book].reviews.$[review].number_of_upvotes": updated_review["number_of_upvotes"]
            }},
            array_filters=[
                {"book.reviews._id": ObjectId(review_id)},
                {"review._id": ObjectId(review_id)}
            ]
        )
    except PyMongoError as e:
        print(f"An error occurred: {e}")
        return "An error occurred"

def delete_review(review_id):
    try:
        collection.update_one(
            {'books.reviews._id': ObjectId(review_id)},
            {'$pull': {'books.$[book].reviews': {'_id': ObjectId(review_id)}}},
            array_filters=[
                {"book.reviews._id": ObjectId(review_id)}
            ]
        )
    except PyMongoError as e:
        print(f"An error occurred: {e}")
        return "An error occurred"
