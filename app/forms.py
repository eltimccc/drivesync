from app.models import User
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from datetime import datetime
import re
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateTimeLocalField,
    SelectField,
    StringField,
    DateTimeField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length, Regexp

from .models import Car


class CarForm(FlaskForm):
    brand = StringField(
        "Например Hyundai Solaris",
        validators=[DataRequired(message="Обязательное поле")],
    )
    car_number = StringField(
        "Например А123МР",
        validators=[
            DataRequired(message="Обязательное поле"),
            Length(min=6, max=6),
            Regexp(
                "^([А-ЯЁ]{1}|[A-Z]{1})\d{3}([А-ЯЁ]{2}|[A-Z]{2})$",
                re.IGNORECASE,
                message="Номер должен состоять из букв и цифр без пробелов",
            ),
        ],
    )
    transmission = SelectField("Выбрать коробку передач", choices=[
                               ('АКПП', 'АКПП'), ('МКПП', 'МКПП')],)

    def validate_car_number(self, car_number):
        car_number.data = car_number.data.upper()
        car = Car.query.filter_by(car_number=car_number.data).first()
        if car:
            raise ValidationError("Машина с таким номером уже существует!")

    submit = SubmitField("Добавить")


class EditCarForm(FlaskForm):
    brand = StringField("Марка", validators=[DataRequired()])
    car_number = StringField("Номер машины", validators=[
        DataRequired(message="Обязательное поле"),
        Length(min=6, max=6),
        Regexp(
            "^([А-ЯЁ]{1}|[A-Z]{1})\d{3}([А-ЯЁ]{2}|[A-Z]{2})$",
            re.IGNORECASE,
            message="Номер должен состоять из букв и цифр без пробелов",
        ),
    ],)
    transmission = SelectField("Коробка передач", choices=[(
        'АКПП', 'АКПП'), ('МКПП', 'МКПП')], validators=[DataRequired()])
    is_deleted = BooleanField("Удалена")

    submit = SubmitField("Сохранить")

    def validate_car_number(form, field):
        field.data = field.data.upper()


class BookingForm(FlaskForm):
    start_datetime = DateTimeField(
        "Дата начала бронирования", format="%Y-%m-%dT%H:%M", validators=[DataRequired()]
    )
    end_datetime = DateTimeField(
        "Дата окончания бронирования",
        format="%Y-%m-%dT%H:%M",
        validators=[DataRequired()],
    )
    car = StringField("ID машины", validators=[DataRequired()])
    description = StringField("Описание")
    phone = StringField("Телефон", validators=[DataRequired()])
    submit = SubmitField("Забронировать")


class SearchCarsForm(FlaskForm):
    start_date = DateTimeLocalField(
        'Дата и время начала', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_date = DateTimeLocalField(
        'Дата и время окончания', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Поиск')
    current_datetime = datetime.now().replace(
        second=0, microsecond=0, minute=0, hour=0)

    def validate_end_date(self, end_date):
        if end_date.data <= self.start_date.data:
            raise ValidationError(
                "Дата и время окончания должны быть позже даты и времени начала.")


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Такой пользователь уже есть.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Такой email уже есть.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
