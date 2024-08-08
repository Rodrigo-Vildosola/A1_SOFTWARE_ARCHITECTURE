import random
import argparse
from faker import Faker
from pymongo import MongoClient
from bson import ObjectId
from decouple import config

# Conexión a MongoDB
mongo_instance = MongoClient(config('MONGODB_URI'))
db = mongo_instance[config('DB_NAME')]

# Inicializando Faker
fake = Faker()

def reset_database():
    db.authors.delete_many({})
    db.books.delete_many({})
    db.reviews.delete_many({})
    db.sales.delete_many({})
    print("Database reset completado con éxito!")

def database_is_empty():
    return (
        db.authors.estimated_document_count() == 0 and
        db.books.estimated_document_count() == 0 and
        db.reviews.estimated_document_count() == 0 and
        db.sales.estimated_document_count() == 0
    )

def generate_seeds():
    # Crear autores primero
    authors = []
    for _ in range(50):
        author = {
            "name": fake.name(),
            "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=70).isoformat(),
            "country_of_origin": fake.country(),
            "short_description": fake.text(max_nb_chars=200)
        }
        authors.append(author)
    author_ids = db.authors.insert_many(authors).inserted_ids

    # Luego crear libros usando los autores creados
    books = []
    for _ in range(300):
        author_id = random.choice(author_ids)
        book = {
            "name": fake.sentence(nb_words=4),
            "summary": fake.text(max_nb_chars=500),
            "date_of_publication": fake.date_this_century().isoformat(),
            "author_id": author_id
        }
        books.append(book)
    book_ids = db.books.insert_many(books).inserted_ids

    # Finalmente, crear reseñas y ventas
    reviews = []
    sales = []
    for book_id in book_ids:
        for _ in range(random.randint(1, 10)):
            review = {
                "book_id": book_id,
                "review": fake.sentence(nb_words=10),
                "score": random.randint(1, 5),
                "number_of_upvotes": random.randint(0, 500)
            }
            reviews.append(review)

        first_year = random.randint(2000, 2019)
        for year in range(first_year, first_year + 5):
            sale = {
                "book_id": book_id,
                "year": year,
                "sales": random.randint(100, 10000)
            }
            sales.append(sale)
    
    db.reviews.insert_many(reviews)
    db.sales.insert_many(sales)
    
    print("Seeding completado con éxito!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed the database with fake data.")
    parser.add_argument('--reset', action='store_true', help="Reset the database before seeding.")
    parser.add_argument('--force', action='store_true', help="Force seeding even if the database is not empty.")

    args = parser.parse_args()

    if args.reset:
        reset_database()
        generate_seeds()
    elif args.force:
        generate_seeds()
    else:
        if database_is_empty():
            generate_seeds()
        else:
            print("Database is not empty. Use --reset to reset the database or --force to seed anyway.")
