from data.db_session import *
from data.authors import Author
from data.series import Series
from data.books import Book


class DataController:
    def __init__(self, db_file):
        global_init(db_file)
        self.session = create_session()

    def add_author(self, name):
        author = Author()

        author.name = name

        self.session.add(author)
        self.session.commit()

    def add_series(self, name):
        series = Series()

        series.name = name

        self.session.add(series)
        self.session.commit()

    def add_book(self, name, description, author_id, price, cover_width, cover_height, short_name='', series_id=-1):
        book = Book()

        book.name = name
        book.short_name = short_name
        book.description = description
        book.author_id = author_id
        book.series_id = series_id
        book.price = price
        book.cover_width = cover_width
        book.cover_height = cover_height

        self.session.add(book)
        self.session.commit()

    def get_author(self, id):
        return self.session.query(Author).get(id)

    def get_book(self, id):
        return self.session.query(Book).get(id)

    def get_books(self):
        return self.session.query(Book).all()
    
    def get_series(self, id):
        return self.session.query(Series).get(id)
