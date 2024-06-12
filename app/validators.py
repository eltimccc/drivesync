from datetime import datetime


def validate_dates(start_date, end_date):
    current_datetime = datetime.now().replace(second=0, microsecond=0, minute=0, hour=0)

    if start_date < current_datetime:
        raise ValueError("Дата начала бронирования не может быть раньше текущей даты")

    if start_date >= end_date:
        raise ValueError(
            "Дата начала не может быть больше даты окончания бронирования "
        )
