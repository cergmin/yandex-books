import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Book(SqlAlchemyBase):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, index=True)
    author_id = sqlalchemy.Column(sqlalchemy.String)
    series = sqlalchemy.Column(sqlalchemy.Integer, default=-1)
    cover_width = sqlalchemy.Column(sqlalchemy.Integer)
    cover_height = sqlalchemy.Column(sqlalchemy.Integer)
