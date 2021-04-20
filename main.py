import config
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
dc.add_author('Милена Завойчинская')
dc.add_author('Джоан Роулинг')
dc.add_series('Высшая Школа Библиотекарей')
dc.add_series('Гарри Поттер')
dc.add_book('Магия книгоходцев', 1, 317, 500, series=1)
dc.add_book('Боевая практика книгоходцев', 1, 317, 500, series=1)
dc.add_book('Книгоходцы особого назначения', 1, 317, 500, series=1)
dc.add_book('Книгоходцы и тайна механического бога', 1, 317, 500, series=1)
dc.add_book('Хроники книгоходцев', 1, 317, 500, series=1)
dc.add_book('Гарри Поттер и философский камень', 2, 333, 500, series=2)
dc.add_book('Гарри Поттер и Тайная комната', 2, 333, 500, series=2)
dc.add_book('Гарри Поттер и узник Азкабана', 2, 333, 500, series=2)
dc.add_book('Гарри Поттер и Кубок огня', 2, 333, 500, series=2)
dc.add_book('Гарри Поттер и Орден Феникса', 2, 333, 500, series=2)
dc.add_book('Гарри Поттер и Принц-полукровка', 2, 333, 500, series=2)
dc.add_book('Гарри Поттер и Дары Смерти', 2, 333, 500, series=2)


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


if __name__ == '__main__':
    db_session.global_init("db/books.db")
    app.run(port=config.PORT, host=config.HOST)
