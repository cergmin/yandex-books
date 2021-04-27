import sqlalchemy
from .db_session import SqlAlchemyBase

cart = sqlalchemy.Table(
    'cart',
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