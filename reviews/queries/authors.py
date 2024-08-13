
from bson.objectid import ObjectId
from reviews.mongo import Mongo

# MongoDB connection
db = Mongo().database
authors_collection = db.object

def get_books_by_author(author_id):
    author = authors_collection.find_one({"_id": ObjectId(author_id)}, {"books": 1})
    return author.get("books", []) if author else []



def get_author_with_books_reviews_sales(page, sort_by, order, name_filter):
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
            "$project": {
                "name": 1,
                "number_of_books": 1,
                "total_sales": 1,
                "average_score": 1
            }
        },
        {
            "$match": {
                "name": { "$regex": name_filter, "$options": "i" }
            }
        },
        {
            "$sort": { sort_by: 1 if order == 'asc' else -1 }
        },
        {
            "$skip": (page - 1) * 10
        },
        {
            "$limit": 10
        }
    ]

    total_pipeline = [
        {
            "$match": {
                "name": { "$regex": name_filter, "$options": "i" }
            }
        },
        {
            "$count": "total"
        }
    ]

    total_count_result = list(authors_collection.aggregate(total_pipeline))
    total_count = total_count_result[0]['total'] if total_count_result else 0
    num_pages = (total_count + 9) // 10  # Calculate number of pages

    return list(authors_collection.aggregate(pipeline)), num_pages
