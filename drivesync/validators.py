from datetime import datetime


def validate_booking_data(start_datetime, end_datetime, car):
    current_datetime = datetime.now().replace(second=0, microsecond=0, minute=0, hour=0)

    if start_datetime < current_datetime:
        raise ValueError("Дата начала бронирования не может быть раньше текущей даты")

    if start_datetime >= end_datetime:
        raise ValueError(
            "Дата начала не может быть больше даты окончания бронирования "
        )

    if car is None:
        raise ValueError("Нужно выбрать машину")


def validate_dates(start_date, end_date):
    current_datetime = datetime.now().replace(
        second=0, microsecond=0, minute=0, hour=0)

    if start_date < current_datetime:
        raise ValueError("Дата начала бронирования не может быть раньше текущей даты")

    if start_date >= end_date:
        raise ValueError(
            "Дата начала не может быть больше даты окончания бронирования "
        )