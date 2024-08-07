from django.shortcuts import render, redirect
from decouple import config
from bson.objectid import ObjectId
import pymongo
from reviews.types import Author
from reviews.utils import get_author_with_books_reviews_sales

# MongoDB connection
client = pymongo.MongoClient(config('MONGODB_URI'))
db = client[config('DB_NAME')]
authors_collection = db['authors']

def get_all_authors():
    authors = []
    for data in authors_collection.find():
        authors.append(Author.deserialize(data))
    return authors

def author_list(request):
    authors = get_author_with_books_reviews_sales()
    for i in authors:
        print(i)
    return render(request, 'authors/author_list.html', {'authors': authors})

def author_detail(request, pk):
    data = authors_collection.find_one({"_id": ObjectId(pk)})
    author = Author.deserialize(data)
    return render(request, 'authors/author_detail.html', {'author': author})

def author_create(request):
    if request.method == "POST":
        author = Author(
            name=request.POST.get('name'),
            date_of_birth=request.POST.get('date_of_birth'),
            country_of_origin=request.POST.get('country_of_origin'),
            short_description=request.POST.get('short_description')
        )
        authors_collection.insert_one(author.serialize())
        return redirect('author_list')
    return render(request, 'authors/author_form.html')

def author_edit(request, pk):
    data = authors_collection.find_one({"_id": ObjectId(pk)})
    author = Author.deserialize(data)
    if request.method == "POST":
        updated_author = Author(
            name=request.POST.get('name'),
            date_of_birth=request.POST.get('date_of_birth'),
            country_of_origin=request.POST.get('country_of_origin'),
            short_description=request.POST.get('short_description'),
            id=pk
        )
        authors_collection.update_one({'_id': ObjectId(pk)}, {'$set': updated_author.serialize()})
        return redirect('author_list')
    return render(request, 'authors/author_form.html', {'author': author})

def author_delete(request, pk):
    data = authors_collection.find_one({"_id": ObjectId(pk)})
    author = Author.deserialize(data)
    if request.method == "POST":
        authors_collection.delete_one({'_id': ObjectId(pk)})
        return redirect('author_list')
    return render(request, 'authors/author_confirm_delete.html', {'author': author})
