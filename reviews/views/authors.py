from django.shortcuts import render, redirect
from reviews.queries.authors import get_author_with_books_reviews_sales, get_author_by_id, create_author, delete_author, update_author
from reviews.utils import handle_uploaded_file
from django.http import HttpResponseNotFound, JsonResponse


def author_data(request):
    sort_by = request.GET.get('sort_by', 'name')
    order = request.GET.get('order', 'asc')
    page = int(request.GET.get('page', 1))
    name_filter = request.GET.get('name_filter', '')

    authors, num_pages = get_author_with_books_reviews_sales(page, sort_by, order, name_filter)

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


def author_list(request):
    return render(request, 'authors/author_list.html')


def author_detail(request, pk):
    author = get_author_by_id(pk, include_books=True)
    if not author:
        return HttpResponseNotFound("Author not found.")
    
    return render(request, 'authors/author_detail.html', {'author': author, 'books': author.get("books")})


def author_create(request):
    if request.method == "POST":
        image = request.FILES.get('image')
        image_url = None

        if image:
            image_url = handle_uploaded_file(image)

        author_data = {
            "name": request.POST.get('name'),
            "date_of_birth": request.POST.get('date_of_birth'),
            "country_of_origin": request.POST.get('country_of_origin'),
            "short_description": request.POST.get('short_description'),
            "image_url": image_url
        }

        if create_author(author_data):
            return redirect('author_list')
        return render(request, 'authors/author_form.html', {'error': 'An error occurred while creating the author.'})
    
    return render(request, 'authors/author_form.html')


def author_edit(request, pk):
    author = get_author_by_id(pk)
    if not author:
        return HttpResponseNotFound("Author not found.")
    
    if request.method == "POST":
        image = request.FILES.get('image')
        image_url = author.get('image_url')
        if image:
            image_url = handle_uploaded_file(image)

        updated_author = {
            "name": request.POST.get('name'),
            "date_of_birth": request.POST.get('date_of_birth'),
            "country_of_origin": request.POST.get('country_of_origin'),
            "short_description": request.POST.get('short_description'),
            "image_url": image_url
        }

        if update_author(pk, updated_author):
            return redirect('author_list')
        return render(request, 'authors/author_form.html', {'author': author, 'error': 'An error occurred while updating the author.'})
    
    return render(request, 'authors/author_form.html', {'author': author})


def author_delete(request, pk):
    author = get_author_by_id(pk)
    if not author:
        return HttpResponseNotFound("Author not found.")
    
    if request.method == "POST":
        if delete_author(pk):
            return redirect('author_list')
        return render(request, 'authors/author_confirm_delete.html', {'author': author, 'error': 'An error occurred while deleting the author.'})
    
    return render(request, 'authors/author_confirm_delete.html', {'author': author})
