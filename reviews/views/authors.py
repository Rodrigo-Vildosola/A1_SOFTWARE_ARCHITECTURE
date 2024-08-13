from django.shortcuts import render, redirect
from bson.objectid import ObjectId
from reviews.queries.authors import get_author_with_books_reviews_sales, get_books_by_author
from reviews.mongo import Mongo
from django.core.paginator import Paginator
from django.http import JsonResponse

# MongoDB connection
db = Mongo().database
authors_collection = db.object


def author_list(request):
    return render(request, 'authors/author_list.html')

def author_data(request):
    sort_by = request.GET.get('sort_by', 'name')
    order = request.GET.get('order', 'asc')
    page = int(request.GET.get('page', 1))
    name_filter = request.GET.get('name_filter', '')

    authors, num_pages = get_author_with_books_reviews_sales(page, sort_by, order, name_filter)

    # Convert ObjectId to string
    for author in authors:
        author['_id'] = str(author['_id'])

    response_data = {
        'authors': authors,
        'num_pages': num_pages,
        'current_page': page,
        'sort_by': sort_by,
        'order': order,
    }

    return JsonResponse(response_data, safe=False)


def author_detail(request, pk):
    author = authors_collection.find_one({"_id": ObjectId(pk)})
    books = get_books_by_author(pk)  # Fetch books by author
    return render(request, 'authors/author_detail.html', {'author': author, 'books': books})

def author_create(request):
    if request.method == "POST":
        author = {
            "name": request.POST.get('name'),
            "date_of_birth": request.POST.get('date_of_birth'),
            "country_of_origin": request.POST.get('country_of_origin'),
            "short_description": request.POST.get('short_description')
        }
        authors_collection.insert_one(author)
        return redirect('author_list')
    return render(request, 'authors/author_form.html')

def author_edit(request, pk):
    author = authors_collection.find_one({"_id": ObjectId(pk)})
    if request.method == "POST":
        updated_author = {
            "name": request.POST.get('name'),
            "date_of_birth": request.POST.get('date_of_birth'),
            "country_of_origin": request.POST.get('country_of_origin'),
            "short_description": request.POST.get('short_description')
        }
        authors_collection.update_one({'_id': ObjectId(pk)}, {'$set': updated_author})
        return redirect('author_list')
    return render(request, 'authors/author_form.html', {'author': author})

def author_delete(request, pk):
    author = authors_collection.find_one({"_id": ObjectId(pk)})
    if request.method == "POST":
        authors_collection.delete_one({'_id': ObjectId(pk)})
        return redirect('author_list')
    return render(request, 'authors/author_confirm_delete.html', {'author': author})
