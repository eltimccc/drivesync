from app.models import Booking
from app.models import Car

BOOKING_STATUSES = {
    "Бронь": "#99959e",  # Светло-серый цвет для забронированных автомобилей
    "Аренда": "#007bff",  # Синий цвет для текущих арендуемых автомобилей
    "Ожидание": "#ffc107",  # Желтый цвет для ожидающих подтверждения
    "Завершено": "#28a745",  # Зеленый цвет для завершенных бронирований
    "Отказ": "#dc3545",  # Красный цвет для отмененных бронирований
}

# Словарь для русских названий дней недели
RU_WEEKDAYS = {
    0: 'Пн',
    1: 'Вт',
    2: 'Ср',
    3: 'Чт',
    4: 'Пт',
    5: 'Сб',
    6: 'Вс'
}
RU_MONTHS = {
    1: 'Январь',
    2: 'Февраль',
    3: 'Марть',
    4: 'Апрель',
    5: 'Май',
    6: 'Июнь',
    7: 'Июль',
    8: 'Август',
    9: 'Сентябрь',
    10: 'Октябрь',
    11: 'Ноябрь',
    12: 'Декабрь'
}


def get_available_cars(start_date, end_date):
    """
    Возвращает список автомобилей, доступных для бронирования на указанный период.

    Автомобили считаются доступными, если они не заняты другими бронированиями
    в пределах указанных дат.

    Args:
        start_date (datetime): Дата начала интересующего периода.
        end_date (datetime): Дата окончания интересующего периода.

    Returns:
        List[Car]: Список доступных автомобилей.
    """

    return Car.query.filter(
        ~Car.bookings.any(
            (Booking.start_date <= end_date) & (Booking.end_date >= start_date)
        )
    ).all()


def enrich_car_with_bookings(car, start_date, end_date):
    """
    Дополняет информацию об автомобиле последним и следующим бронированиями
    относительно указанного периода.

    Это полезно для отображения информации о ближайших временных окнах,
    когда автомобиль был или будет занят.

    Args:
        car (Car): Объект автомобиля, который нужно дополнить.
        start_date (datetime): Дата начала интересующего периода.
        end_date (datetime): Дата окончания интересующего периода.

    Returns:
        None: Функция модифицирует переданный объект автомобиля.
    """

    last_booking = (
        Booking.query.filter(Booking.car_id == car.id,
                             Booking.end_date <= start_date)
        .order_by(Booking.end_date.desc())
        .first()
    )

    next_booking = (
        Booking.query.filter(Booking.car_id == car.id,
                             Booking.start_date >= end_date)
        .order_by(Booking.start_date)
        .first()
    )

    car.last_booking_end = (
        last_booking.end_date.strftime(
            "%d.%m.%Y %H:%M") if last_booking else None
    )

    car.next_booking_start = (
        next_booking.start_date.strftime(
            "%d.%m.%Y %H:%M") if next_booking else None
    )


def format_datetime(datetime_obj):
    return datetime_obj.strftime("%d.%m.%Y %H:%М")
