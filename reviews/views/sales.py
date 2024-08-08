from django.shortcuts import render, redirect
from bson.objectid import ObjectId
from reviews.utils import get_all
from reviews.mongo import Mongo

# MongoDB connection
db = Mongo().database
sales_collection = db['sales']
books_collection = db['books']

def get_all_sales():
    sales = []
    for data in sales_collection.find():
        data['id'] = str(data['_id'])
        sales.append(data)
    return sales

def sales_list(request):
    sales = list(sales_collection.find())
    return render(request, 'sales/sales_list.html', {'sales': sales})

def sale_detail(request, pk):
    data = sales_collection.find_one({"_id": ObjectId(pk)})
    return render(request, 'sales/sale_detail.html', {'sales': data})

def sale_create(request):
    if request.method == "POST":
        sales = {
            "book_id": ObjectId(request.POST.get('book_id')),
            "year": request.POST.get('year'),
            "sales": request.POST.get('sales')
        }
        sales_collection.insert_one(sales)
        return redirect('sales_list')
    books = list(books_collection.find())
    return render(request, 'sales/sale_form.html', {'books': books})

def sale_edit(request, pk):
    data = sales_collection.find_one({"_id": ObjectId(pk)})
    if request.method == "POST":
        updated_sales = {
            "book_id": ObjectId(request.POST.get('book_id')),
            "year": request.POST.get('year'),
            "sales": request.POST.get('sales')
        }
        sales_collection.update_one({'_id': ObjectId(pk)}, {'$set': updated_sales})
        return redirect('sales_list')
    books = list(books_collection.find())
    return render(request, 'sales/sale_form.html', {'sales': data, 'books': books})

def sale_delete(request, pk):
    data = sales_collection.find_one({"_id": ObjectId(pk)})
    if request.method == "POST":
        sales_collection.delete_one({'_id': ObjectId(pk)})
        return redirect('sales_list')
    return render(request, 'sales/sale_confirm_delete.html', {'sales': data})
