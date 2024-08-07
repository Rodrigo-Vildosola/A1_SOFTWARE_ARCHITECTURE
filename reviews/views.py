from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
import pymongo
from bson.objectid import ObjectId
from decouple import config

# MongoDB connection
client = pymongo.MongoClient(config('MONGODB_URI'))
db = client[config('DB_NAME')]

# Collections
authors_collection = db['authors']
books_collection = db['books']
reviews_collection = db['reviews']
salesbyyear_collection = db['salesbyyear']

def get_all(collection):
    collection_data = []
    for i in collection.find():
        i['id'] = str(i['_id'])
        collection_data.append(i)
    return collection_data

# Author Views
def author_list(request):
    authors = get_all(authors_collection)
    return render(request, 'reviews/author_list.html', {'authors': authors})

def author_detail(request, pk):
    author = authors_collection.find_one({"_id": ObjectId(pk)})
    author['id'] = str(author['_id'])
    return render(request, 'reviews/author_detail.html', {'author': author})

def author_create(request):
    if request.method == "POST":
        name = request.POST.get('name')
        date_of_birth = request.POST.get('date_of_birth')
        country_of_origin = request.POST.get('country_of_origin')
        short_description = request.POST.get('short_description')
        author = {
            "name": name,
            "date_of_birth": date_of_birth,
            "country_of_origin": country_of_origin,
            "short_description": short_description
        }
        authors_collection.insert_one(author)
        return redirect('author_list')
    return render(request, 'reviews/author_form.html')

def author_edit(request, pk):
    author = authors_collection.find_one({"_id": ObjectId(pk)})
    if request.method == "POST":
        updated_data = {
            "name": request.POST.get('name'),
            "date_of_birth": request.POST.get('date_of_birth'),
            "country_of_origin": request.POST.get('country_of_origin'),
            "short_description": request.POST.get('short_description')
        }
        authors_collection.update_one({'_id': ObjectId(pk)}, {'$set': updated_data})
        return redirect('author_list')
    author['id'] = str(author['_id'])
    return render(request, 'reviews/author_form.html', {'author': author})

def author_delete(request, pk):
    author = authors_collection.find_one({"_id": ObjectId(pk)})
    if request.method == "POST":
        authors_collection.delete_one({'_id': ObjectId(pk)})
        return redirect('author_list')
    author['id'] = str(author['_id'])
    return render(request, 'reviews/author_confirm_delete.html', {'author': author})

# Book Views
def book_list(request):
    books = get_all(books_collection)
    return render(request, 'reviews/book_list.html', {'books': books})

def book_detail(request, pk):
    book = books_collection.find_one({"_id": ObjectId(pk)})
    book['id'] = str(book['_id'])
    return render(request, 'reviews/book_detail.html', {'book': book})

def book_create(request):
    if request.method == "POST":
        name = request.POST.get('name')
        summary = request.POST.get('summary')
        date_of_publication = request.POST.get('date_of_publication')
        number_of_sales = request.POST.get('number_of_sales')
        author_id = request.POST.get('author_id')
        book = {
            "name": name,
            "summary": summary,
            "date_of_publication": date_of_publication,
            "number_of_sales": number_of_sales,
            "author_id": ObjectId(author_id)
        }
        books_collection.insert_one(book)
        return redirect('book_list')
    authors = get_all(authors_collection)
    return render(request, 'reviews/book_form.html', {'authors': authors})

def book_edit(request, pk):
    book = books_collection.find_one({"_id": ObjectId(pk)})
    if request.method == "POST":
        updated_data = {
            "name": request.POST.get('name'),
            "summary": request.POST.get('summary'),
            "date_of_publication": request.POST.get('date_of_publication'),
            "number_of_sales": request.POST.get('number_of_sales'),
            "author_id": ObjectId(request.POST.get('author_id'))
        }
        books_collection.update_one({'_id': ObjectId(pk)}, {'$set': updated_data})
        return redirect('book_list')
    book['id'] = str(book['_id'])
    authors = get_all(authors_collection)
    return render(request, 'reviews/book_form.html', {'book': book, 'authors': authors})

def book_delete(request, pk):
    book = books_collection.find_one({"_id": ObjectId(pk)})
    if request.method == "POST":
        books_collection.delete_one({'_id': ObjectId(pk)})
        return redirect('book_list')
    book['id'] = str(book['_id'])
    return render(request, 'reviews/book_confirm_delete.html', {'book': book})

# Review Views
def review_list(request):
    reviews = get_all(reviews_collection)
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

def review_detail(request, pk):
    review = reviews_collection.find_one({"_id": ObjectId(pk)})
    review['id'] = str(review['_id'])
    return render(request, 'reviews/review_detail.html', {'review': review})

def review_create(request):
    if request.method == "POST":
        book_id = request.POST.get('book_id')
        review_text = request.POST.get('review')
        score = request.POST.get('score')
        number_of_upvotes = request.POST.get('number_of_upvotes')
        review = {
            "book_id": ObjectId(book_id),
            "review": review_text,
            "score": score,
            "number_of_upvotes": number_of_upvotes
        }
        reviews_collection.insert_one(review)
        return redirect('review_list')
    books = get_all(books_collection)
    return render(request, 'reviews/review_form.html', {'books': books})

def review_edit(request, pk):
    review = reviews_collection.find_one({"_id": ObjectId(pk)})
    if request.method == "POST":
        updated_data = {
            "book_id": ObjectId(request.POST.get('book_id')),
            "review": request.POST.get('review'),
            "score": request.POST.get('score'),
            "number_of_upvotes": request.POST.get('number_of_upvotes')
        }
        reviews_collection.update_one({'_id': ObjectId(pk)}, {'$set': updated_data})
        return redirect('review_list')
    review['id'] = str(review['_id'])
    books = get_all(books_collection)
    return render(request, 'reviews/review_form.html', {'review': review, 'books': books})

def review_delete(request, pk):
    review = reviews_collection.find_one({"_id": ObjectId(pk)})
    if request.method == "POST":
        reviews_collection.delete_one({'_id': ObjectId(pk)})
        return redirect('review_list')
    review['id'] = str(review['_id'])
    return render(request, 'reviews/review_confirm_delete.html', {'review': review})

# SalesByYear Views
def salesbyyear_list(request):
    sales = get_all(salesbyyear_collection)
    return render(request, 'reviews/salesbyyear_list.html', {'sales': sales})

def salesbyyear_detail(request, pk):
    sales = salesbyyear_collection.find_one({"_id": ObjectId(pk)})
    sales['id'] = str(sales['_id'])
    return render(request, 'reviews/salesbyyear_detail.html', {'sales': sales})

def salesbyyear_create(request):
    if request.method == "POST":
        book_id = request.POST.get('book_id')
        year = request.POST.get('year')
        sales = request.POST.get('sales')
        sales_record = {
            "book_id": ObjectId(book_id),
            "year": year,
            "sales": sales
        }
        salesbyyear_collection.insert_one(sales_record)
        return redirect('salesbyyear_list')
    books = get_all(books_collection)
    return render(request, 'reviews/salesbyyear_form.html', {'books': books})

def salesbyyear_edit(request, pk):
    sales = salesbyyear_collection.find_one({"_id": ObjectId(pk)})
    if request.method == "POST":
        updated_data = {
            "book_id": ObjectId(request.POST.get('book_id')),
            "year": request.POST.get('year'),
            "sales": request.POST.get('sales')
        }
        salesbyyear_collection.update_one({'_id': ObjectId(pk)}, {'$set': updated_data})
        return redirect('salesbyyear_list')
    sales['id'] = str(sales['_id'])
    books = get_all(books_collection)
    return render(request, 'reviews/salesbyyear_form.html', {'sales': sales, 'books': books})

def salesbyyear_delete(request, pk):
    sales = salesbyyear_collection.find_one({"_id": ObjectId(pk)})
    if request.method == "POST":
        salesbyyear_collection.delete_one({'_id': ObjectId(pk)})
        return redirect('salesbyyear_list')
    sales['id'] = str(sales['_id'])
    return render(request, 'reviews/salesbyyear_confirm_delete.html', {'sales': sales})
