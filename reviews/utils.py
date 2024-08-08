from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config
from .mongo import Mongo

# MongoDB connection
db = Mongo().database

authors_collection = db['authors']
books_collection = db['books']
reviews_collection = db['reviews']
sales_collection = db['sales']

def get_all(collection):
    collection_data = []
    for i in collection.find():
        i['id'] = str(i['_id'])
        collection_data.append(i)
    return collection_data

def get_books_by_author(author_id):
    books = books_collection.find({"author_id": ObjectId(author_id)})
    return list(books)

def get_reviews_by_book(book_id):
    reviews = reviews_collection.find({"book_id": ObjectId(book_id)})
    return list(reviews)

def get_sales_by_book(book_id):
    sales = sales_collection.find({"book_id": ObjectId(book_id)})
    return list(sales)

def get_author_with_books_reviews_sales():
    pipeline = [
        {
            '$lookup': {
                'from': 'books',
                'localField': '_id',
                'foreignField': 'author_id',
                'as': 'author_books'
            }
        },
        {
            '$addFields': {
                'number_of_books': { '$size': '$author_books' }
            }
        },
        {
            '$unwind': {
                'path': '$author_books',
                'preserveNullAndEmptyArrays': True
            }
        },
        {
            '$lookup': {
                'from': 'sales',
                'localField': 'author_books._id',
                'foreignField': 'book_id',
                'as': 'book_sales'
            }
        },
        {
            '$lookup': {
                'from': 'reviews',
                'localField': 'author_books._id',
                'foreignField': 'book_id',
                'as': 'book_reviews'
            }
        },
        {
            '$group': {
                '_id': '$_id',
                'name': { '$first': '$name' },
                'date_of_birth': { '$first': '$date_of_birth' },
                'country_of_origin': { '$first': '$country_of_origin' },
                'short_description': { '$first': '$short_description' },
                'number_of_books': { '$first': '$number_of_books' },
                'total_sales': { 
                    '$sum': { 
                        '$sum': { 
                            '$ifNull': [ 
                                { 
                                    '$map': { 
                                        'input': '$book_sales', 
                                        'as': 'sale', 
                                        'in': { '$toInt': '$$sale.sales' } 
                                    } 
                                }, 
                                0 
                            ] 
                        } 
                    } 
                },
                'average_score': {
                    '$avg': {
                        '$avg': {
                            '$ifNull': [
                                {
                                    '$map': {
                                        'input': '$book_reviews',
                                        'as': 'book_review',
                                        'in': { '$toDouble': '$$book_review.score' }
                                    }
                                },
                                []
                            ]
                        }
                    }
                }
            }
        },
        {
            '$sort': { 'name': 1 }  # Sort by author name
        }
    ]

    # Execute the aggregation pipeline
    return list(authors_collection.aggregate(pipeline))

def get_top_rated_books_with_reviews():
    top_rated_books_aggregate = books_collection.aggregate([
        {
            "$lookup": {
                "from": "reviews",
                "localField": "_id",
                "foreignField": "book_id",
                "as": "reviews"
            }
        },
        {
            "$addFields": {
                "average_score": { "$avg": "$reviews.score" },
                "highest_review": { "$arrayElemAt": [{ "$sortArray": { "input": "$reviews", "sortBy": { "score": -1 } } }, 0] },
                "lowest_review": { "$arrayElemAt": [{ "$sortArray": { "input": "$reviews", "sortBy": { "score": 1 } } }, 0] },
                "id": { "$toString": "$_id" }
            }
        },
        {
            "$sort": { "average_score": -1 }
        },
        {
            "$limit": 10
        }
    ])
    return list(top_rated_books_aggregate)

def get_top_selling_books():
    top_selling_books_aggregate = books_collection.aggregate([
        {
            "$lookup": {
                "from": "sales",
                "localField": "_id",
                "foreignField": "book_id",
                "as": "sales"
            }
        },
        {
            "$group": {
                "_id": "$_id",
                "name": { "$first": "$name" },
                "author_id": { "$first": "$author_id" },
                "total_sales": { "$sum": "$sales.sales" },
                "year_sales": { "$push": "$sales" }
            }
        },
        {
            "$lookup": {
                "from": "authors",
                "localField": "author_id",
                "foreignField": "_id",
                "as": "author"
            }
        },
        {
            "$unwind": "$author"
        },
        {
            "$lookup": {
                "from": "books",
                "localField": "author._id",
                "foreignField": "author_id",
                "as": "author_books"
            }
        },
        {
            "$addFields": {
                "author_total_sales": { "$sum": "$author_books.sales.sales" },
                "top_5_years": {
                    "$map": {
                        "input": { "$filter": { "input": "$year_sales", "as": "sale", "cond": { "$lte": ["$$sale.sales", 5] } } },
                        "as": "sale",
                        "in": "$$sale.year"
                    }
                },
                "id": { "$toString": "$_id" }
            }
        },
        {
            "$sort": { "total_sales": -1 }
        },
        {
            "$limit": 50
        }
    ])
    return list(top_selling_books_aggregate)

def search_books(query, page=1, limit=10):
    skip = (page - 1) * limit
    regex_query = {"$regex": query, "$options": "i"}  # Case-insensitive regex

    search_results = books_collection.find(
        { "$or": [ {"name": regex_query}, {"summary": regex_query} ] }
    ).skip(skip).limit(limit)
    
    books = []
    for book in search_results:
        book['id'] = str(book['_id'])
        books.append(book)
    
    return books

