from bson.objectid import ObjectId

def get_all(collection):
    collection_data = []
    for i in collection.find():
        i['id'] = str(i['_id'])
        collection_data.append(i)
    return collection_data

def get_related_books(author_id, books_collection):
    return list(books_collection.find({"author_id": ObjectId(author_id)}))

def get_related_reviews(book_id, reviews_collection):
    return list(reviews_collection.find({"book_id": ObjectId(book_id)}))

def get_related_sales(book_id, sales_collection):
    return list(sales_collection.find({"book_id": ObjectId(book_id)}))
