import random
from faker import Faker
from pymongo import MongoClient
from decouple import config
from reviews.types import Author, Book, Review, Sales

# Conexión a MongoDB
mongo_instance = MongoClient(config('MONGODB_URI'))
db = mongo_instance[config('DB_NAME')]

# Inicializando Faker
fake = Faker()

def generate_seeds():
    # Crear autores primero
    authors = []
    for _ in range(50):
        author = Author(
            name=fake.name(),
            date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=70).isoformat(),
            country_of_origin=fake.country(),
            short_description=fake.text(max_nb_chars=200)
        )
        authors.append(author.serialize())
    author_ids = db.authors.insert_many(authors).inserted_ids

    # Luego crear libros usando los autores creados
    books = []
    for _ in range(300):
        author_id = random.choice(author_ids)
        book = Book(
            name=fake.sentence(nb_words=4),
            summary=fake.text(max_nb_chars=500),
            date_of_publication=fake.date_this_century().isoformat(),
            number_of_sales=random.randint(1000, 100000),
            author_id=str(author_id)
        )
        books.append(book.serialize())
    book_ids = db.books.insert_many(books).inserted_ids

    # Finalmente, crear reseñas y ventas
    reviews = []
    sales = []
    for book_id in book_ids:
        for _ in range(random.randint(1, 10)):
            review = Review(
                book_id=str(book_id),
                review=fake.text(max_nb_chars=300),
                score=random.randint(1, 5),
                number_of_upvotes=random.randint(0, 500)
            )
            reviews.append(review.serialize())

        first_year = random.randint(2000, 2019)
        for year in range(first_year, first_year + 5):
            sale = Sales(
                book_id=str(book_id),
                year=year,
                sales=random.randint(100, 10000)
            )
            sales.append(sale.serialize())
    
    db.reviews.insert_many(reviews)
    db.sales.insert_many(sales)
    
    print("Seeding completado con éxito!")

if __name__ == "__main__":
    generate_seeds()
