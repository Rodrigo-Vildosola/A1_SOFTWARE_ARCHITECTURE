from django.shortcuts import render, redirect
from decouple import config
from bson.objectid import ObjectId
import pymongo
from reviews.utils import get_author_with_books_reviews_sales
from reviews.mongo import Mongo
from reviews.queries.authors import get_books_by_author  # Import the new query function


# MongoDB connection
db = Mongo().database
authors_collection = db['authors']
books_collection = db['books']



def author_list(request):
    authors = get_author_with_books_reviews_sales()
    return render(request, 'authors/author_list.html', {'authors': authors})

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
