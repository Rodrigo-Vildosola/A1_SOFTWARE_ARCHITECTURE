from mongoengine import Document, fields
from django.utils import timezone

class Author(Document):
    name = fields.StringField(max_length=255, required=True)
    date_of_birth = fields.DateField(required=True)
    country_of_origin = fields.StringField(max_length=255, required=True)
    short_description = fields.StringField()

    def __str__(self):
        return self.name

class Book(Document):
    name = fields.StringField(max_length=255, required=True)
    summary = fields.StringField()
    date_of_publication = fields.DateField(required=True)
    number_of_sales = fields.IntField()
    author = fields.ReferenceField(Author, reverse_delete_rule=fields.CASCADE)

    def __str__(self):
        return self.name

class Review(Document):
    book = fields.ReferenceField(Book, reverse_delete_rule=fields.CASCADE)
    review = fields.StringField()
    score = fields.IntField(choices=[1, 2, 3, 4, 5], required=True)
    number_of_upvotes = fields.IntField(default=0)

    def __str__(self):
        return f"{self.book.name} - {self.score}"

class SalesByYear(Document):
    book = fields.ReferenceField(Book, reverse_delete_rule=fields.CASCADE)
    year = fields.IntField(required=True)
    sales = fields.IntField(required=True)

    def __str__(self):
        return f"{self.book.name} - {self.year}"
