
from bson.objectid import ObjectId
from reviews.utils import collection


def get_books_by_author(author_id):
    author = collection.find_one({"_id": ObjectId(author_id)}, {"books": 1})
    return author.get("books", []) if author else []



def get_author_with_books_reviews_sales(page, sort_by, order, name_filter):
    sort_fields = {
        'name': 'name',
        'number_of_books': 'number_of_books',
        'average_score': 'average_score',
        'total_sales': 'total_sales'
    }
    
    sort_field = sort_fields.get(sort_by, 'name')

    pipeline = [
        {
            "$addFields": {
                # Ensure books is an array or an empty array if missing
                "books": { "$ifNull": ["$books", []] },
                
                # Calculate the number of books
                "number_of_books": { "$size": { "$ifNull": ["$books", []] } },
                
                # Calculate the total sales (ensure books.sales is handled properly)
                "total_sales": {
                    "$sum": {
                        "$map": {
                            "input": { "$ifNull": ["$books", []] },
                            "as": "book",
                            "in": {
                                "$sum": {
                                    "$map": {
                                        "input": { "$ifNull": ["$$book.sales", []] },
                                        "as": "sale",
                                        "in": { "$toInt": { "$ifNull": ["$$sale.sales", 0] } }
                                    }
                                }
                            }
                        }
                    }
                },
                
                # Calculate the average review score
                "average_score": {
                    "$avg": {
                        "$map": {
                            "input": { "$ifNull": ["$books", []] },
                            "as": "book",
                            "in": {
                                "$avg": {
                                    "$map": {
                                        "input": { "$ifNull": ["$$book.reviews", []] },
                                        "as": "review",
                                        "in": { "$toDouble": { "$ifNull": ["$$review.score", 0] } }
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
            "$sort": { sort_field: 1 if order == 'asc' else -1 }
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

    total_count_result = list(collection.aggregate(total_pipeline))
    total_count = total_count_result[0]['total'] if total_count_result else 0
    num_pages = (total_count + 9) // 10

    return list(collection.aggregate(pipeline)), num_pages
