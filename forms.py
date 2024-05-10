from datetime import datetime
import re
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    SelectField,
    StringField,
    DateTimeField,
    SubmitField,
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
    transmission = SelectField("Выбрать коробку передач", choices=[('АКПП', 'АКПП'), ('МКПП', 'МКПП')],)

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
    transmission = SelectField("Коробка передач", choices=[('АКПП', 'АКПП'), ('МКПП', 'МКПП')], validators=[DataRequired()])
    is_deleted = BooleanField("Удалена")

    def validate_car_number(self, car_number):
        car_number.data = car_number.data.upper()
        car = Car.query.filter_by(car_number=car_number.data).first()
        if car:
            raise ValidationError("Машина с таким номером уже существует!")

    submit = SubmitField("Сохранить")


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
