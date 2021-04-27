import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from .cart import cart
from .bought import bought_books


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )
    login = sqlalchemy.Column(
        sqlalchemy.String,
        index=True,
        unique=True
    )
    name = sqlalchemy.Column(
        sqlalchemy.String
    )
    surname = sqlalchemy.Column(
        sqlalchemy.String
    )
    password_hash = sqlalchemy.Column(
        sqlalchemy.String
    )
    status = sqlalchemy.Column(
        sqlalchemy.Integer,
        default=0
    )
    balance = sqlalchemy.Column(
        sqlalchemy.Integer,
        default=0
    )
    cart = sqlalchemy.orm.relation(
        'Book',
        secondary='cart',
        backref='user_cart'
    )
    bought_books = sqlalchemy.orm.relation(
        'Book',
        secondary='bought_books',
        backref='user_boughts'
    )
