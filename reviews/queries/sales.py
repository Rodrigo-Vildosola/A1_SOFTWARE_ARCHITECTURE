from reviews.mongo import Mongo
from bson.objectid import ObjectId

db = Mongo().database
authors_collection = db['object']

def get_all_sales():
    pipeline = [
        {
            "$unwind": "$books"
        },
        {
            "$unwind": "$books.sales"
        },
        {
            "$project": {
                "_id": "$books.sales._id",
                "author_name": "$name",
                "book_id": "$books._id",
                "book_name": "$books.name",
                "year": "$books.sales.year",
                "sales": "$books.sales.sales"
            }
        }
    ]
    return list(authors_collection.aggregate(pipeline))

def get_sale_by_id(sale_id):
    pipeline = [
        {
            "$unwind": "$books"
        },
        {
            "$unwind": "$books.sales"
        },
        {
            "$match": { "books.sales._id": ObjectId(sale_id) }
        },
        {
            "$project": {
                "_id": "$books.sales._id",
                "author_name": "$name",
                "book_id": "$books._id",
                "book_name": "$books.name",
                "year": "$books.sales.year",
                "sales": "$books.sales.sales"
            }
        }
    ]
    return authors_collection.aggregate(pipeline).next()

def create_sale(book_id, sale):
    sale["_id"] = ObjectId()
    authors_collection.update_one(
        {'books._id': ObjectId(book_id)},
        {'$push': {'books.$.sales': sale}}
    )
    return sale

def update_sale(sale_id, updated_sale):
    authors_collection.update_one(
        {'books.sales._id': ObjectId(sale_id)},
        {'$set': {
            "books.$[book].sales.$[sale].year": updated_sale["year"],
            "books.$[book].sales.$[sale].sales": updated_sale["sales"]
        }},
        array_filters=[
            {"book.sales._id": ObjectId(sale_id)}
        ]
    )

def delete_sale(sale_id):
    authors_collection.update_one(
        {'books.sales._id': ObjectId(sale_id)},
        {'$pull': {'books.$[book].sales': {'_id': ObjectId(sale_id)}}},
        array_filters=[
            {"book.sales._id": ObjectId(sale_id)}
        ]
    )
