
from bson.objectid import ObjectId
from reviews.mongo import Mongo

# MongoDB connection
db = Mongo().database
authors_collection = db.object

def get_books_by_author(author_id):
    author = authors_collection.find_one({"_id": ObjectId(author_id)}, {"books": 1})
    return author.get("books", []) if author else []



def get_author_with_books_reviews_sales():
    pipeline = [
        {
            "$addFields": {
                "number_of_books": { "$size": "$books" },
                "total_sales": {
                    "$sum": {
                        "$map": {
                            "input": "$books",
                            "as": "book",
                            "in": {
                                "$sum": {
                                    "$map": {
                                        "input": "$$book.sales",
                                        "as": "sale",
                                        "in": { "$toInt": "$$sale.sales" }
                                    }
                                }
                            }
                        }
                    }
                },
                "average_score": {
                    "$avg": {
                        "$map": {
                            "input": "$books",
                            "as": "book",
                            "in": {
                                "$avg": {
                                    "$map": {
                                        "input": "$$book.reviews",
                                        "as": "review",
                                        "in": { "$toDouble": "$$review.score" }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        {
            "$sort": { "name": 1 }  # Sort by author name
        }
    ]

    # Execute the aggregation pipeline
    return list(authors_collection.aggregate(pipeline))
