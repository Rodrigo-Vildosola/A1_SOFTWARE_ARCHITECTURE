from bson.objectid import ObjectId
from reviews.mongo import Mongo

# MongoDB connection
db = Mongo().database
books_collection = db['books']
authors_collection = db['authors']
reviews_collection = db['reviews']
sales_collection = db['sales']

def get_top_rated_books():
    pipeline = [
        {
            "$lookup": {
                "from": "reviews",
                "localField": "_id",
                "foreignField": "book_id",
                "as": "book_reviews"
            }
        },
        {
            "$unwind": "$book_reviews"
        },
        {
            "$group": {
                "_id": "$_id",
                "title": { "$first": "$name" },
                "author_id": { "$first": "$author_id" },
                "average_rating": { "$avg": { "$toDouble": "$book_reviews.score" } },
                "reviews": { "$push": "$book_reviews" }
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

    return list(books_collection.aggregate(pipeline))

def get_top_selling_books():
    pipeline = [
        {
            "$lookup": {
                "from": "sales",
                "localField": "_id",
                "foreignField": "book_id",
                "as": "book_sales"
            }
        },
        {
            "$unwind": {
                "path": "$book_sales",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$group": {
                "_id": "$_id",
                "title": {"$first": "$name"},
                "author_id": {"$first": "$author_id"},
                "total_sales": {"$sum": {"$convert": {"input": "$book_sales.sales", "to": "int", "onError": 0, "onNull": 0}}},
                "publication_year": {"$first": {"$year": {"$dateFromString": {"dateString": "$date_of_publication"}}}}
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
            "$lookup": {
                "from": "sales",
                "localField": "author_id",
                "foreignField": "book_id",
                "as": "author_sales"
            }
        },
        {
            "$group": {
                "_id": "$_id",
                "title": {"$first": "$title"},
                "author": {"$first": "$author_info.name"},
                "author_id": {"$first": "$author_info._id"},
                "total_sales": {"$first": "$total_sales"},
                "author_total_sales": {"$sum": {"$convert": {"input": "$author_sales.sales", "to": "int", "onError": 0, "onNull": 0}}},
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
                "author_total_sales": 1,
                "is_top_5_publication_year": 1
            }
        }
    ]

    return list(books_collection.aggregate(pipeline))


def get_books_aggregate():
    pipeline = [
        {
            "$lookup": {
                "from": "sales",
                "localField": "_id",
                "foreignField": "book_id",
                "as": "book_sales"
            }
        },
        {
            '$unwind': {
                'path': '$book_sales',
                'preserveNullAndEmptyArrays': True
            }
        },
        {
            "$group": {
                "_id": "$_id",
                "name": { "$first": "$name" },
                "summary": { "$first": "$summary" },
                "date_of_publication": { "$first": "$date_of_publication" },
                "author_id": { "$first": "$author_id" },
                "number_of_sales": { '$sum': { '$toInt': '$book_sales.sales' } }
            }
        }
    ]
    return list(books_collection.aggregate(pipeline))

def get_book_by_id(pk):
    book = books_collection.find_one({"_id": ObjectId(pk)})
    if book:
        author = authors_collection.find_one({"_id": book["author_id"]}, {"_id": 1, "name": 1})
        if author:
            book["author"] = {"id": str(author["_id"]), "name": author["name"]}
    return book

def get_reviews_by_book(pk):
    return list(reviews_collection.find({"book_id": ObjectId(pk)}))

def get_sales_by_book(pk):
    return list(sales_collection.find({"book_id": ObjectId(pk)}))

def create_book(data):
    return books_collection.insert_one(data)

def update_book(pk, data):
    return books_collection.update_one({'_id': ObjectId(pk)}, {'$set': data})

def delete_book(pk):
    return books_collection.delete_one({'_id': ObjectId(pk)})
