import sqlalchemy
from .db_session import SqlAlchemyBase


class Book(SqlAlchemyBase):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, index=True)
    short_name = sqlalchemy.Column(sqlalchemy.String, default='')
    description = sqlalchemy.Column(sqlalchemy.Text, default='')
    author_id = sqlalchemy.Column(sqlalchemy.String)
    series_id = sqlalchemy.Column(sqlalchemy.Integer, default=-1)
    price = sqlalchemy.Column(sqlalchemy.Float)
    cover_width = sqlalchemy.Column(sqlalchemy.Integer)
    cover_height = sqlalchemy.Column(sqlalchemy.Integer)
