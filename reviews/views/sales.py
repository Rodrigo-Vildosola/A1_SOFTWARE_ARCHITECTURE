from django.shortcuts import render, redirect
from bson.objectid import ObjectId
from decouple import config
import pymongo

# MongoDB connection
client = pymongo.MongoClient(config('MONGODB_URI'))
db = client[config('DB_NAME')]
sales_collection = db['sales']
books_collection = db['books']

def get_all(collection):
    collection_data = []
    for i in collection.find():
        i['id'] = str(i['_id'])
        collection_data.append(i)
    return collection_data

def sales_list(request):
    sales = get_all(sales_collection)
    return render(request, 'reviews/sales_list.html', {'sales': sales})

def sale_detail(request, pk):
    sales = sales_collection.find_one({"_id": ObjectId(pk)})
    sales['id'] = str(sales['_id'])
    return render(request, 'reviews/sale_detail.html', {'sales': sales})

def sale_create(request):
    if request.method == "POST":
        book_id = request.POST.get('book_id')
        year = request.POST.get('year')
        sales = request.POST.get('sales')
        sales_record = {
            "book_id": ObjectId(book_id),
            "year": year,
            "sales": sales
        }
        sales_collection.insert_one(sales_record)
        return redirect('sales_list')
    books = get_all(books_collection)
    return render(request, 'reviews/sale_form.html', {'books': books})

def sale_edit(request, pk):
    sales = sales_collection.find_one({"_id": ObjectId(pk)})
    if request.method == "POST":
        updated_data = {
            "book_id": ObjectId(request.POST.get('book_id')),
            "year": request.POST.get('year'),
            "sales": request.POST.get('sales')
        }
        sales_collection.update_one({'_id': ObjectId(pk)}, {'$set': updated_data})
        return redirect('sales_list')
    sales['id'] = str(sales['_id'])
    books = get_all(books_collection)
    return render(request, 'reviews/sale_form.html', {'sales': sales, 'books': books})

def sale_delete(request, pk):
    sales = sales_collection.find_one({"_id": ObjectId(pk)})
    if request.method == "POST":
        sales_collection.delete_one({'_id': ObjectId(pk)})
        return redirect('sales_list')
    sales['id'] = str(sales['_id'])
    return render(request, 'reviews/sale_confirm_delete.html', {'sales': sales})
