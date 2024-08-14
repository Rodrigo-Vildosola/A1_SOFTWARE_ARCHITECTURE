from django.shortcuts import render, redirect
from bson.objectid import ObjectId
from reviews.queries.authors import get_author_with_books_reviews_sales, get_books_by_author
from reviews.utils import collection

from django.http import HttpResponseNotFound, JsonResponse




def get_author_by_id(pk, include_books=False):
    try:
        match_stage = {"$match": {"_id": ObjectId(pk)}}
        project_stage = {
            "$project": {
                "_id": 1,
                "name": 1,
                "date_of_birth": 1,
                "country_of_origin": 1,
                "short_description": 1,
                "books": {"$cond": {"if": include_books, "then": "$books", "else": "$$REMOVE"}}
            }
        }

        pipeline = [match_stage, project_stage]

        author = collection.aggregate(pipeline).next()
        if not author:
            return None
        
        # author['_id'] = str(author['_id'])
        # if include_books and 'books' in author:
        #     for book in author['books']:
        #         book['_id'] = str(book['_id'])
        return author
    except StopIteration:
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def author_list(request):
    return render(request, 'authors/author_list.html')

def author_data(request):
    sort_by = request.GET.get('sort_by', 'name')
    order = request.GET.get('order', 'asc')
    page = int(request.GET.get('page', 1))
    name_filter = request.GET.get('name_filter', '')

    authors, num_pages = get_author_with_books_reviews_sales(page, sort_by, order, name_filter)

    # Convert ObjectId to string
    for author in authors:
        author['_id'] = str(author['_id'])

    response_data = {
        'authors': authors,
        'num_pages': num_pages,
        'current_page': page,
        'sort_by': sort_by,
        'order': order,
    }

    return JsonResponse(response_data, safe=False)


def author_detail(request, pk):
    author = get_author_by_id(pk, include_books=True)
    if not author:
        return HttpResponseNotFound("Author not found.")
    return render(request, 'authors/author_detail.html', {'author': author, 'books': author.get("books")})

def author_create(request):
    if request.method == "POST":
        author = {
            "name": request.POST.get('name'),
            "date_of_birth": request.POST.get('date_of_birth'),
            "country_of_origin": request.POST.get('country_of_origin'),
            "short_description": request.POST.get('short_description')
        }
        try:
            collection.insert_one(author)
            return redirect('author_list')
        except Exception as e:
            print(f"An error occurred: {e}")
            return render(request, 'authors/author_form.html', {'error': 'An error occurred while creating the author.'})
    return render(request, 'authors/author_form.html')

def author_edit(request, pk):
    author = get_author_by_id(pk)
    if not author:
        return HttpResponseNotFound("Author not found.")
    if request.method == "POST":
        updated_author = {
            "name": request.POST.get('name'),
            "date_of_birth": request.POST.get('date_of_birth'),
            "country_of_origin": request.POST.get('country_of_origin'),
            "short_description": request.POST.get('short_description')
        }
        try:
            collection.update_one({'_id': ObjectId(pk)}, {'$set': updated_author})
            return redirect('author_list')
        except Exception as e:
            print(f"An error occurred: {e}")
            return render(request, 'authors/author_form.html', {'author': author, 'error': 'An error occurred while updating the author.'})
    
    return render(request, 'authors/author_form.html', {'author': author})

def author_delete(request, pk):
    author = get_author_by_id(pk)
    if not author:
        return HttpResponseNotFound("Author not found.")
    
    if request.method == "POST":
        try:
            collection.delete_one({'_id': ObjectId(pk)})
            return redirect('author_list')
        except Exception as e:
            print(f"An error occurred: {e}")
            return render(request, 'authors/author_confirm_delete.html', {'author': author, 'error': 'An error occurred while deleting the author.'})
    
    return render(request, 'authors/author_confirm_delete.html', {'author': author})
