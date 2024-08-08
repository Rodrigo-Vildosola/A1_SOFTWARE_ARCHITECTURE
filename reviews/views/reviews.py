from django.shortcuts import render, redirect
from bson.objectid import ObjectId
from reviews.utils import get_all
from reviews.mongo import Mongo

# MongoDB connection
db = Mongo().database
reviews_collection = db['reviews']
books_collection = db['books']

def get_all_reviews():
    reviews = []
    for data in reviews_collection.find():
        reviews.append(data)
    return reviews

def review_list(request):
    reviews = list(reviews_collection.find())
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

def review_detail(request, pk):
    data = reviews_collection.find_one({"_id": ObjectId(pk)})
    return render(request, 'reviews/review_detail.html', {'review': data})

def review_create(request):
    if request.method == "POST":
        review = {
            "book_id": ObjectId(request.POST.get('book_id')),
            "review": request.POST.get('review'),
            "score": request.POST.get('score'),
            "number_of_upvotes": request.POST.get('number_of_upvotes')
        }
        reviews_collection.insert_one(review)
        return redirect('review_list')
    books = list(books_collection.find())
    return render(request, 'reviews/review_form.html', {'books': books})

def review_edit(request, pk):
    data = reviews_collection.find_one({"_id": ObjectId(pk)})
    if request.method == "POST":
        updated_review = {
            "book_id": ObjectId(request.POST.get('book_id')),
            "review": request.POST.get('review'),
            "score": request.POST.get('score'),
            "number_of_upvotes": request.POST.get('number_of_upvotes')
        }
        reviews_collection.update_one({'_id': ObjectId(pk)}, {'$set': updated_review})
        return redirect('review_list')
    books = list(books_collection.find())
    return render(request, 'reviews/review_form.html', {'review': data, 'books': books})

def review_delete(request, pk):
    data = reviews_collection.find_one({"_id": ObjectId(pk)})
    if request.method == "POST":
        reviews_collection.delete_one({'_id': ObjectId(pk)})
        return redirect('review_list')
    return render(request, 'reviews/review_confirm_delete.html', {'review': data})
