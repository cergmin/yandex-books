from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import TextAreaField, StringField, IntegerField, FloatField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    login = StringField(
        'Логин',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()]
    )
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    name = StringField(
        'Ваше имя',
        validators=[DataRequired()]
    )
    surname = StringField(
        'Ваша фамилия',
        validators=[DataRequired()]
    )
    email = StringField(
        'E-mail',
        validators=[DataRequired(), Email()]
    )
    login = StringField(
        'Логин',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()]
    )
    submit = SubmitField('Зарегестрироваться')


class PaymentForm(FlaskForm):
    giftcode = StringField(
        'Подарочный код'
    )
    submit = SubmitField('Активировать')


class AddBookForm(FlaskForm):
    cover = FileField(
        'Обложка',
        validators=[FileRequired()]
    )
    book = FileField(
        'Текст',
        validators=[FileRequired()]
    )
    name = StringField(
        'Название',
        validators=[DataRequired()]
    )
    short_name = StringField(
        'Короткое название'
    )
    description = TextAreaField(
        'Описание',
        validators=[DataRequired()]
    )
    author_id = IntegerField(
        'Автор',
        validators=[DataRequired()]
    )
    series_id = IntegerField(
        'Серия',
        validators=[DataRequired()]
    )
    price = FloatField(
        'Цена',
        validators=[DataRequired()]
    )
    submit = SubmitField('Добавить')