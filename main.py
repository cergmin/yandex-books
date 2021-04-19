import config
from sections import *
from controllers import *
from flask import Flask, render_template

app = Flask(
    __name__,
    template_folder=config.TEMPLATE_FOLDER,
    static_folder=config.STATIC_FOLDER
)

dc = DataController()


@app.route('/')
def index():
    sections = []

    sections.append(
        BookSection([
            {
                'book_id': 9,
                'book_name': 'Гарри Поттер и философский камень',
                'author_id': 2,
                'author_name': 'Джоан Роулинг',
                'cover_width': 333,
                'cover_height': 500
            },
            {
                'book_id': 10,
                'book_name': 'Гарри Поттер и Тайная комната',
                'author_id': 2,
                'author_name': 'Джоан Роулинг',
                'cover_width': 333,
                'cover_height': 500
            },
            {
                'book_id': 11,
                'book_name': 'Гарри Поттер и узник Азкабана',
                'author_id': 2,
                'author_name': 'Джоан Роулинг',
                'cover_width': 333,
                'cover_height': 500
            },
            {
                'book_id': 12,
                'book_name': 'Гарри Поттер и Кубок огня',
                'author_id': 2,
                'author_name': 'Джоан Роулинг',
                'cover_width': 333,
                'cover_height': 500
            },
            {
                'book_id': 13,
                'book_name': 'Гарри Поттер и Орден Феникса',
                'author_id': 2,
                'author_name': 'Джоан Роулинг',
                'cover_width': 333,
                'cover_height': 500
            },
            {
                'book_id': 14,
                'book_name': 'Гарри Поттер и Принц-полукровка',
                'author_id': 2,
                'author_name': 'Джоан Роулинг',
                'cover_width': 333,
                'cover_height': 500
            },
            {
                'book_id': 15,
                'book_name': 'Гарри Поттер и Дары Смерти',
                'author_id': 2,
                'author_name': 'Джоан Роулинг',
                'cover_width': 333,
                'cover_height': 500
            },
            {
                'book_id': 1,
                'book_name': 'Магия книгоходцев',
                'author_id': 1,
                'author_name': 'Милена Завойчинская',
                'cover_width': 317,
                'cover_height': 500
            },
            {
                'book_id': 2,
                'book_name': 'Боевая практика книгоходцев',
                'author_id': 1,
                'author_name': 'Милена Завойчинская',
                'cover_width': 317,
                'cover_height': 500
            },
            {
                'book_id': 3,
                'book_name': 'Книгоходцы особого назначения',
                'author_id': 1,
                'author_name': 'Милена Завойчинская',
                'cover_width': 317,
                'cover_height': 500
            },
            {
                'book_id': 4,
                'book_name': 'Книгоходцы и тайна механического бога',
                'author_id': 1,
                'author_name': 'Милена Завойчинская',
                'cover_width': 317,
                'cover_height': 500
            },
            {
                'book_id': 5,
                'book_name': 'Хроники книгоходцев',
                'author_id': 1,
                'author_name': 'Милена Завойчинская',
                'cover_width': 317,
                'cover_height': 500
            },
        ], title='Новинки')
    )

    return render_template(
        'index.html',
        sections=sections
    )


if __name__ == '__main__':
    app.run(port=config.PORT, host=config.HOST)