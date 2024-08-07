from django.shortcuts import render, redirect
from decouple import config
from bson.objectid import ObjectId
import pymongo
from reviews.types import Review
from reviews.utils import get_all

# MongoDB connection
client = pymongo.MongoClient(config('MONGODB_URI'))
db = client[config('DB_NAME')]
reviews_collection = db['reviews']
books_collection = db['books']

def get_all_reviews():
    reviews = []
    for data in reviews_collection.find():
        reviews.append(Review.deserialize(data))
    return reviews

def review_list(request):
    reviews = get_all_reviews()
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

def review_detail(request, pk):
    data = reviews_collection.find_one({"_id": ObjectId(pk)})
    review = Review.deserialize(data)
    return render(request, 'reviews/review_detail.html', {'review': review})

def review_create(request):
    if request.method == "POST":
        review = Review(
            book_id=request.POST.get('book_id'),
            review=request.POST.get('review'),
            score=request.POST.get('score'),
            number_of_upvotes=request.POST.get('number_of_upvotes')
        )
        reviews_collection.insert_one(review.serialize())
        return redirect('review_list')
    books = get_all(books_collection)
    return render(request, 'reviews/review_form.html', {'books': books})

def review_edit(request, pk):
    data = reviews_collection.find_one({"_id": ObjectId(pk)})
    review = Review.deserialize(data)
    if request.method == "POST":
        updated_review = Review(
            book_id=request.POST.get('book_id'),
            review=request.POST.get('review'),
            score=request.POST.get('score'),
            number_of_upvotes=request.POST.get('number_of_upvotes'),
            id=pk
        )
        reviews_collection.update_one({'_id': ObjectId(pk)}, {'$set': updated_review.serialize()})
        return redirect('review_list')
    books = get_all(books_collection)
    return render(request, 'reviews/review_form.html', {'review': review, 'books': books})

def review_delete(request, pk):
    data = reviews_collection.find_one({"_id": ObjectId(pk)})
    review = Review.deserialize(data)
    if request.method == "POST":
        reviews_collection.delete_one({'_id': ObjectId(pk)})
        return redirect('review_list')
    return render(request, 'reviews/review_confirm_delete.html', {'review': review})
