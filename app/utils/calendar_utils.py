from collections import defaultdict
from datetime import datetime, timedelta

from flask import request
from app.models.booking import Booking
from app.models.car import Car
from app.utils.utils import RU_MONTHS, RU_WEEKDAYS


def get_available_cars() -> list:
    """Получаем список доступных машин."""
    return Car.query.filter_by(is_deleted=False).all()


def get_start_date_from_request() -> datetime:
    """Получаем начальную дату из запроса или текущую дату."""
    start_date_str = request.args.get('start_date')
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        except ValueError:
            start_date = datetime.today()
    else:
        start_date = datetime.today()

    return start_date.replace(hour=0, minute=0, second=0, microsecond=0)


def get_week_title(start_date: datetime) -> str:
    """Формируем заголовок недели на основе месяца и года."""
    return f"{RU_MONTHS[start_date.month]} {start_date.year}"


def get_week_dates(start_date: datetime) -> list:
    """Генерируем список дней недели для отображения в календаре."""
    dates = []
    for i in range(7):
        day = start_date + timedelta(days=i)
        dates.append({
            'day': day.day,
            'weekday': RU_WEEKDAYS[day.weekday()],
            'date': day,
            'month_name': RU_MONTHS[day.month]
        })
    return dates


def get_bookings_in_range(start_date: datetime, last_day: datetime) -> list:
    """Получаем все бронирования, которые попадают в диапазон недели."""
    return Booking.query.filter(
        Booking.start_date < last_day,
        Booking.end_date >= start_date,
        Booking.status != "Отказ"
    ).all()


def map_bookings_to_dates(bookings: list, start_date: datetime, last_day: datetime) -> dict:
    """Сопоставляем бронирования с датами в пределах указанного диапазона."""
    bookings_dict = defaultdict(dict)
    for booking in bookings:
        current = booking.start_date
        while current.date() <= booking.end_date.date():
            if start_date.date() <= current.date() < last_day.date():
                if current.date() not in bookings_dict[booking.car_id]:
                    bookings_dict[booking.car_id][current.date()] = {
                        'booking_id': booking.id,
                        'end_date': booking.end_date,
                        'status': booking.status
                    }
            current += timedelta(days=1)
    return bookings_dict