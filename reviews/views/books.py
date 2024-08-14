from django.http import JsonResponse
from django.shortcuts import render, redirect
from bson.objectid import ObjectId
from reviews.mongo import Mongo
from reviews.queries.books import (
    get_top_rated_books,
    get_top_selling_books,
    get_books_aggregate,
    get_book_by_id,
    get_reviews_by_book,
    get_sales_by_book,
    create_book,
    update_book,
    delete_book
)

db = Mongo().database
collection = db.object

def top_books(request):
    return render(request, 'top_books.html')

def top_rated_books(request):
    top_rated_books = get_top_rated_books()
    for book in top_rated_books:
        print(book)
        book['_id'] = str(book['_id'])
        book['author_id'] = str(book['author_id'])
        if book.get('highest_rated_review'):
            book['highest_rated_review']['_id'] = str(book['highest_rated_review']['_id'])
        if book.get('lowest_rated_review'):
            book['lowest_rated_review']['_id'] = str(book['lowest_rated_review']['_id'])

    response_data = {
        'top_rated_books': top_rated_books,
    }
    return JsonResponse(response_data)

def top_selling_books(request):
    top_selling_books = get_top_selling_books()
    for book in top_selling_books:
        book['_id'] = str(book['_id'])
        book['author_id'] = str(book['author_id'])

    response_data = {
        'top_selling_books': top_selling_books,
    }
    return JsonResponse(response_data)



def book_list(request):
    return render(request, 'books/book_list.html')

def book_data(request):
    page = int(request.GET.get('page', 1))
    name_filter = request.GET.get('name_filter', '')

    books = get_books_aggregate(page, name_filter)
    
    # Convert ObjectId to string
    for book in books:
        book['_id'] = str(book['_id'])
        book['author_id'] = str(book['author_id'])

    total_books = collection.aggregate([
        {
            "$unwind": "$books"
        },
        {
            "$match": {
                "books.name": { "$regex": name_filter, "$options": "i" }
            }
        },
        {
            "$count": "total"
        }
    ])

    total_books_count = next(total_books, {}).get('total', 0)
    num_pages = (total_books_count + 19) // 20  # Calculate number of pages

    response_data = {
        'books': books,
        'num_pages': num_pages,
        'current_page': page,
    }

    return JsonResponse(response_data, safe=False)

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
        author_id = ObjectId(request.POST.get('author_id_hidden'))
        book = {
            "name": request.POST.get('name'),
            "summary": request.POST.get('summary'),
            "date_of_publication": request.POST.get('date_of_publication'),
        }
        create_book(author_id, book)
        return redirect('book_list')
    
    authors = list(collection.find({}, {"_id": 1, "name": 1}))
    return render(request, 'books/book_form.html', {'authors': authors})


def book_create_for_author(request, author_id):
    if request.method == "POST":
        author_id = ObjectId(author_id)
        book = {
            "name": request.POST.get('name'),
            "summary": request.POST.get('summary'),
            "date_of_publication": request.POST.get('date_of_publication'),
        }
        create_book(author_id, book)
        return redirect('author_detail', pk=author_id)
    
    author = collection.find_one({"_id": ObjectId(author_id)}, {"_id": 1, "name": 1})
    return render(request, 'books/book_form.html', {'author': author})

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
    
    authors = list(collection.find({}, {"_id": 1, "name": 1}))
    print(book)
    return render(request, 'books/book_form.html', {'book': book, 'authors': authors})

def book_delete(request, pk):
    book = get_book_by_id(pk)
    if request.method == "POST":
        delete_book(pk)
        return redirect('book_list')
    return render(request, 'books/book_confirm_delete.html', {'book': book})
