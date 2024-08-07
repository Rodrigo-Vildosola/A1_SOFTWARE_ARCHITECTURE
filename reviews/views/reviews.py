from django.shortcuts import render, redirect
from bson.objectid import ObjectId
from decouple import config
import pymongo

# MongoDB connection
client = pymongo.MongoClient(config('MONGODB_URI'))
db = client[config('DB_NAME')]
reviews_collection = db['reviews']
books_collection = db['books']

def get_all(collection):
    collection_data = []
    for i in collection.find():
        i['id'] = str(i['_id'])
        collection_data.append(i)
    return collection_data

def review_list(request):
    reviews = get_all(reviews_collection)
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

def review_detail(request, pk):
    review = reviews_collection.find_one({"_id": ObjectId(pk)})
    review['id'] = str(review['_id'])
    return render(request, 'reviews/review_detail.html', {'review': review})

def review_create(request):
    if request.method == "POST":
        book_id = request.POST.get('book_id')
        review_text = request.POST.get('review')
        score = request.POST.get('score')
        number_of_upvotes = request.POST.get('number_of_upvotes')
        review = {
            "book_id": ObjectId(book_id),
            "review": review_text,
            "score": score,
            "number_of_upvotes": number_of_upvotes
        }
        reviews_collection.insert_one(review)
        return redirect('review_list')
    books = get_all(books_collection)
    return render(request, 'reviews/review_form.html', {'books': books})

def review_edit(request, pk):
    review = reviews_collection.find_one({"_id": ObjectId(pk)})
    if request.method == "POST":
        updated_data = {
            "book_id": ObjectId(request.POST.get('book_id')),
            "review": request.POST.get('review'),
            "score": request.POST.get('score'),
            "number_of_upvotes": request.POST.get('number_of_upvotes')
        }
        reviews_collection.update_one({'_id': ObjectId(pk)}, {'$set': updated_data})
        return redirect('review_list')
    review['id'] = str(review['_id'])
    books = get_all(books_collection)
    return render(request, 'reviews/review_form.html', {'review': review, 'books': books})

def review_delete(request, pk):
    review = reviews_collection.find_one({"_id": ObjectId(pk)})
    if request.method == "POST":
        reviews_collection.delete_one({'_id': ObjectId(pk)})
        return redirect('review_list')
    review['id'] = str(review['_id'])
    return render(request, 'reviews/review_confirm_delete.html', {'review': review})
