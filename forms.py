from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
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