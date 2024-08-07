from django.urls import path
from .views import (
    home,
    author_list, author_detail, author_create, author_edit, author_delete,
    book_list, book_detail, book_create, book_edit, book_delete,
    review_list, review_detail, review_create, review_edit, review_delete,
    sales_list, sale_detail, sale_create, sale_edit, sale_delete
)

urlpatterns = [
    path('', home, name='home_page'),
    
    path('authors/', author_list, name='author_list'),
    path('author/new/', author_create, name='author_create'),
    path('author/<str:pk>/edit/', author_edit, name='author_edit'),
    path('author/<str:pk>/delete/', author_delete, name='author_delete'),
    path('author/<str:pk>/', author_detail, name='author_detail'),

    path('books/', book_list, name='book_list'),
    path('book/new/', book_create, name='book_create'),
    path('book/<str:pk>/edit/', book_edit, name='book_edit'),
    path('book/<str:pk>/delete/', book_delete, name='book_delete'),
    path('book/<str:pk>/', book_detail, name='book_detail'),

    path('reviews/', review_list, name='review_list'),
    path('review/new/', review_create, name='review_create'),
    path('review/<str:pk>/edit/', review_edit, name='review_edit'),
    path('review/<str:pk>/delete/', review_delete, name='review_delete'),
    path('review/<str:pk>/', review_detail, name='review_detail'),

    path('sales/', sales_list, name='sales_list'),
    path('sales/new/', sale_create, name='sales_create'),
    path('sales/<str:pk>/edit/', sale_edit, name='sales_edit'),
    path('sales/<str:pk>/delete/', sale_delete, name='sales_delete'),
    path('sales/<str:pk>/', sale_detail, name='sales_detail'),
]
