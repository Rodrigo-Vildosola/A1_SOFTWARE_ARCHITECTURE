from django.http import JsonResponse
from django.shortcuts import render, redirect
from bson.objectid import ObjectId
from reviews.queries.sales import get_all_sales, get_sale_by_id, create_sale, update_sale, delete_sale
from reviews.utils import collection

def sales_list(request):
    return render(request, 'sales/sale_list.html')

def sales_data(request):
    page = int(request.GET.get('page', 1))
    name_filter = request.GET.get('name_filter', '')

    sales, total_sales_count = get_all_sales(page, name_filter)

    for sale in sales:
        sale['_id'] = str(sale['_id'])
        sale['book_id'] = str(sale['book_id'])

    response_data = {
        'sales': sales,
        'num_pages': (total_sales_count + 19) // 20,  # Calculate number of pages
        'current_page': page,
    }

    return JsonResponse(response_data)


def sale_detail(request, pk):
    sale = get_sale_by_id(pk)
    if sale: 
        return render(request, 'sales/sale_detail.html', {'sale': sale})
    else:
        return render(request, '404.html', {'message': 'Sale not found'})

def sale_create(request):
    if request.method == "POST":
        book_id = ObjectId(request.POST.get('book_id'))
        sale = {
            "year": int(request.POST.get('year')),
            "sales": int(request.POST.get('sales'))
        }
        create_sale(book_id, sale)
        return redirect('sales_list')
    
    # Fetch only necessary fields (name and id) to avoid loading too much data
    books = list(collection.aggregate([
        {"$unwind": "$books"},
        {"$project": {"_id": "$books._id", "name": "$books.name"}}
    ]))
    return render(request, 'sales/sale_form.html', {'books': books})

def sale_create_for_book(request, book_id):
    if request.method == "POST":
        book_id = ObjectId(book_id)
        sale = {
            "year": int(request.POST.get('year')),
            "sales": int(request.POST.get('sales'))
        }
        create_sale(book_id, sale)
        return redirect('sales_list')
    
    # Fetch only necessary fields (name and id) to avoid loading too much data
    books = list(collection.aggregate([
        {"$unwind": "$books"},
        {"$project": {"_id": "$books._id", "name": "$books.name"}}
    ]))
    return render(request, 'sales/sale_form.html', {'books': books})


def sale_edit(request, pk):
    sale = get_sale_by_id(pk)
    if request.method == "POST":
        updated_sale = {
            "year": int(request.POST.get('year')),
            "sales": int(request.POST.get('sales'))
        }
        update_sale(pk, updated_sale)
        return redirect('sales_list')
    
    # Fetch only necessary fields (name and id) to avoid loading too much data
    books = list(collection.aggregate([
        {"$unwind": "$books"},
        {"$project": {"_id": "$books._id", "name": "$books.name"}}
    ]))
    return render(request, 'sales/sale_form.html', {'sale': sale, 'books': books})

def sale_delete(request, pk):
    sale = get_sale_by_id(pk)
    if request.method == "POST":
        delete_sale(pk)
        return redirect('sales_list')
    return render(request, 'sales/sale_confirm_delete.html', {'sale': sale})
