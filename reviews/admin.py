from django.contrib import admin
from .models import Author, Book, Review, SalesByYear

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(SalesByYear)
