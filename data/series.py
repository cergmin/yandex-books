import sqlalchemy
from .db_session import SqlAlchemyBase


class Series(SqlAlchemyBase):
    __tablename__ = 'series'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, index=True)
