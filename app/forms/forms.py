import re
from datetime import datetime
from flask import current_app
from app.models import Booking, User
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
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

from app.models import Car


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
    transmission = SelectField(
        "Выбрать коробку передач",
        choices=[("АКПП", "АКПП"), ("МКПП", "МКПП")],
    )

    def validate_car_number(self, car_number):
        car_number.data = car_number.data.upper()
        car = Car.query.filter_by(car_number=car_number.data).first()
        if car:
            current_app.logger.error(f"Error add car with  number: {car_number.data}")
            raise ValidationError("Машина с таким номером уже существует!")

    submit = SubmitField("Добавить")


class EditCarForm(FlaskForm):
    brand = StringField("Марка", validators=[DataRequired()])
    car_number = StringField(
        "Номер машины",
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
    transmission = SelectField(
        "Коробка передач",
        choices=[("АКПП", "АКПП"), ("МКПП", "МКПП")],
        validators=[DataRequired()],
    )
    is_deleted = BooleanField("Удалена")

    submit = SubmitField("Сохранить")

    def validate_car_number(form, field):
        field.data = field.data.upper()


class BookingForm(FlaskForm):
    start_datetime = DateTimeField(
        "Дата начала бронирования", format="%d.%m.%Y %H:%M", validators=[DataRequired()]
    )
    end_datetime = DateTimeField(
        "Дата окончания бронирования",
        format="%d.%m.%Y %H:%M",
        validators=[DataRequired()],
    )
    car = SelectField(
        "Автомобиль", coerce=int, validators=[DataRequired()], default=None
    )
    phone = StringField("Телефон")
    description = TextAreaField("Описание")
    submit = SubmitField("Забронировать")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_car_choices()

    def set_car_choices(self):
        car_choices = [(0, "Выберите автомобиль")]
        car_choices.extend(
            (car.id, f"{car.brand} {car.car_number}")
            for car in Car.query.filter_by(is_deleted=False).all()
        )
        self.car.choices = car_choices

    def validate_start_datetime(self, field):
        current_datetime = datetime.now().replace(
            second=0, microsecond=0, minute=0, hour=0
        )
        if field.data < current_datetime:
            raise ValidationError(
                "Дата начала бронирования не может быть раньше текущей даты"
            )

    def validate_end_datetime(self, field):
        if field.data <= self.start_datetime.data:
            raise ValidationError(
                "Дата окончания бронирования должна быть позже даты начала"
            )

    def validate_car(self, field):
        if field.data is not None:
            overlapping_bookings = Booking.query.filter(
                Booking.car_id == field.data,
                Booking.start_date < self.end_datetime.data,
                Booking.end_date > self.start_datetime.data,
                Booking.status != "Отказ",
                Booking.status != "Завершено",
            ).first()
            if overlapping_bookings:
                raise ValidationError(
                    "Эта машина уже забронирована на выбранный период"
                )


class BookingUpdateForm(FlaskForm):
    start_date = DateTimeField(
        "Дата и время начала", format="%d.%m.%Y %H:%M", validators=[DataRequired()]
    )
    end_date = DateTimeField(
        "Дата и время окончания", format="%d.%m.%Y %H:%M", validators=[DataRequired()]
    )
    phone = StringField("Телефон", validators=[Length(max=20)])
    description = TextAreaField("Заметка", validators=[Length(max=200)])
    status = SelectField("Статус", validators=[DataRequired()])


class SearchCarsForm(FlaskForm):
    start_date = DateTimeLocalField(
        "Дата и время начала", format="%Y-%m-%dT%H:%M", validators=[DataRequired()]
    )
    end_date = DateTimeLocalField(
        "Дата и время окончания", format="%Y-%m-%dT%H:%M", validators=[DataRequired()]
    )
    submit = SubmitField("Поиск")
    current_datetime = datetime.now().replace(second=0, microsecond=0, minute=0, hour=0)

    def validate_end_date(self, end_date):
        if end_date.data <= self.start_date.data:
            raise ValidationError(
                "Дата и время окончания должны быть позже даты и времени начала."
            )


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Такой пользователь уже есть.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Такой email уже есть.")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Запомнить меня")
    submit = SubmitField("Login")


class HiddenForm(FlaskForm):
    pass


class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password')
    confirm = PasswordField('Confirm Password')
    is_superuser = BooleanField('Superuser')
    submit = SubmitField('Update')
