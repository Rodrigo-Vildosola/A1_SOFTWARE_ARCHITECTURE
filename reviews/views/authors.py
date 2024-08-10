from django.shortcuts import render, redirect
from bson.objectid import ObjectId
from reviews.queries.authors import get_author_with_books_reviews_sales, get_books_by_author
from reviews.mongo import Mongo

# MongoDB connection
db = Mongo().database
authors_collection = db.object

def author_list(request):
    sort_by = request.GET.get('sort_by', 'name')
    order = request.GET.get('order', 'asc')

    authors = get_author_with_books_reviews_sales()

    reverse = True if order == 'desc' else False

    if sort_by == 'name':
        authors = sorted(authors, key=lambda x: x['name'].lower() if x['name'] else '', reverse=reverse)
    elif sort_by == 'number_of_books':
        authors = sorted(authors, key=lambda x: x.get('number_of_books', 0), reverse=reverse)
    elif sort_by == 'average_score':
        authors = sorted(authors, key=lambda x: x.get('average_score', float('-inf')) if x.get('average_score') is not None else float('-inf'), reverse=reverse)
    elif sort_by == 'total_sales':
        authors = sorted(authors, key=lambda x: x.get('total_sales', float('-inf')) if x.get('total_sales') is not None else float('-inf'), reverse=reverse)

    sort_arrows = {
        'name': '▼' if sort_by == 'name' and order == 'asc' else '▲' if sort_by == 'name' else '',
        'number_of_books': '▼' if sort_by == 'number_of_books' and order == 'asc' else '▲' if sort_by == 'number_of_books' else '',
        'average_score': '▼' if sort_by == 'average_score' and order == 'asc' else '▲' if sort_by == 'average_score' else '',
        'total_sales': '▼' if sort_by == 'total_sales' and order == 'asc' else '▲' if sort_by == 'total_sales' else '',
    }

    return render(request, 'authors/author_list.html', {'authors': authors, 'sort_by': sort_by, 'order': order, 'sort_arrows': sort_arrows})

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
