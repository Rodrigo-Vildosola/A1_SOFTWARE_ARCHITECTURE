from django.http import JsonResponse
from django.shortcuts import render, redirect
from reviews.utils import collection
from bson.objectid import ObjectId
from django.urls import reverse
from reviews.queries.reviews import get_all_reviews, get_review_by_id, create_review, update_review, delete_review


def review_list(request):
    return render(request, 'reviews/review_list.html')

def review_data(request):
    page = int(request.GET.get('page', 1))
    name_filter = request.GET.get('name_filter', '')

    reviews, total_reviews_count = get_all_reviews(page, name_filter)

    for review in reviews:
        review['_id'] = str(review['_id'])
        review['book_id'] = str(review['book_id'])


    response_data = {
        'reviews': reviews,
        'num_pages': (total_reviews_count + 19) // 20,  # Calculate number of pages
        'current_page': page,
    }

    return JsonResponse(response_data)

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
    
    books = list(collection.aggregate([
        {"$unwind": "$books"},
        {"$project": {"_id": "$books._id", "name": "$books.name"}}
    ]))
    return render(request, 'reviews/review_form.html', {'books': books})



def review_create_for_book(request, book_id):
    book = collection.find_one({"books._id": ObjectId(book_id)}, {"books.$": 1})
    book = book['books'][0] if book else None
    
    if request.method == "POST":
        review = {
            "review": request.POST.get('review'),
            "score": int(request.POST.get('score')),
            "number_of_upvotes": int(request.POST.get('number_of_upvotes'))
        }
        create_review(ObjectId(book_id), review)
        return redirect(reverse('book_detail', args=[str(book_id)]))
    
    return render(request, 'reviews/review_form.html', {'book': book})


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
