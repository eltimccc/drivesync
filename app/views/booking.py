from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app import db
from app.constants import (
    BOOKING_ADD_BP_ROUTE,
    BOOKING_DELETE_BP_ROUTE,
    BOOKING_DETAIL_MODAL_TEMPLATE,
    BOOKING_DETAIL_TEMPLATE,
    BOOKING_EDIT_BP_ROUTE,
    BOOKING_EDIT_TEMPLATE,
    BOOKING_MAIN_ROUTE,
    BOOKING_VIEW_BOOKING_ROUTE,
    BOOKING_VIEW_BP_ROUTE,
)
from app.models import Booking, Car
from app.utils.utils import BOOKING_STATUSES, add_booking_get, add_booking_post


booking_blueprint = Blueprint("booking", __name__, url_prefix="/booking")


@booking_blueprint.route(BOOKING_VIEW_BP_ROUTE, methods=["GET"])
@login_required
def view_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    status_color = BOOKING_STATUSES.get(booking.status, "#ffffff")

    formatted_created_at = booking.created_at.strftime('%d.%m.%Y %H:%M')
    
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render_template(
            BOOKING_DETAIL_MODAL_TEMPLATE, booking=booking, status_color=status_color, formatted_created_at=formatted_created_at
        )
    else:
        return render_template(
            BOOKING_DETAIL_TEMPLATE, booking=booking, status_color=status_color, formatted_created_at=formatted_created_at
        )


# @booking_blueprint.route('/all_bookings', methods=["GET"])
# @login_required
# def all_bookings():
#     bookings = Booking.query.all()
#     return render_template('all_bookings.html', bookings=bookings)
@booking_blueprint.route('/all_bookings', methods=["GET"])
@login_required
def all_bookings():
    sort_by = request.args.get('sort_by', 'created_at')
    sort_order = request.args.get('sort_order', 'desc')

    if sort_order == 'desc':
        bookings = Booking.query.order_by(getattr(Booking, sort_by).desc()).all()
    else:
        bookings = Booking.query.order_by(getattr(Booking, sort_by).asc()).all()

    return render_template('all_bookings.html', bookings=bookings, sort_by=sort_by, sort_order=sort_order)



@booking_blueprint.route(BOOKING_ADD_BP_ROUTE, methods=["GET", "POST"])
@login_required
def add_booking():
    if request.method == "POST":
        return add_booking_post()
    else:
        return add_booking_get()


@booking_blueprint.route(BOOKING_EDIT_BP_ROUTE, methods=["GET", "POST"])
@login_required
def edit_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    cars = Car.query.filter_by(is_deleted=False).all()
    status_choices = list(BOOKING_STATUSES.keys())
    errors = {}

    if request.method == "POST":
        try:
            description = request.form["description"]
            phone = request.form["phone"]
            start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%dT%H:%M")
            end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%dT%H:%M")
            car_id = request.form.get("car")
            car = Car.query.get(car_id)
            new_status = request.form.get("status")

            # validate_dates(start_date, end_date)

            booking.description = description
            booking.phone = phone
            booking.start_date = start_date
            booking.end_date = end_date
            booking.car = car

            if new_status in status_choices:
                booking.status = new_status
                booking.color = BOOKING_STATUSES[new_status]
                if booking.color == BOOKING_STATUSES["Отказ"]:
                    booking.end_date = booking.start_date

            db.session.commit()
            flash("Бронирование успешно обновлено", "success")
            return redirect(url_for(BOOKING_VIEW_BOOKING_ROUTE, booking_id=booking.id))

        except ValueError as e:
            errors["validation_error"] = str(e)

    return render_template(
        BOOKING_EDIT_TEMPLATE,
        booking=booking,
        cars=cars,
        status_choices=status_choices,
        booking_statuses=BOOKING_STATUSES,
        errors=errors,
    )


@booking_blueprint.route(BOOKING_DELETE_BP_ROUTE, methods=["POST"])
@login_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    return redirect(url_for(BOOKING_MAIN_ROUTE))