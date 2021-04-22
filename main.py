import config
from utils import *
from sections import *
from controllers import *
from flask import Flask, render_template
from data import db_session

app = Flask(
    __name__,
    template_folder=config.TEMPLATE_FOLDER,
    static_folder=config.STATIC_FOLDER
)

app.config['SECRET_KEY'] = config.SECRET_KEY

dc = DataController('db/books.db')
# dc.add_author('Милена Завойчинская')
# dc.add_author('Джоан Роулинг')
# dc.add_series('Высшая Школа Библиотекарей')
# dc.add_series('Гарри Поттер')
# dc.add_book('Высшая Школа Библиотекарей. Магия книгоходцев', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur in feugiat lacus, at scelerisque orci. Etiam dictum condimentum pulvinar. Aenean sollicitudin dignissim lorem non fermentum. Nam semper ligula sed pretium pharetra. Pellentesque tempus pretium fringilla. Proin nec mi sit amet velit dapibus tincidunt at vitae enim. Vestibulum consectetur dolor ut dui ultrices lobortis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Praesent porttitor leo eget ligula malesuada, tempor vehicula lacus vehicula. Donec id ipsum et ipsum dignissim condimentum. Fusce ultricies ullamcorper lacus sit amet pretium.', 1, 169, 317, 500, series_id=1, short_name='Магия книгоходцев')
# dc.add_book('Высшая Школа Библиотекарей. Боевая практика книгоходцев', 'Описание', 1, 199.99, 317, 500, series_id=1, short_name='Боевая практика книгоходцев')
# dc.add_book('Высшая Школа Библиотекарей. Книгоходцы особого назначения', 'Описание', 1, 200, 317, 500, series_id=1, short_name='Книгоходцы особого назначения')
# dc.add_book('Высшая Школа Библиотекарей. Книгоходцы и тайна механического бога', 'Описание', 1, 500, 317, 500, series_id=1, short_name='Книгоходцы и тайна механического бога')
# dc.add_book('Высшая Школа Библиотекарей. Хроники книгоходцев', 'Описание', 1, 100, 317, 500, series_id=1, short_name='Хроники книгоходцев')
# dc.add_book('Гарри Поттер и философский камень', 'Описание', 2, 500, 333, 500, series_id=2)
# dc.add_book('Гарри Поттер и Тайная комната', 'Описание', 2, 299.99, 333, 500, series_id=2)
# dc.add_book('Гарри Поттер и узник Азкабана', 'Описание', 2, 560, 333, 500, series_id=2)
# dc.add_book('Гарри Поттер и Кубок огня', 'Описание', 2, 290, 333, 500, series_id=2)
# dc.add_book('Гарри Поттер и Орден Феникса', 'Описание', 2, 315, 333, 500, series_id=2)
# dc.add_book('Гарри Поттер и Принц-полукровка', 'Описание', 2, 500, 333, 500, series_id=2)
# dc.add_book('Гарри Поттер и Дары Смерти', 'Описание', 2, 500, 333, 500, series_id=2)


@app.route('/')
def index():
    sections = []

    sections.append(
        BookSection(dc, dc.get_books())
    )

    return render_template(
        'index.html',
        sections=sections
    )


@app.route('/book/<int:book_id>')
def book(book_id):
    book = dc.get_book(book_id)
    data = {
        'book': book,
        'author': dc.get_author(book.author_id),
        'series': dc.get_series(book.series_id),
        'price': str(
            int(book.price)
            if int(book.price) == book.price else
            book.price
        ) + ' ' + plural(
            book.price, 'рубль', 'рубля', 'рублей'
        )
    }

    return render_template(
        'book.html',
        **data
    )


@app.route('/author/<int:author_id>')
def author(author_id):
    author = dc.get_author(author_id)
    data = {
        'author_id': str(author.id),
        'author_name': author.name
    }

    return render_template(
        'author.html',
        **data
    )


@app.route('/series/<int:series_id>')
def series(series_id):
    series = dc.get_series(series_id)
    data = {
        'author_id': str(series.id),
        'author_name': series.name
    }

    return render_template(
        'author.html',
        **data
    )


if __name__ == '__main__':
    db_session.global_init("db/books.db")
    app.run(port=config.PORT, host=config.HOST)
