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
    brand = StringField('Пример Hyundai Solaris', validators=[
                        DataRequired(message='Обязательное поле')])
    car_number = StringField(
        'Например А123МР',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(min=6, max=6),
            Regexp('^([А-ЯЁ]{1}|[A-Z]{1})\d{3}([А-ЯЁ]{2}|[A-Z]{2})$',
                   re.IGNORECASE,
                   message='Номер должен состоять букв и цифр без пробелов')
        ]
    )

    def validate_car_number(self, car_number):
        car_number.data = car_number.data.upper()
        car = Car.query.filter_by(car_number=car_number.data).first()
        if car:
            raise ValidationError('Машина с таким номером уже существует.')

    submit = SubmitField('Добавить')
