from pymongo import MongoClient
from bson.objectid import ObjectId
from decouple import config
from .types import Author, Book, Review, Sales

# MongoDB connection
client = MongoClient(config('MONGODB_URI'))
db = client[config('DB_NAME')]

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
    for book in books:
        book['id'] = str(book['_id'])
    return list(books)

def get_reviews_by_book(book_id):
    reviews = reviews_collection.find({"book_id": ObjectId(book_id)})
    for review in reviews:
        review['id'] = str(review['_id'])
    return list(reviews)

def get_sales_by_book(book_id):
    sales = sales_collection.find({"book_id": ObjectId(book_id)})
    for sale in sales:
        sale['id'] = str(sale['_id'])
    return list(sales)

def get_author_with_books_reviews_sales():
    authors_aggregate = authors_collection.aggregate([
        {
            "$lookup": {
                "from": "books",
                "localField": "_id",
                "foreignField": "author_id",
                "as": "books"
            }
        },
        {
            "$unwind": {
                "path": "$books",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$lookup": {
                "from": "reviews",
                "localField": "books._id",
                "foreignField": "book_id",
                "as": "reviews"
            }
        },
        {
            "$lookup": {
                "from": "sales",
                "localField": "books._id",
                "foreignField": "book_id",
                "as": "sales"
            }
        },
        {
            "$group": {
                "_id": "$_id",
                "name": { "$first": "$name" },
                "number_of_books": { "$sum": { "$cond": [{ "$ifNull": ["$books._id", False] }, 1, 0] } },
                "average_score": { "$avg": "$reviews.score" },
                "total_sales": { "$sum": "$sales.sales" }
            }
        },
        {
            "$addFields": {
                "id": { "$toString": "$_id" }
            }
        },
        {
            "$project": {
                "_id": 0
            }
        }
    ])
    return list(authors_aggregate)

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
        },
        {
            "$project": {
                "_id": 0
            }
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
        },
        {
            "$project": {
                "_id": 0
            }
        }
    ])
    return list(top_selling_books_aggregate)

def search_books(query, page=1, limit=10):
    skip = (page - 1) * limit
    search_results = books_collection.find(
        { "$text": { "$search": query } },
        { "score": { "$meta": "textScore" } }
    ).sort(
        [("score", { "$meta": "textScore" })]
    ).skip(skip).limit(limit)
    
    books = []
    for book in search_results:
        book['id'] = str(book['_id'])
        books.append(book)
    
    return books
