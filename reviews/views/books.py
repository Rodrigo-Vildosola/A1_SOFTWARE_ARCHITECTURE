from django.shortcuts import render, redirect
from decouple import config
from bson.objectid import ObjectId
import pymongo
from reviews.utils import get_all, get_reviews_by_book, get_sales_by_book

# MongoDB connection
client = pymongo.MongoClient(config('MONGODB_URI'))
db = client[config('DB_NAME')]
books_collection = db['books']
authors_collection = db['authors']
reviews_collection = db['reviews']
sales_collection = db['sales']

def get_all_books():
    books = []
    for data in books_collection.find():
        data["id"] = str(data["_id"])
        books.append(data)
    return books


def book_list(request):
    books = get_all_books()
    return render(request, 'books/book_list.html', {'books': books})

def book_detail(request, pk):
    book = books_collection.find_one({"_id": ObjectId(pk)})
    book["id"] = str(book["_id"])
    reviews = get_reviews_by_book(pk)
    sales = get_sales_by_book(pk)
    return render(request, 'books/book_detail.html', {'book': book, 'reviews': reviews, 'sales': sales})

def book_create(request):
    if request.method == "POST":
        book = {
            "name": request.POST.get('name'),
            "summary": request.POST.get('summary'),
            "date_of_publication": request.POST.get('date_of_publication'),
            "number_of_sales": int(request.POST.get('number_of_sales')),
            "author_id": request.POST.get('author_id')
        }
        print(book)
        books_collection.insert_one(book)
        return redirect('book_list')
    authors = list(authors_collection.find())
    return render(request, 'books/book_form.html', {'authors': authors})

def book_edit(request, pk):
    book = books_collection.find_one({"_id": ObjectId(pk)})
    if request.method == "POST":
        updated_book = {
            "name": request.POST.get('name'),
            "summary": request.POST.get('summary'),
            "date_of_publication": request.POST.get('date_of_publication'),
            "number_of_sales": int(request.POST.get('number_of_sales')),
            "author_id": request.POST.get('author_id')
        }
        print(book)

        books_collection.update_one({'_id': ObjectId(pk)}, {'$set': updated_book})
        return redirect('book_list')
    authors = list(authors_collection.find())
    return render(request, 'books/book_form.html', {'book': book, 'authors': authors})

def book_delete(request, pk):
    book = books_collection.find_one({"_id": ObjectId(pk)})
    if request.method == "POST":
        books_collection.delete_one({'_id': ObjectId(pk)})
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})
