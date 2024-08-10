from django.shortcuts import render
from reviews.utils import search_books
from reviews.mongo import Mongo


db = Mongo().database

def home(request):
    return render(request, 'index.html')

def search_view(request):
    query = request.GET.get('query', '')
    page = int(request.GET.get('page', 1))
    books = search_books(query, page)
    return render(request, 'search_results.html', {'books': books, 'query': query, 'page': page})

def custom_404(request, exception):
    return render(request, '404.html', {'message': 'Page not found'}, status=404)
