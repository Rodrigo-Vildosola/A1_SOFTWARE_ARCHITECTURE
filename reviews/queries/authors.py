
from bson.objectid import ObjectId
from reviews.utils import collection, generate_cache_key, cache_set, cache_get
from reviews.redis import redis_client  


def get_books_by_author(author_id):
    author = collection.find_one({"_id": ObjectId(author_id)}, {"books": 1})
    return author.get("books", []) if author else []


def get_author_by_id(pk, include_books=False):
    try:
        match_stage = {"$match": {"_id": ObjectId(pk)}}
        project_stage = {
            "$project": {
                "_id": 1,
                "name": 1,
                "date_of_birth": 1,
                "country_of_origin": 1,
                "short_description": 1,
                "image_url": 1,
                "books": {"$cond": {"if": include_books, "then": "$books", "else": "$$REMOVE"}}
            }
        }

        pipeline = [match_stage, project_stage]

        author = collection.aggregate(pipeline).next()
        if not author:
            return None
        
        return author
    except StopIteration:
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_author_with_books_reviews_sales(page, sort_by, order, name_filter):
    cache_key = generate_cache_key("author_with_books", page, sort_by, order, name_filter)
    cached_data = cache_get(cache_key)
    if cached_data:
        print("CACHE HIT")
        return cached_data
    
    print("CACHE MISS")

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
                "books": { "$ifNull": ["$books", []] },
                "number_of_books": { "$size": { "$ifNull": ["$books", []] } },
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

    result = (list(collection.aggregate(pipeline)), num_pages)

    # Cache the result
    cache_set(cache_key, result)

    return result




def create_author(author_data):
    """Create an author and invalidate cache related to author listings."""
    try:
        collection.insert_one(author_data)
        redis_client.flushdb()  # Invalidate all cache related to author listings
        return True
    except Exception as e:
        print(f"An error occurred while creating the author: {e}")
        return False


def update_author(pk, updated_author):
    """Update an author by ID and invalidate relevant cache."""
    try:
        collection.update_one({'_id': ObjectId(pk)}, {'$set': updated_author})
        redis_client.flushdb()  # Invalidate all cache related to author listings
        return True
    except Exception as e:
        print(f"An error occurred while updating the author: {e}")
        return False


def delete_author(pk):
    """Delete an author by ID and invalidate relevant cache."""
    try:
        collection.delete_one({'_id': ObjectId(pk)})
        redis_client.flushdb()  # Invalidate all cache related to author listings
        return True
    except Exception as e:
        print(f"An error occurred while deleting the author: {e}")
        return False
