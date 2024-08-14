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
    db.object.delete_many({})
    print("Database reset completado con éxito!")

def database_is_empty():
    return db.object.estimated_document_count() == 0

def generate_seeds():
    # Crear autores con libros, reseñas y ventas
    authors = []
    for _ in range(50):
        books = []
        for _ in range(random.randint(1, 10)):
            reviews = []
            sales = []
            for _ in range(random.randint(1, 10)):
                review = {
                    "_id": ObjectId(),
                    "review": fake.sentence(nb_words=10),
                    "score": random.randint(1, 5),
                    "number_of_upvotes": random.randint(0, 500)
                }
                reviews.append(review)

            first_year = random.randint(2000, 2019)
            for year in range(first_year, first_year + 5):
                sale = {
                    "_id": ObjectId(),
                    "year": year,
                    "sales": random.randint(100, 10000)
                }
                sales.append(sale)

            book = {
                "_id": ObjectId(),
                "name": fake.sentence(nb_words=4),
                "summary": fake.text(max_nb_chars=500),
                "date_of_publication": fake.date_this_century().isoformat(),
                "reviews": reviews,
                "sales": sales
            }
            books.append(book)

        author = {
            "_id": ObjectId(),
            "name": fake.name(),
            "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=70).isoformat(),
            "country_of_origin": fake.country(),
            "short_description": fake.text(max_nb_chars=200),
            "books": books
        }
        authors.append(author)
    
    db.object.insert_many(authors)
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
