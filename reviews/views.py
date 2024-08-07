from django.shortcuts import render, get_object_or_404, redirect
from .models import Author, Book, Review, SalesByYear
from .forms import AuthorForm, BookForm, ReviewForm, SalesByYearForm

# Author Views
def author_list(request):
    authors = Author.objects.all()
    return render(request, 'reviews/author_list.html', {'authors': authors})

def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(request, 'reviews/author_detail.html', {'author': author})

def author_create(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm()
    return render(request, 'reviews/author_form.html', {'form': form})

def author_edit(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm(instance=author)
    return render(request, 'reviews/author_form.html', {'form': form})

def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == "POST":
        author.delete()
        return redirect('author_list')
    return render(request, 'reviews/author_confirm_delete.html', {'author': author})


# Book Views
def book_list(request):
    books = Book.objects.all()
    return render(request, 'reviews/book_list.html', {'books': books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'reviews/book_detail.html', {'book': book})

def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'reviews/book_form.html', {'form': form})

def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'reviews/book_form.html', {'form': form})

def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('book_list')
    return render(request, 'reviews/book_confirm_delete.html', {'book': book})


# Review Views
def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    return render(request, 'reviews/review_detail.html', {'review': review})

def review_create(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('review_list')
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_form.html', {'form': form})

def review_edit(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('review_list')
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/review_form.html', {'form': form})

def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == "POST":
        review.delete()
        return redirect('review_list')
    return render(request, 'reviews/review_confirm_delete.html', {'review': review})


# SalesByYear Views
def salesbyyear_list(request):
    sales = SalesByYear.objects.all()
    return render(request, 'reviews/salesbyyear_list.html', {'sales': sales})

def salesbyyear_detail(request, pk):
    sales = get_object_or_404(SalesByYear, pk=pk)
    return render(request, 'reviews/salesbyyear_detail.html', {'sales': sales})

def salesbyyear_create(request):
    if request.method == "POST":
        form = SalesByYearForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('salesbyyear_list')
    else:
        form = SalesByYearForm()
    return render(request, 'reviews/salesbyyear_form.html', {'form': form})

def salesbyyear_edit(request, pk):
    sales = get_object_or_404(SalesByYear, pk=pk)
    if request.method == "POST":
        form = SalesByYearForm(request.POST, instance=sales)
        if form.is_valid():
            form.save()
            return redirect('salesbyyear_list')
    else:
        form = SalesByYearForm(instance=sales)
    return render(request, 'reviews/salesbyyear_form.html', {'form': form})

def salesbyyear_delete(request, pk):
    sales = get_object_or_404(SalesByYear, pk=pk)
    if request.method == "POST":
        sales.delete()
        return redirect('salesbyyear_list')
    return render(request, 'reviews/salesbyyear_confirm_delete.html', {'sales': sales})
