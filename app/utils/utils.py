from app.models import Booking
from app.models import Car

BOOKING_STATUSES = {
    "Аренда": "#007bff",  # Синий цвет для текущих арендуемых автомобилей
    "Бронь": "#99959e",  # Светло-серый цвет для забронированных автомобилей
    "Ожидание": "#ffc107",  # Желтый цвет для ожидающих подтверждения
    "Завершено": "#28a745",  # Зеленый цвет для завершенных бронирований
    "Отказ": "#dc3545",  # Красный цвет для отмененных бронирований
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
        Booking.query.filter(Booking.car_id == car.id, Booking.end_date <= start_date)
        .order_by(Booking.end_date.desc())
        .first()
    )

    next_booking = (
        Booking.query.filter(Booking.car_id == car.id, Booking.start_date >= end_date)
        .order_by(Booking.start_date)
        .first()
    )

    car.last_booking_end = (
        last_booking.end_date.strftime("%d.%m.%Y %H:%M") if last_booking else None
    )

    car.next_booking_start = (
        next_booking.start_date.strftime("%d.%m.%Y %H:%M") if next_booking else None
    )


def format_datetime(datetime_obj):
    return datetime_obj.strftime("%d.%m.%Y %H:%М")
