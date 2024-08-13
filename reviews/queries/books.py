from bson.objectid import ObjectId
from reviews.mongo import Mongo
from pymongo.errors import PyMongoError


# MongoDB connection
db = Mongo().database
collection = db['object']

def get_top_rated_books():
    try:
        pipeline = [
            {"$unwind": "$books"},
            {"$unwind": "$books.reviews"},
            {
                "$group": {
                    "_id": "$books._id",
                    "book_name": {"$first": "$books.name"},
                    "author_name": {"$first": "$name"},
                    "author_id": {"$first": "$_id"},
                    "average_score": {"$avg": "$books.reviews.score"},
                    "reviews": {"$push": "$books.reviews"}
                }
            },
            {
                "$project": {
                    "book_name": 1,
                    "author_name": 1,
                    "author_id": 1,
                    "average_score": 1,
                    "reviews": 1,
                    "highest_rated_review": {
                        "$arrayElemAt": [
                            {
                                "$filter": {
                                    "input": "$reviews",
                                    "as": "review",
                                    "cond": {"$eq": ["$$review.score", {"$max": "$reviews.score"}]}
                                }
                            }, 0
                        ]
                    },
                    "lowest_rated_review": {
                        "$arrayElemAt": [
                            {
                                "$filter": {
                                    "input": "$reviews",
                                    "as": "review",
                                    "cond": {"$eq": ["$$review.score", {"$min": "$reviews.score"}]}
                                }
                            }, 0
                        ]
                    }
                }
            },
            {"$sort": {"average_score": -1}},
            {"$limit": 10},
            {
                "$project": {
                    "book_name": 1,
                    "author_name": 1,
                    "author_id": 1,
                    "average_score": 1,
                    "highest_rated_review": {
                        "_id": "$highest_rated_review._id",
                        "review": "$highest_rated_review.review",
                        "score": "$highest_rated_review.score"
                    },
                    "lowest_rated_review": {
                         "_id": "$lowest_rated_review._id",
                        "review": "$lowest_rated_review.review",
                        "score": "$lowest_rated_review.score"
                    }
                }
            }
        ]
        return list(collection.aggregate(pipeline))
    except PyMongoError as e:
        print(f"An error occurred: {e}")
        return []



def get_top_selling_books():
    pipeline = [
        {
            "$unwind": "$books"
        },
        {
            "$unwind": {
                "path": "$books.sales",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$group": {
                "_id": "$books._id",
                "title": {"$first": "$books.name"},
                "author_id": {"$first": "$_id"},
                "total_sales": {"$sum": {"$convert": {"input": "$books.sales.sales", "to": "int", "onError": 0, "onNull": 0}}},
                "publication_year": {"$first": {"$year": {"$dateFromString": {"dateString": "$books.date_of_publication"}}}}
            }
        },
        {
            "$sort": {"total_sales": -1}
        },
        {
            "$limit": 50
        },
        {
            "$lookup": {
                "from": "authors",
                "localField": "author_id",
                "foreignField": "_id",
                "as": "author_info"
            }
        },
        {
            "$unwind": "$author_info"
        },
        {
            "$group": {
                "_id": "$_id",
                "title": {"$first": "$title"},
                "author": {"$first": "$author_info.name"},
                "author_id": {"$first": "$author_info._id"},
                "total_sales": {"$first": "$total_sales"},
                "publication_year": {"$first": "$publication_year"},
                "is_top_5_publication_year": {
                    "$first": {
                        "$cond": {
                            "if": {"$lte": ["$publication_year", 5]},
                            "then": "Yes",
                            "else": "No"
                        }
                    }
                }
            }
        },
        {
            "$project": {
                "title": 1,
                "author": 1,
                "author_id": 1,
                "total_sales": 1,
                "is_top_5_publication_year": 1
            }
        }
    ]

    return list(collection.aggregate(pipeline))


def get_books_aggregate(page, name_filter=''):
    pipeline = [
        {
            "$unwind": "$books"
        },
        {
            '$unwind': {
                'path': '$books.sales',
                'preserveNullAndEmptyArrays': True
            }
        },
        {
            "$match": {
                "books.name": { "$regex": name_filter, "$options": "i" }
            }
        },
        {
            "$group": {
                "_id": "$books._id",
                "name": { "$first": "$books.name" },
                "summary": { "$first": "$books.summary" },
                "date_of_publication": { "$first": "$books.date_of_publication" },
                "author_id": { "$first": "$_id" },
                "number_of_sales": { '$sum': { '$toInt': '$books.sales.sales' } }
            }
        },
        {
            "$sort": { "name": 1 }  # Default sorting by name
        },
        {
            "$skip": (page - 1) * 20
        },
        {
            "$limit": 20
        }
    ]
    return list(collection.aggregate(pipeline))



def get_book_by_id(pk):
    pipeline = [
        {
            "$unwind": "$books"
        },
        {
            "$match": { "books._id": ObjectId(pk) }
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
        }
    ]
    book = list(collection.aggregate(pipeline))
    return book[0] if book else None


def get_reviews_by_book(pk):
    pipeline = [
        {
            "$unwind": "$books"
        },
        {
            "$match": { "books._id": ObjectId(pk) }
        },
        {
            "$unwind": "$books.reviews"
        },
        {
            "$project": {
                "_id": "$books.reviews._id",
                "review": "$books.reviews.review",
                "score": "$books.reviews.score",
                "number_of_upvotes": "$books.reviews.number_of_upvotes",
                "book_id": "$books._id"
            }
        }
    ]
    return list(collection.aggregate(pipeline))

def get_sales_by_book(pk):
    pipeline = [
        {
            "$unwind": "$books"
        },
        {
            "$match": { "books._id": ObjectId(pk) }
        },
        {
            "$unwind": "$books.sales"
        },
        {
            "$project": {
                "_id": "$books.sales._id",
                "year": "$books.sales.year",
                "sales": "$books.sales.sales",
                "book_id": "$books._id"
            }
        }
    ]
    return list(collection.aggregate(pipeline))

def create_book(author_id, book_data):
    book_data["_id"] = ObjectId()
    return collection.update_one(
        {'_id': ObjectId(author_id)},
        {'$push': {'books': book_data}}
    )

def update_book(pk, data):
    return collection.update_one(
        {'books._id': ObjectId(pk)},
        {'$set': {f'books.$.{key}': value for key, value in data.items()}}
    )

def delete_book(pk):
    return collection.update_one(
        {'books._id': ObjectId(pk)},
        {'$pull': {'books': {'_id': ObjectId(pk)}}}
    )
