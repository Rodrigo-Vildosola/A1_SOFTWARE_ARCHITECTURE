from django import forms
from .models import Author, Book, Review, SalesByYear

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'


class SalesByYearForm(forms.ModelForm):
    class Meta:
        model = SalesByYear
        fields = '__all__'
