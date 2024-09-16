from datetime import datetime
from flask import request, current_app, redirect, url_for
from app.constants import BOOKING_MAIN_ROUTE
from app.models import Booking
from app import db


def prepopulate_form_from_request(form):
    """Заполняет форму данными из GET-запроса."""
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    car_id = request.args.get("car_id")

    if start_date:
        try:
            form.start_datetime.data = datetime.strptime(start_date, "%d.%m.%Y %H:%M")
        except ValueError:
            form.start_datetime.errors.append(
                "Неверный формат даты начала. Используйте дд.мм.гггг чч:мм"
            )
            current_app.logger.error(f"Failed to parse start_date: {start_date}")

    if end_date:
        try:
            form.end_datetime.data = datetime.strptime(end_date, "%d.%m.%Y %H:%M")
        except ValueError:
            form.end_datetime.errors.append(
                "Неверный формат даты окончания. Используйте дд.мм.гггг чч:мм"
            )
            current_app.logger.error(f"Failed to parse end_date: {end_date}")

    if car_id:
        try:
            form.car.data = int(car_id)
        except ValueError:
            current_app.logger.error(f"Invalid car_id: {car_id}")


def handle_successful_booking(form, current_user):
    """Обрабатывает успешную валидацию формы и создает новое бронирование."""
    new_booking = Booking(
        start_date=form.start_datetime.data,
        end_date=form.end_datetime.data,
        car_id=form.car.data,
        phone=form.phone.data,
        description=form.description.data,
        user=current_user,
    )

    db.session.add(new_booking)
    db.session.commit()

    current_app.logger.info(
        f"User {current_user.username} добавлено новое бронирование с ID: {new_booking.id}"
    )
    return redirect(url_for(BOOKING_MAIN_ROUTE))


def log_form_errors(form, current_user):
    """Логирует ошибки валидации формы."""
    if form.errors:
        current_app.logger.warning(
            f"User {current_user.username} failed booking form validation: {form.errors}"
        )
