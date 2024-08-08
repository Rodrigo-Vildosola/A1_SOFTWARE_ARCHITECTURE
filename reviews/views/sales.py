from django.shortcuts import render, redirect
from reviews.utils import sales_collection, books_collection
from bson.objectid import ObjectId
from reviews.queries.sales import get_all_sales, get_sale_by_id

def sales_list(request):
    sales = get_all_sales()
    return render(request, 'sales/sale_list.html', {'sales': sales})

def sale_detail(request, pk):
    sale = get_sale_by_id(pk)
    return render(request, 'sales/sale_detail.html', {'sale': sale})

def sale_create(request):
    if request.method == "POST":
        sale = {
            "book_id": ObjectId(request.POST.get('book_id')),
            "year": request.POST.get('year'),
            "sales": int(request.POST.get('sales'))
        }
        sales_collection.insert_one(sale)
        return redirect('sales_list')
    books = list(books_collection.find())
    return render(request, 'sales/sale_form.html', {'books': books})

def sale_edit(request, pk):
    sale = get_sale_by_id(pk)
    if request.method == "POST":
        updated_sale = {
            "book_id": ObjectId(request.POST.get('book_id')),
            "year": request.POST.get('year'),
            "sales": int(request.POST.get('sales'))
        }
        sales_collection.update_one({'_id': ObjectId(pk)}, {'$set': updated_sale})
        return redirect('sales_list')
    books = list(books_collection.find())
    return render(request, 'sales/sale_form.html', {'sale': sale, 'books': books})

def sale_delete(request, pk):
    sale = get_sale_by_id(pk)
    if request.method == "POST":
        sales_collection.delete_one({'_id': ObjectId(pk)})
        return redirect('sales_list')
    return render(request, 'sales/sale_confirm_delete.html', {'sale': sale})
