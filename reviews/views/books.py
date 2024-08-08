from django.shortcuts import render, redirect
from bson.objectid import ObjectId
from reviews.utils import authors_collection
from reviews.queries.books import (
    get_top_rated_books,
    get_books_aggregate,
    get_book_by_id,
    get_reviews_by_book,
    get_sales_by_book,
    create_book,
    update_book,
    delete_book
)


def top_books(request):
    top_rated_books = get_top_rated_books()
    top_selling_books = [
        {
            "title": "Book A",
            "author": "Author A",
            "total_sales": 1000000,
            "author_total_sales": 5000000,
            "top_5_publication_year": "Yes",
        },
        # ... more books
    ]
    context = {
        'top_rated_books': top_rated_books,
        'top_selling_books': top_selling_books,
    }
    return render(request, 'top_books.html', context)


def book_list(request):
    books = get_books_aggregate()
    return render(request, 'books/book_list.html', {'books': books})

def book_detail(request, pk):
    book = get_book_by_id(pk)
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
        create_book(book)
        return redirect('book_list')
    authors = list(authors_collection.find())
    return render(request, 'books/book_form.html', {'authors': authors})

def book_edit(request, pk):
    book = get_book_by_id(pk)
    if request.method == "POST":
        updated_book = {
            "name": request.POST.get('name'),
            "summary": request.POST.get('summary'),
            "date_of_publication": request.POST.get('date_of_publication'),
            "author_id": ObjectId(request.POST.get('author_id'))
        }
        update_book(pk, updated_book)
        return redirect('book_list')
    authors = list(authors_collection.find())
    return render(request, 'books/book_form.html', {'book': book, 'authors': authors})

def book_delete(request, pk):
    book = get_book_by_id(pk)
    if request.method == "POST":
        delete_book(pk)
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})
