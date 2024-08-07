from django.urls import path
from . import views

urlpatterns = [
    path('authors/', views.author_list, name='author_list'),
    path('author/<int:pk>/', views.author_detail, name='author_detail'),
    path('author/new/', views.author_create, name='author_create'),
    path('author/<int:pk>/edit/', views.author_edit, name='author_edit'),
    path('author/<int:pk>/delete/', views.author_delete, name='author_delete'),
    path('books/', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/new/', views.book_create, name='book_create'),
    path('book/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('reviews/', views.review_list, name='review_list'),
    path('review/<int:pk>/', views.review_detail, name='review_detail'),
    path('review/new/', views.review_create, name='review_create'),
    path('review/<int:pk>/edit/', views.review_edit, name='review_edit'),
    path('review/<int:pk>/delete/', views.review_delete, name='review_delete'),
    path('salesbyyear/', views.salesbyyear_list, name='salesbyyear_list'),
    path('salesbyyear/<int:pk>/', views.salesbyyear_detail, name='salesbyyear_detail'),
    path('salesbyyear/new/', views.salesbyyear_create, name='salesbyyear_create'),
    path('salesbyyear/<int:pk>/edit/', views.salesbyyear_edit, name='salesbyyear_edit'),
    path('salesbyyear/<int:pk>/delete/', views.salesbyyear_delete, name='salesbyyear_delete'),
]
