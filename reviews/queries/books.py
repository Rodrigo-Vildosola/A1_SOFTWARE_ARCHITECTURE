from bson.objectid import ObjectId
from reviews.mongo import Mongo

# MongoDB connection
db = Mongo().database
authors_collection = db['object']

def get_top_rated_books():
    pipeline = [
        {
            "$unwind": "$books"
        },
        {
            "$unwind": "$books.reviews"
        },
        {
            "$group": {
                "_id": "$books._id",
                "title": { "$first": "$books.name" },
                "author_id": { "$first": "$_id" },
                "average_rating": { "$avg": { "$toDouble": "$books.reviews.score" } },
                "reviews": { "$push": "$books.reviews" }
            }
        },
        {
            "$sort": { "average_rating": -1 }
        },
        {
            "$limit": 10
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
            "$project": {
                "title": 1,
                "author": "$author_info.name",
                "author_id": "$author_info._id",
                "average_rating": 1,
                "most_popular_review": {
                    "$arrayElemAt": [
                        { "$sortArray": { "input": "$reviews", "sortBy": { "number_of_upvotes": -1 } } },
                        0
                    ]
                },
                "highest_rated_review": {
                    "$arrayElemAt": [
                        { "$sortArray": { "input": "$reviews", "sortBy": { "score": -1 } } },
                        0
                    ]
                },
                "lowest_rated_review": {
                    "$arrayElemAt": [
                        { "$sortArray": { "input": "$reviews", "sortBy": { "score": 1 } } },
                        0
                    ]
                }
            }
        }
    ]

    return list(authors_collection.aggregate(pipeline))


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

    return list(authors_collection.aggregate(pipeline))


def get_books_aggregate():
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
            "$group": {
                "_id": "$books._id",
                "name": { "$first": "$books.name" },
                "summary": { "$first": "$books.summary" },
                "date_of_publication": { "$first": "$books.date_of_publication" },
                "author_id": { "$first": "$_id" },
                "number_of_sales": { '$sum': { '$toInt': '$books.sales.sales' } }
            }
        }
    ]
    return list(authors_collection.aggregate(pipeline))


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
    book = list(authors_collection.aggregate(pipeline))
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
    return list(authors_collection.aggregate(pipeline))

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
    return list(authors_collection.aggregate(pipeline))

def create_book(author_id, book_data):
    book_data["_id"] = ObjectId()
    return authors_collection.update_one(
        {'_id': ObjectId(author_id)},
        {'$push': {'books': book_data}}
    )

def update_book(pk, data):
    return authors_collection.update_one(
        {'books._id': ObjectId(pk)},
        {'$set': {f'books.$.{key}': value for key, value in data.items()}}
    )

def delete_book(pk):
    return authors_collection.update_one(
        {'books._id': ObjectId(pk)},
        {'$pull': {'books': {'_id': ObjectId(pk)}}}
    )
