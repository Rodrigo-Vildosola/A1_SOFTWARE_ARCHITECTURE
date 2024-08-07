from django.urls import path
from . import views

urlpatterns = [
    path('authors/', views.author_list, name='author_list'),
    path('author/<str:pk>/', views.author_detail, name='author_detail'),
    path('author/new/', views.author_create, name='author_create'),
    path('author/<str:pk>/edit/', views.author_edit, name='author_edit'),
    path('author/<str:pk>/delete/', views.author_delete, name='author_delete'),
    path('books/', views.book_list, name='book_list'),
    path('book/<str:pk>/', views.book_detail, name='book_detail'),
    path('book/new/', views.book_create, name='book_create'),
    path('book/<str:pk>/edit/', views.book_edit, name='book_edit'),
    path('book/<str:pk>/delete/', views.book_delete, name='book_delete'),
    path('reviews/', views.review_list, name='review_list'),
    path('review/<str:pk>/', views.review_detail, name='review_detail'),
    path('review/new/', views.review_create, name='review_create'),
    path('review/<str:pk>/edit/', views.review_edit, name='review_edit'),
    path('review/<str:pk>/delete/', views.review_delete, name='review_delete'),
    path('salesbyyear/', views.salesbyyear_list, name='salesbyyear_list'),
    path('salesbyyear/<str:pk>/', views.salesbyyear_detail, name='salesbyyear_detail'),
    path('salesbyyear/new/', views.salesbyyear_create, name='salesbyyear_create'),
    path('salesbyyear/<str:pk>/edit/', views.salesbyyear_edit, name='salesbyyear_edit'),
    path('salesbyyear/<str:pk>/delete/', views.salesbyyear_delete, name='salesbyyear_delete'),
]
