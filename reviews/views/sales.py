from django.shortcuts import render, redirect
from decouple import config
from bson.objectid import ObjectId
import pymongo
from reviews.types import Sales
from reviews.utils import get_all

# MongoDB connection
client = pymongo.MongoClient(config('MONGODB_URI'))
db = client[config('DB_NAME')]
sales_collection = db['sales']
books_collection = db['books']

def get_all_sales():
    sales = []
    for data in sales_collection.find():
        sales.append(Sales.deserialize(data))
    return sales

def sales_list(request):
    sales = get_all_sales()
    return render(request, 'reviews/sales_list.html', {'sales': sales})

def sale_detail(request, pk):
    data = sales_collection.find_one({"_id": ObjectId(pk)})
    sales = Sales.deserialize(data)
    return render(request, 'reviews/sale_detail.html', {'sales': sales})

def sale_create(request):
    if request.method == "POST":
        sales = Sales(
            book_id=request.POST.get('book_id'),
            year=request.POST.get('year'),
            sales=request.POST.get('sales')
        )
        sales_collection.insert_one(sales.serialize())
        return redirect('sales_list')
    books = get_all(books_collection)
    return render(request, 'reviews/sale_form.html', {'books': books})

def sale_edit(request, pk):
    data = sales_collection.find_one({"_id": ObjectId(pk)})
    sales = Sales.deserialize(data)
    if request.method == "POST":
        updated_sales = Sales(
            book_id=request.POST.get('book_id'),
            year=request.POST.get('year'),
            sales=request.POST.get('sales'),
            id=pk
        )
        sales_collection.update_one({'_id': ObjectId(pk)}, {'$set': updated_sales.serialize()})
        return redirect('sales_list')
    books = get_all(books_collection)
    return render(request, 'reviews/sale_form.html', {'sales': sales, 'books': books})

def sale_delete(request, pk):
    data = sales_collection.find_one({"_id": ObjectId(pk)})
    sales = Sales.deserialize(data)
    if request.method == "POST":
        sales_collection.delete_one({'_id': ObjectId(pk)})
        return redirect('sales_list')
    return render(request, 'reviews/sale_confirm_delete.html', {'sales': sales})
