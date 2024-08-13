from django.shortcuts import render, redirect
from reviews.utils import collection
from bson.objectid import ObjectId
from reviews.queries.reviews import get_all_reviews, get_review_by_id, create_review, update_review, delete_review


def review_list(request):
    reviews = get_all_reviews()
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

def review_detail(request, pk):
    review = get_review_by_id(pk)
    if review: 
        return render(request, 'reviews/review_detail.html', {'review': review})
    else:
        return render(request, '404.html', {'message': 'Review not found'})

def review_create(request):
    if request.method == "POST":
        book_id = ObjectId(request.POST.get('book_id'))
        review = {
            "review": request.POST.get('review'),
            "score": int(request.POST.get('score')),
            "number_of_upvotes": int(request.POST.get('number_of_upvotes'))
        }
        create_review(book_id, review)
        return redirect('review_list')
    
    # Fetch only necessary fields (name and id) to avoid loading too much data
    books = list(collection.aggregate([
        {"$unwind": "$books"},
        {"$project": {"_id": "$books._id", "name": "$books.name"}}
    ]))
    return render(request, 'reviews/review_form.html', {'books': books})

def review_edit(request, pk):
    review = get_review_by_id(pk)
    if request.method == "POST":
        updated_review = {
            "review": request.POST.get('review'),
            "score": int(request.POST.get('score')),
            "number_of_upvotes": int(request.POST.get('number_of_upvotes'))
        }
        update_review(pk, updated_review)
        return redirect('review_list')
    
    # Fetch only necessary fields (name and id) to avoid loading too much data
    books = list(collection.aggregate([
        {"$unwind": "$books"},
        {"$project": {"_id": "$books._id", "name": "$books.name"}}
    ]))
    return render(request, 'reviews/review_form.html', {'review': review, 'books': books})

def review_delete(request, pk):
    review = get_review_by_id(pk)
    if request.method == "POST":
        delete_review(pk)
        return redirect('review_list')
    return render(request, 'reviews/review_confirm_delete.html', {'review': review})
