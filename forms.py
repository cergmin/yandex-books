from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


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
    login = StringField(
        'Логин',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()]
    )
    submit = SubmitField('Зарегестрироваться')