from reviews.mongo import Mongo
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError

# Initialize database and collection
db = Mongo().database
collection = db['object']

def get_all_reviews():
    try:
        pipeline = [
            {"$unwind": "$books"},
            {"$unwind": "$books.reviews"},
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
            }
        ]
        return list(collection.aggregate(pipeline))
    except PyMongoError as e:
        print(f"An error occurred: {e}")
        return []

def get_review_by_id(review_id):
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
