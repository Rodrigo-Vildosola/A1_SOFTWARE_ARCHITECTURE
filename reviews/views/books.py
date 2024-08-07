from django.shortcuts import render, redirect
from decouple import config
from bson.objectid import ObjectId
import pymongo
from reviews.types import Book
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
        books.append(Book.deserialize(data))
    return books

def book_list(request):
    books = get_all_books()
    return render(request, 'books/book_list.html', {'books': books})

def book_detail(request, pk):
    data = books_collection.find_one({"_id": ObjectId(pk)})
    book = Book.deserialize(data)
    reviews = get_reviews_by_book(pk, reviews_collection)
    sales = get_sales_by_book(pk, sales_collection)
    print(reviews)
    print(sales)
    return render(request, 'books/book_detail.html', {'book': book, 'reviews': reviews, 'sales': sales})

def book_create(request):
    if request.method == "POST":
        book = Book(
            name=request.POST.get('name'),
            summary=request.POST.get('summary'),
            date_of_publication=request.POST.get('date_of_publication'),
            number_of_sales=request.POST.get('number_of_sales'),
            author_id=request.POST.get('author_id')
        )
        books_collection.insert_one(book.serialize())
        return redirect('book_list')
    authors = get_all(authors_collection)
    return render(request, 'books/book_form.html', {'authors': authors})

def book_edit(request, pk):
    data = books_collection.find_one({"_id": ObjectId(pk)})
    book = Book.deserialize(data)
    if request.method == "POST":
        updated_book = Book(
            name=request.POST.get('name'),
            summary=request.POST.get('summary'),
            date_of_publication=request.POST.get('date_of_publication'),
            number_of_sales=request.POST.get('number_of_sales'),
            author_id=request.POST.get('author_id'),
            id=pk
        )
        books_collection.update_one({'_id': ObjectId(pk)}, {'$set': updated_book.serialize()})
        return redirect('book_list')
    authors = get_all(authors_collection)
    return render(request, 'books/book_form.html', {'book': book, 'authors': authors})

def book_delete(request, pk):
    data = books_collection.find_one({"_id": ObjectId(pk)})
    book = Book.deserialize(data)
    if request.method == "POST":
        books_collection.delete_one({'_id': ObjectId(pk)})
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})
