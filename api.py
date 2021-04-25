import flask
import config
from random import sample, randint
from controllers import DataController
from json import dumps

dc = DataController('db/data.db')

blueprint = flask.Blueprint(
    'api',
    __name__,
    template_folder=config.TEMPLATE_FOLDER
)


@blueprint.route('/api/sections/<int:amount>', methods=['GET'])
def get_sections(amount):
    sections = []

    for i in range(amount):
        sections.append({
            'title': 'Название секции #' + str(i),
            'books': [],
            'max_cover_ratio': 0

        })

        books = sample(
            dc.get_books(),
            randint(5, 10)
        )

        for book in books:
            sections[-1]['books'].append({
                'book_id': str(book.id),
                'book_name': (
                    book.name
                    if len(book.short_name) == 0 else
                    book.short_name
                ),
                'author_id': str(book.author_id),
                'author_name': dc.get_author(book.author_id).name,
                'cover_ratio': book.cover_height / book.cover_width
            })

            sections[-1]['max_cover_ratio'] = max(
                sections[-1]['max_cover_ratio'],
                book.cover_height / book.cover_width
            )

    return dumps(sections)