from bson.objectid import ObjectId

class Author:
    def __init__(self, name, date_of_birth, country_of_origin, short_description, id=None):
        self.name = name
        self.date_of_birth = date_of_birth
        self.country_of_origin = country_of_origin
        self.short_description = short_description
        self.id = str(id) if id else None

    def serialize(self):
        data = {
            "name": self.name,
            "date_of_birth": self.date_of_birth,
            "country_of_origin": self.country_of_origin,
            "short_description": self.short_description
        }
        if self.id:
            data["_id"] = ObjectId(self.id)
        return data

    @staticmethod
    def deserialize(data):
        return Author(
            name=data.get("name"),
            date_of_birth=data.get("date_of_birth"),
            country_of_origin=data.get("country_of_origin"),
            short_description=data.get("short_description"),
            id=data.get("_id")
        )

class Book:
    def __init__(self, name, summary, date_of_publication, number_of_sales, author_id, id=None):
        self.name = name
        self.summary = summary
        self.date_of_publication = date_of_publication
        self.number_of_sales = number_of_sales
        self.author_id = str(author_id)
        self.id = str(id) if id else None

    def serialize(self):
        data = {
            "name": self.name,
            "summary": self.summary,
            "date_of_publication": self.date_of_publication,
            "number_of_sales": self.number_of_sales,
            "author_id": ObjectId(self.author_id)
        }
        if self.id:
            data["_id"] = ObjectId(self.id)
        return data

    @staticmethod
    def deserialize(data):
        return Book(
            name=data.get("name"),
            summary=data.get("summary"),
            date_of_publication=data.get("date_of_publication"),
            number_of_sales=data.get("number_of_sales"),
            author_id=data.get("author_id"),
            id=data.get("_id")
        )

class Review:
    def __init__(self, book_id, review, score, number_of_upvotes, id=None):
        self.book_id = str(book_id)
        self.review = review
        self.score = score
        self.number_of_upvotes = number_of_upvotes
        self.id = str(id) if id else None

    def serialize(self):
        data = {
            "book_id": ObjectId(self.book_id),
            "review": self.review,
            "score": self.score,
            "number_of_upvotes": self.number_of_upvotes
        }
        if self.id:
            data["_id"] = ObjectId(self.id)
        return data

    @staticmethod
    def deserialize(data):
        return Review(
            book_id=data.get("book_id"),
            review=data.get("review"),
            score=data.get("score"),
            number_of_upvotes=data.get("number_of_upvotes"),
            id=data.get("_id")
        )

class Sales:
    def __init__(self, book_id, year, sales, id=None):
        self.book_id = str(book_id)
        self.year = year
        self.sales = sales
        self.id = str(id) if id else None

    def serialize(self):
        data = {
            "book_id": ObjectId(self.book_id),
            "year": self.year,
            "sales": self.sales
        }
        if self.id:
            data["_id"] = ObjectId(self.id)
        return data

    @staticmethod
    def deserialize(data):
        return Sales(
            book_id=data.get("book_id"),
            year=data.get("year"),
            sales=data.get("sales"),
            id=data.get("_id")
        )
