import sqlalchemy
from .db_session import SqlAlchemyBase

bought_books = sqlalchemy.Table(
    'bought_books',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column(
        'user',
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('users.id')
    ),
    sqlalchemy.Column(
        'book',
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('books.id')
    )
)