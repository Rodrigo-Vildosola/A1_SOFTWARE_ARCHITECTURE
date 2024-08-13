from django.urls import path
from .views import (
    home, search_view,
    author_list, author_data, author_detail, author_create, author_edit, author_delete,
    top_books, top_rated_books, top_selling_books, book_list, book_data, book_detail, book_create, book_edit, book_delete,
    review_list, review_data, review_detail, review_create, review_edit, review_delete,
    sales_list, sales_data, sale_detail, sale_create, sale_edit, sale_delete
)

urlpatterns = [
    path('', home, name='home_page'),
    path('search/', search_view, name='search'),

    path('authors/', author_list, name='author_list'),
    path('authors/data/', author_data, name='author_data'),
    path('author/new/', author_create, name='author_create'),
    path('author/<str:pk>/edit/', author_edit, name='author_edit'),
    path('author/<str:pk>/delete/', author_delete, name='author_delete'),
    path('author/<str:pk>/', author_detail, name='author_detail'),

    path('books/', book_list, name='book_list'),
    path('books/data/', book_data, name='books_data'),
    path('book/new/', book_create, name='book_create'),
    path('book/<str:pk>/edit/', book_edit, name='book_edit'),
    path('book/<str:pk>/delete/', book_delete, name='book_delete'),
    path('book/<str:pk>/', book_detail, name='book_detail'),
    path('top-books/', top_books, name='top_books'),
    path('top-books/top-rated/', top_rated_books, name='top_rated_books'),
    path('top-books/top-selling/', top_selling_books, name='top_selling_books'),

    path('reviews/', review_list, name='review_list'),
    path('reviews/data/', review_data, name='review_data'),
    path('review/new/', review_create, name='review_create'),
    path('review/<str:pk>/edit/', review_edit, name='review_edit'),
    path('review/<str:pk>/delete/', review_delete, name='review_delete'),
    path('review/<str:pk>/', review_detail, name='review_detail'),

    path('sales/', sales_list, name='sales_list'),
    path('sales/data/', sales_data, name='sales_data'),
    path('sale/new/', sale_create, name='sale_create'),
    path('sale/<str:pk>/edit/', sale_edit, name='sale_edit'),
    path('sale/<str:pk>/delete/', sale_delete, name='sale_delete'),
    path('sale/<str:pk>/', sale_detail, name='sale_detail'),
]

