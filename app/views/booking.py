from datetime import datetime, timedelta
from collections import defaultdict
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    current_app,
)
from flask_login import current_user, login_required

from app import db
from app.constants import (
    BOOKING_ADD_BP_ROUTE,
    BOOKING_ADD_TEMPLATE,
    BOOKING_BP_NAME_ROUTE,
    BOOKING_CALENDAR_TEMPLATE,
    BOOKING_DELETE_BP_ROUTE,
    BOOKING_DETAIL_MODAL_ROUTE,
    BOOKING_DETAIL_MODAL_TEMPLATE,
    BOOKING_DETAIL_TEMPLATE,
    BOOKING_EDIT_BP_ROUTE,
    BOOKING_EDIT_TEMPLATE,
    BOOKING_MAIN_ROUTE,
    BOOKING_MODAL_TEMPLATE,
    BOOKING_URL_PREFIX,
    BOOKING_VIEW_BP_ROUTE,
)
from app.utils.booking_helpers import handle_successful_booking, log_form_errors, prepopulate_form_from_request
from app.forms.forms import BookingForm, BookingUpdateForm
from app.models import Booking
from app.models import Car
from app.utils.utils import BOOKING_STATUSES, RU_MONTHS, RU_WEEKDAYS


booking_blueprint = Blueprint(
    BOOKING_BP_NAME_ROUTE, __name__, url_prefix=BOOKING_URL_PREFIX
)


@booking_blueprint.route(BOOKING_VIEW_BP_ROUTE, methods=["GET"])
@login_required
def view_booking(booking_id):
    current_app.logger.info(f"Accessed view booking with ID: {booking_id}")
    booking = Booking.query.get_or_404(booking_id)
    status_color = BOOKING_STATUSES.get(booking.status, "#ffffff")

    formatted_created_at = booking.created_at.strftime("%d.%m.%Y %H:%M")

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        current_app.logger.debug(
            f"Rendering booking detail modal for booking ID: {booking_id}"
        )
        return render_template(
            BOOKING_DETAIL_MODAL_TEMPLATE,
            booking=booking,
            status_color=status_color,
            formatted_created_at=formatted_created_at,
        )
    else:
        current_app.logger.debug(
            f"Rendering booking detail page for booking ID: {booking_id}"
        )
        return render_template(
            BOOKING_DETAIL_TEMPLATE,
            booking=booking,
            status_color=status_color,
            formatted_created_at=formatted_created_at,
        )


@booking_blueprint.route(BOOKING_DETAIL_MODAL_ROUTE, methods=["GET"])
@login_required
def view_booking_modal(booking_id):
    current_app.logger.info(
        f"Accessed view booking modal with ID: {booking_id}")
    booking = Booking.query.get_or_404(booking_id)
    status_color = BOOKING_STATUSES.get(booking.status, "#ffffff")

    formatted_created_at = booking.created_at.strftime("%d.%m.%Y %H:%M")

    current_app.logger.debug(
        f"Rendering booking detail modal for booking ID: {booking_id}"
    )
    return render_template(
        BOOKING_DETAIL_MODAL_TEMPLATE,
        booking=booking,
        status_color=status_color,
        formatted_created_at=formatted_created_at,
    )


@booking_blueprint.route("/bookings/today", methods=["GET"])
@login_required
def bookings_today():
    date_str = request.args.get("date")
    if date_str:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        selected_date = datetime.today().date()

    pick_ups = (
        db.session.query(Booking)
        .join(Car)
        .filter(
            db.func.date(
                Booking.start_date) == selected_date, Booking.status != "Отказ"
        )
        .all()
    )
    drop_offs = (
        db.session.query(Booking)
        .join(Car)
        .filter(
            db.func.date(
                Booking.end_date) == selected_date, Booking.status != "Отказ"
        )
        .all()
    )

    return render_template(
        "bookings_today.html",
        pick_ups=pick_ups,
        drop_offs=drop_offs,
        today=selected_date,
    )


@booking_blueprint.route(BOOKING_ADD_BP_ROUTE, methods=["POST", "GET"])
@login_required
def add_booking():
    current_app.logger.info(
        f"User {current_user.username} accessed add booking endpoint."
    )
    form = BookingForm()
    cars = Car.query.filter_by(is_deleted=False).all()

    if request.method == "GET":
        prepopulate_form_from_request(form)

    if form.validate_on_submit():
        return handle_successful_booking(form, current_user)
    else:
        log_form_errors(form, current_user)

    return render_template(BOOKING_ADD_TEMPLATE, form=form, cars=cars)


@booking_blueprint.route(BOOKING_EDIT_BP_ROUTE, methods=["GET", "POST"])
@login_required
def edit_booking(booking_id):
    current_app.logger.info(
        f"User {current_user.username} accessed edit booking page with ID: {booking_id}"
    )
    booking = Booking.query.get_or_404(booking_id)
    form = BookingUpdateForm(obj=booking)
    form.status.choices = [(key, key) for key in BOOKING_STATUSES.keys()]
    cars = Car.query.filter_by(is_deleted=False).all()

    if form.validate_on_submit():
        current_app.logger.info(
            f"User {current_user.username} validated booking form for update of booking ID: {booking_id}"
        )
        booking.description = form.description.data
        booking.phone = form.phone.data
        booking.start_date = form.start_date.data
        booking.end_date = form.end_date.data
        booking.status = form.status.data

        car_id = request.form.get("car")
        booking.car = Car.query.get(car_id)

        booking.color = BOOKING_STATUSES[booking.status]
        if booking.color == BOOKING_STATUSES["Отказ"]:
            booking.end_date = booking.start_date

        db.session.commit()
        flash("Бронирование успешно обновлено", "success")
        current_app.logger.info(
            f"User {current_user.username} updated booking with ID: {booking_id}"
        )
        return redirect(url_for(BOOKING_MAIN_ROUTE, edited_booking_id=booking.id))
    else:
        current_app.logger.warning(
            f"User {current_user.username} failed booking form validation for booking ID: {booking_id}"
        )

    return render_template(BOOKING_EDIT_TEMPLATE, form=form, booking=booking, cars=cars)


@booking_blueprint.route(BOOKING_DELETE_BP_ROUTE, methods=["POST"])
@login_required
def delete_booking(booking_id):
    current_app.logger.info(
        f"User {current_user.username} accessed delete booking with ID: {booking_id}"
    )
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    current_app.logger.warning(
        f"User {current_user.username} deleted booking with ID: {booking_id}"
    )
    return redirect(url_for(BOOKING_MAIN_ROUTE))


@booking_blueprint.route('/calendar', methods=["GET"])
@login_required
def calendar_view():
    cars = Car.query.filter_by(is_deleted=False).all()

    # Получение параметра start_date из строки запроса
    start_date_str = request.args.get('start_date')
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        except ValueError:
            start_date = datetime.today()
    else:
        start_date = datetime.today()

    start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)

    current_week_title = f"{RU_MONTHS[start_date.month]} {start_date.year}"

    dates = []
    for i in range(7):
        day = start_date + timedelta(days=i)
        dates.append({
            'day': day.day,
            'weekday': RU_WEEKDAYS[day.weekday()],
            'date': day,
            'month_name': RU_MONTHS[day.month]
        })

    last_day = start_date + timedelta(days=7)

    bookings = Booking.query.filter(
        Booking.start_date < last_day,
        Booking.end_date >= start_date,
        Booking.status != "Отказ"
    ).all()

    # car_id -> date -> {'booking_id': id, 'end_date': date}
    bookings_dict = defaultdict(dict)
    for booking in bookings:
        current = booking.start_date
        while current.date() <= booking.end_date.date():
            if start_date.date() <= current.date() < last_day.date():
                if current.date() not in bookings_dict[booking.car_id]:
                    bookings_dict[booking.car_id][current.date()] = {
                        'booking_id': booking.id,
                        'end_date': booking.end_date
                    }
            current += timedelta(days=1)

    for car in cars:
        bookings_dict.setdefault(car.id, {})

    prev_start_date = start_date - timedelta(days=7)
    next_start_date = start_date + timedelta(days=7)

    return render_template(
        BOOKING_CALENDAR_TEMPLATE,
        cars=cars,
        dates=dates,
        current_week=current_week_title,
        bookings_dict=bookings_dict,
        prev_start_date=prev_start_date.strftime('%Y-%m-%d'),
        next_start_date=next_start_date.strftime('%Y-%m-%d')
    )
