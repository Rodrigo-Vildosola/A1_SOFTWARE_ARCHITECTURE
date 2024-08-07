from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    country_of_origin = models.CharField(max_length=255)
    short_description = models.TextField()

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=255)
    summary = models.TextField()
    date_of_publication = models.DateField()
    number_of_sales = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.name


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField()
    score = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    number_of_upvotes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.book.name} - {self.score}"


class SalesByYear(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='yearly_sales')
    year = models.IntegerField()
    sales = models.IntegerField()

    def __str__(self):
        return f"{self.book.name} - {self.year}"
