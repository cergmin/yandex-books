import flask
import config
from random import sample, randint, choice
from controllers import DataController
from flask_login import current_user, login_required
from json import dumps

dc = DataController('db/data.db')

blueprint = flask.Blueprint(
    'api',
    __name__,
    template_folder=config.TEMPLATE_FOLDER
)


@blueprint.route('/api/sections/<int:amount>', methods=['GET'])
def api_sections(amount):
    sections = []

    title_start = [
        'Точно', 'Мы уверены', 'Несомненно'
    ]

    title_end = [
        ' тебе понравится', ' тебя поразит', ' тебя удивит',
        'вам понравится', 'вас поразит', 'вас удивит'
    ]

    for i in range(amount):
        sections.append({
            'title': choice(title_start) + ' ' + choice(title_end),
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


@blueprint.route('/api/cart/<int:book_id>', methods=['PUT', 'DELETE'])
@login_required
def api_cart(book_id):
    if flask.request.method == 'PUT':
        dc.add_item_to_cart(current_user.id, book_id)
    elif flask.request.method == 'DELETE':
        dc.delete_item_from_cart(current_user.id, book_id)
    
    return dumps({
        'is_ok': True
    })


@blueprint.route('/api/buy/<int:book_id>', methods=['POST'])
@login_required
def api_buy(book_id):
    return dumps(
        dc.buy_book(current_user.id, book_id)
    )