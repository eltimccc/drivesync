from datetime import datetime
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
    BOOKING_ALL_ROUTE,
    BOOKING_ALL_TEMPLATE,
    BOOKING_BP_NAME_ROUTE,
    BOOKING_DELETE_BP_ROUTE,
    BOOKING_DETAIL_MODAL_TEMPLATE,
    BOOKING_DETAIL_TEMPLATE,
    BOOKING_EDIT_BP_ROUTE,
    BOOKING_EDIT_TEMPLATE,
    BOOKING_MAIN_ROUTE,
    BOOKING_MODAL_TEMPLATE,
    BOOKING_URL_PREFIX,
    BOOKING_VIEW_BOOKING_ROUTE,
    BOOKING_VIEW_BP_ROUTE,
)
from app.forms.forms import BookingForm, BookingUpdateForm
from app.models import Booking, Car
from app.utils.utils import BOOKING_STATUSES


booking_blueprint = Blueprint(BOOKING_BP_NAME_ROUTE, __name__, url_prefix=BOOKING_URL_PREFIX)


@booking_blueprint.route(BOOKING_VIEW_BP_ROUTE, methods=["GET"])
@login_required
def view_booking(booking_id):
    current_app.logger.info(f"Accessed view booking with ID: {booking_id}")
    booking = Booking.query.get_or_404(booking_id)
    status_color = BOOKING_STATUSES.get(booking.status, "#ffffff")

    formatted_created_at = booking.created_at.strftime("%d.%m.%Y %H:%M")

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render_template(
            BOOKING_DETAIL_MODAL_TEMPLATE,
            booking=booking,
            status_color=status_color,
            formatted_created_at=formatted_created_at,
        )
    else:
        return render_template(
            BOOKING_DETAIL_TEMPLATE,
            booking=booking,
            status_color=status_color,
            formatted_created_at=formatted_created_at,
        )


@booking_blueprint.route(BOOKING_ALL_ROUTE, methods=["GET"])
@login_required
def all_bookings():
    current_app.logger.info("Accessed all bookings page.")
    sort_by = request.args.get("sort_by", "created_at")
    sort_order = request.args.get("sort_order", "desc")

    if sort_order == "desc":
        bookings = Booking.query.order_by(getattr(Booking, sort_by).desc()).all()
    else:
        bookings = Booking.query.order_by(getattr(Booking, sort_by).asc()).all()

    return render_template(
        BOOKING_ALL_TEMPLATE, bookings=bookings, sort_by=sort_by, sort_order=sort_order
    )


@booking_blueprint.route(BOOKING_ADD_BP_ROUTE, methods=["GET"])
@login_required
def get_booking():
    current_app.logger.info("Accessed add booking page.")
    form = BookingForm()
    car_id = request.args.get("car_id")
    start_datetime = request.args.get("start_datetime")
    end_datetime = request.args.get("end_datetime")

    cars = None
    if car_id and start_datetime and end_datetime:
        cars = Car.query.filter_by(is_deleted=False).all()
        return render_template(
            BOOKING_ADD_TEMPLATE,
            cars=cars,
            car_id=car_id,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )
    elif request.headers.get("X-Requested-With") == "XMLHttpRequest":
        cars = Car.query.filter_by(is_deleted=False).all()
        return render_template(BOOKING_MODAL_TEMPLATE, cars=cars)
    else:
        if cars is None:
            cars = Car.query.filter_by(is_deleted=False).all()
        return render_template(
            BOOKING_ADD_TEMPLATE, cars=cars, bootstrap=True, form=form
        )


@booking_blueprint.route(BOOKING_ADD_BP_ROUTE, methods=["POST", "GET"])
@login_required
def add_booking():
    form = BookingForm()
    cars = Car.query.filter_by(is_deleted=False).all()

    if request.method == "GET":
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        car_id = request.args.get("car_id")

        if start_date:
            print(start_date)
            try:
                form.start_datetime.data = datetime.strptime(
                    start_date, "%d.%m.%Y %H:%M"
                )
            except ValueError:
                form.start_datetime.data = None
        if end_date:
            try:
                form.end_datetime.data = datetime.strptime(end_date, "%d.%m.%Y %H:%M")
            except ValueError:
                form.end_datetime.data = None
        if car_id:
            form.car.data = car_id

    if form.validate_on_submit():
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
        return redirect(url_for(BOOKING_MAIN_ROUTE))

    return render_template(BOOKING_ADD_TEMPLATE, form=form, cars=cars)


@booking_blueprint.route(BOOKING_EDIT_BP_ROUTE, methods=["GET", "POST"])
@login_required
def edit_booking(booking_id):
    current_app.logger.info(f"Accessed edit booking page with ID: {booking_id}")
    booking = Booking.query.get_or_404(booking_id)
    form = BookingUpdateForm(obj=booking)
    form.status.choices = [(key, key) for key in BOOKING_STATUSES.keys()]
    cars = Car.query.filter_by(is_deleted=False).all()

    if form.validate_on_submit():
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
        current_app.logger.info(f"Updated booking with ID: {booking_id}")
        return redirect(url_for(BOOKING_VIEW_BOOKING_ROUTE, booking_id=booking.id))

    return render_template(BOOKING_EDIT_TEMPLATE, form=form, booking=booking, cars=cars)


@booking_blueprint.route(BOOKING_DELETE_BP_ROUTE, methods=["POST"])
@login_required
def delete_booking(booking_id):
    current_app.logger.info(f"Accessed delete booking with ID: {booking_id}")
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    current_app.logger.warning(f"Deleted booking with ID: {booking_id}")
    return redirect(url_for(BOOKING_MAIN_ROUTE))
