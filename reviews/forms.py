from django import forms
from .models import Author, Book, Review, SalesByYear

class AuthorForm(forms.Form):
    name = forms.CharField(max_length=255)
    date_of_birth = forms.DateField()
    country_of_origin = forms.CharField(max_length=255)
    short_description = forms.CharField(widget=forms.Textarea)

    def save(self, commit=True):
        data = self.cleaned_data
        author = Author(**data)
        if commit:
            author.save()
        return author

class BookForm(forms.Form):
    name = forms.CharField(max_length=255)
    summary = forms.CharField(widget=forms.Textarea)
    date_of_publication = forms.DateField()
    number_of_sales = forms.IntegerField()
    author = forms.ModelChoiceField(queryset=Author.objects.all())

    def save(self, commit=True):
        data = self.cleaned_data
        book = Book(**data)
        if commit:
            book.save()
        return book

class ReviewForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Book.objects.all())
    review = forms.CharField(widget=forms.Textarea)
    score = forms.IntegerField(min_value=1, max_value=5)
    number_of_upvotes = forms.IntegerField()

    def save(self, commit=True):
        data = self.cleaned_data
        review = Review(**data)
        if commit:
            review.save()
        return review

class SalesByYearForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Book.objects.all())
    year = forms.IntegerField()
    sales = forms.IntegerField()

    def save(self, commit=True):
        data = self.cleaned_data
        sales_by_year = SalesByYear(**data)
        if commit:
            sales_by_year.save()
        return sales_by_year
