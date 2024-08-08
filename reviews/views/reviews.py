from django.shortcuts import render, redirect
from reviews.utils import reviews_collection, books_collection
from bson.objectid import ObjectId
from reviews.queries.reviews import get_all_reviews, get_review_by_id


def review_list(request):
    reviews = get_all_reviews()
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

def review_detail(request, pk):
    review = get_review_by_id(pk)
    return render(request, 'reviews/review_detail.html', {'review': review})

def review_create(request):
    if request.method == "POST":
        review = {
            "book_id": ObjectId(request.POST.get('book_id')),
            "review": request.POST.get('review'),
            "score": int(request.POST.get('score')),
            "number_of_upvotes": int(request.POST.get('number_of_upvotes'))
        }
        reviews_collection.insert_one(review)
        return redirect('review_list')
    books = list(books_collection.find())
    return render(request, 'reviews/review_form.html', {'books': books})

def review_edit(request, pk):
    review = get_review_by_id(pk)
    if request.method == "POST":
        updated_review = {
            "book_id": ObjectId(request.POST.get('book_id')),
            "review": request.POST.get('review'),
            "score": int(request.POST.get('score')),
            "number_of_upvotes": int(request.POST.get('number_of_upvotes'))
        }
        reviews_collection.update_one({'_id': ObjectId(pk)}, {'$set': updated_review})
        return redirect('review_list')
    books = list(books_collection.find())
    return render(request, 'reviews/review_form.html', {'review': review, 'books': books})

def review_delete(request, pk):
    review = get_review_by_id(pk)
    if request.method == "POST":
        reviews_collection.delete_one({'_id': ObjectId(pk)})
        return redirect('review_list')
    return render(request, 'reviews/review_confirm_delete.html', {'review': review})
