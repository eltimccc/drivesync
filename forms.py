from datetime import datetime
import re
from flask_wtf import FlaskForm
from wtforms import (
    DateTimeLocalField,
    SelectField,
    StringField,
    DateTimeField,
    SubmitField,
    TextAreaField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length, Regexp

from models import Car


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

    def validate_car_number(self, car_number):
        car_number.data = car_number.data.upper()
        car = Car.query.filter_by(car_number=car_number.data).first()
        if car:
            raise ValidationError("Машина с таким номером уже существует!")

    submit = SubmitField("Добавить")


class BookingForm(FlaskForm):
    car_id = StringField("Car ID", validators=[DataRequired()])
    start_datetime = DateTimeField(
        "Start Date and Time", format="%Y-%m-%dT%H:%M", validators=[DataRequired()]
    )
    end_datetime = DateTimeField(
        "End Date and Time", format="%Y-%m-%dT%H:%M", validators=[DataRequired()]
    )
    phone = StringField("Phone")
    description = TextAreaField("Description")
    submit = SubmitField("Submit")

    def validate_start_datetime(self, start_datetime):
        current_datetime = datetime.now().replace(
            second=0, microsecond=0, minute=0, hour=0
        )
        if start_datetime.data < current_datetime:
            raise ValidationError(
                "Дата начала бронирования не может быть раньше текущей даты"
            )

    def validate_end_datetime(self, end_datetime):
        if self.start_datetime.data >= end_datetime.data:
            raise ValidationError(
                "Дата начала не может быть больше даты окончания бронирования "
            )

    def validate_car_id(self, car_id):
        car = Car.query.get(car_id.data)
        if not car or car.is_deleted:
            raise ValidationError("Нужно выбрать доступный автомобиль")
