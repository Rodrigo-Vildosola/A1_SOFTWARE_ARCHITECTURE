from django.shortcuts import render, redirect
from decouple import config
from bson.objectid import ObjectId
import pymongo
from reviews.utils import get_all, get_reviews_by_book, get_sales_by_book
from reviews.mongo import Mongo

# MongoDB connection
db = Mongo().database
books_collection = db['books']
authors_collection = db['authors']
reviews_collection = db['reviews']
sales_collection = db['sales']


def book_list(request):
    books_aggregate = books_collection.aggregate([
        {
            "$lookup": {
                "from": "sales",
                "localField": "_id",
                "foreignField": "book_id",
                "as": "sales"
            }
        },
        {
            "$addFields": {
                "number_of_sales": { "$sum": "$sales.sales" }
            }
        },
        {
            "$project": {
                "name": 1,
                "summary": 1,
                "date_of_publication": 1,
                "author_id": 1,
                "number_of_sales": 1
            }
        }
    ])
    books = list(books_aggregate)
    print(books)
    return render(request, 'books/book_list.html', {'books': books})

def book_detail(request, pk):
    book = books_collection.find_one({"_id": ObjectId(pk)})
    reviews = get_reviews_by_book(pk)
    sales = get_sales_by_book(pk)
    
    # Calculate the total sales for the book
    total_sales = sum(int(sale['sales']) for sale in sales)
    book['number_of_sales'] = total_sales
    
    return render(request, 'books/book_detail.html', {'book': book, 'reviews': reviews, 'sales': sales})

def book_create(request):
    if request.method == "POST":
        book = {
            "name": request.POST.get('name'),
            "summary": request.POST.get('summary'),
            "date_of_publication": request.POST.get('date_of_publication'),
            "author_id": ObjectId(request.POST.get('author_id'))
        }
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
            "author_id": ObjectId(request.POST.get('author_id'))
        }
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
