import sqlalchemy
from .db_session import SqlAlchemyBase


class GiftCode(SqlAlchemyBase):
    __tablename__ = 'giftcodes'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )
    code = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    value = sqlalchemy.Column(sqlalchemy.Integer)
