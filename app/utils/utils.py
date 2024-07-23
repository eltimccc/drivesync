from app.models import Booking, Car

BOOKING_STATUSES = {
    "Аренда": "#007bff",  # Синий цвет
    "Завершено": "#28a745",  # Зеленый цвет
    "Отказ": "#dc3545",  # Красный цвет
    "Ожидание": "#ffc107",  # Желтый цвет
    "Бронь": "#99959e",  # Светло-серый
}


def get_available_cars(start_date, end_date):
    return Car.query.filter(
        ~Car.bookings.any(
            (Booking.start_date <= end_date) & (Booking.end_date >= start_date)
        )
    ).all()


def enrich_car_with_bookings(car, start_date, end_date):
    # Поиск последнего бронирования до начала интересующего периода
    last_booking = (
        Booking.query.filter(Booking.car_id == car.id, Booking.end_date <= start_date)
        .order_by(Booking.end_date.desc())
        .first()
    )

    # Поиск следующего бронирования после окончания интересующего периода
    next_booking = (
        Booking.query.filter(Booking.car_id == car.id, Booking.start_date >= end_date)
        .order_by(Booking.start_date)
        .first()
    )

    # Если найдено последнее бронирование, добавляем его дату окончания к информации об автомобиле
    if last_booking:
        car.last_booking_end = last_booking.end_date.strftime("%d.%m.%Y %H:%M")
    else:
        car.last_booking_end = "Нет данных"

    # Если найдено следующее бронирование, добавляем его дату начала к информации об автомобиле
    if next_booking:
        car.next_booking_start = next_booking.start_date.strftime("%d.%m.%Y %H:%M")
    else:
        car.next_booking_start = "Нет данных"


def format_datetime(datetime_obj):
    return datetime_obj.strftime("%d.%m.%Y %H:%M")
