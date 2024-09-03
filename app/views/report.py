from collections import defaultdict
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request
from flask_login import login_required
from sqlalchemy import and_

from app.constants import (
    REPORT_BOOKING_DURATION_BP_ROUTE,
    REPORT_BOOKING_DURATION_TEMPLATE,
    REPORT_BOOKING_PERIOD_BP_ROUTE,
    REPORT_BOOKING_PERIOD_TEMPLATE,
    REPORT_PAGE_TEMPLATE,
    REPORT_RENTCAR_AMOUNT_BP_ROUTE,
    REPORT_RENTCAR_AMOUNT_TEMPLATE,
    REPORT_STATUS_RENT_BP_ROUTE,
    REPORT_STATUS_RENT_TEMPLATE,
    SEARCH_AVAIALBLE_CARS_TEMPLATE,
    SEARCH_CARS_BP_ROUTE,
)
from app.forms.forms import SearchCarsForm
from app.models import Booking
from app.models import Car
from app.utils.utils import BOOKING_STATUSES

report_blueprint = Blueprint("report", __name__, url_prefix="/report")


@report_blueprint.route("/reports_page", methods=["GET"])
@login_required
def reports_page():
    return render_template(REPORT_PAGE_TEMPLATE)


@report_blueprint.route(REPORT_BOOKING_PERIOD_BP_ROUTE, methods=["GET", "POST"])
@login_required
def generate_report():
    if request.method == "POST":
        start_date_str = request.form["start_date"]
        end_date_str = request.form["end_date"]
        start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M")

        bookings = Booking.query.filter(
            Booking.start_date.between(start_date, end_date)
        ).all()

        bookings_completed = Booking.query.filter(
            and_(
                Booking.end_date.between(start_date, end_date),
                Booking.start_date <= end_date,
            )
        ).count()

        bookings_by_status = defaultdict(int)
        for booking in bookings:
            bookings_by_status[booking.status] += 1

        start_date_formatted = start_date.strftime("%d.%m.%Y %H:%M")
        end_date_formatted = end_date.strftime("%d.%m.%Y %H:%M")

        return render_template(
            REPORT_BOOKING_PERIOD_TEMPLATE,
            start_date=start_date_formatted,
            end_date=end_date_formatted,
            bookings_count=len(bookings),
            bookings_completed=bookings_completed,
            bookings_by_status=bookings_by_status,
            booking_statuses=BOOKING_STATUSES,
        )

    return render_template(REPORT_BOOKING_PERIOD_TEMPLATE)


@report_blueprint.route(REPORT_RENTCAR_AMOUNT_BP_ROUTE, methods=["GET", "POST"])
@login_required
def report_rent_amount():
    if request.method == "POST":
        start_date_str = request.form["start_date"]
        end_date_str = request.form["end_date"]
        start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M")

        cars = Car.query.all()

        cars_booked = []
        for car in cars:
            bookings_count = Booking.query.filter(
                Booking.car_id == car.id,
                Booking.start_date <= end_date,
                Booking.end_date >= start_date,
            ).count()
            if bookings_count > 0:
                cars_booked.append((car, bookings_count))

        start_date_formatted = start_date.strftime("%d.%m.%Y %H:%M")
        end_date_formatted = end_date.strftime("%d.%m.%Y %H:%M")

        return render_template(
            REPORT_RENTCAR_AMOUNT_TEMPLATE,
            start_date=start_date_formatted,
            end_date=end_date_formatted,
            cars_booked=cars_booked,
        )

    return render_template(REPORT_RENTCAR_AMOUNT_TEMPLATE)


@report_blueprint.route(REPORT_STATUS_RENT_BP_ROUTE, methods=["GET", "POST"])
@login_required
def report_status_rent():
    if request.method == "POST":
        start_date_str = request.form["start_date"]
        end_date_str = request.form["end_date"]
        start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M")

        bookings = Booking.query.filter(
            Booking.start_date <= end_date,
            Booking.end_date >= start_date,
            Booking.status == "Аренда",
        ).all()

        cars_status = {}
        for booking in bookings:
            car = booking.car
            if car not in cars_status:
                cars_status[car] = "Аренда"

        start_date_formatted = start_date.strftime("%d.%m.%Y %H:%M")
        end_date_formatted = end_date.strftime("%d.%m.%Y %H:%M")

        return render_template(
            REPORT_STATUS_RENT_TEMPLATE,
            start_date=start_date_formatted,
            end_date=end_date_formatted,
            cars_status=cars_status,
        )

    return render_template(REPORT_STATUS_RENT_TEMPLATE)


@report_blueprint.route(REPORT_BOOKING_DURATION_BP_ROUTE, methods=["GET", "POST"])
@login_required
def report_booking_duration():
    if request.method == "POST":
        start_date_str = request.form["start_date"]
        end_date_str = request.form["end_date"]
        start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M")

        cars = Car.query.filter(Car.is_deleted == False).all()

        cars_duration = {}
        total_duration = timedelta()

        for car in cars:
            bookings = Booking.query.filter(
                Booking.car_id == car.id,
                Booking.start_date <= end_date,
                Booking.end_date >= start_date,
            ).all()

            car_duration = timedelta()
            for booking in bookings:
                intersection_start = (
                    booking.start_date
                    if booking.start_date >= start_date
                    else start_date
                )
                intersection_end = (
                    booking.end_date if booking.end_date <= end_date else end_date
                )
                duration = intersection_end - intersection_start
                car_duration += duration

            cars_duration[car] = car_duration
            total_duration += car_duration

        total_hours = total_duration.total_seconds() // 3600
        total_minutes = (total_duration.total_seconds() % 3600) // 60
        total_duration_str = f"{int(total_hours)} часов {int(total_minutes)} минут"

        return render_template(
            REPORT_BOOKING_DURATION_TEMPLATE,
            start_date=start_date_str,
            end_date=end_date_str,
            cars_duration=cars_duration,
            total_duration=total_duration_str,
        )

    return render_template(REPORT_BOOKING_DURATION_TEMPLATE)


@report_blueprint.route(SEARCH_CARS_BP_ROUTE, methods=["GET", "POST"])
@login_required
def search_cars():
    form = SearchCarsForm()
    if request.method == "POST" and form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        return handle_search_cars_post(start_date, end_date, form)

    return render_search_form_with_errors(form)


def handle_search_cars_post(start_date, end_date, form):
    available_cars = fetch_available_cars(start_date, end_date)
    start_date_formatted = format_date(start_date)
    end_date_formatted = format_date(end_date)

    return render_template(
        SEARCH_AVAIALBLE_CARS_TEMPLATE,
        cars=available_cars,
        start_date=start_date_formatted,
        end_date=end_date_formatted,
        form=form,
    )


def fetch_available_cars(start_date, end_date):
    available_cars = (
        Car.query.filter(
            ~Car.bookings.any(
                (Booking.start_date <= end_date)
                & (Booking.end_date >= start_date)
                & (Booking.status != "Отказ")
                & (Booking.status != "Завершено")
            )
        )
        .filter_by(is_deleted=False)
        .all()
    )

    for car in available_cars:
        car.last_booking_info = get_formatted_last_booking(car.id, start_date)
        car.next_booking_info = get_formatted_next_booking(car.id, end_date)

    return available_cars


def get_formatted_last_booking(car_id, start_date):
    last_booking = (
        Booking.query.filter(Booking.car_id == car_id, Booking.end_date < start_date)
        .order_by(Booking.end_date.desc())
        .first()
    )

    return format_booking_dates(last_booking) if last_booking else None


def get_formatted_next_booking(car_id, end_date):
    next_booking = (
        Booking.query.filter(Booking.car_id == car_id, Booking.start_date >= end_date)
        .order_by(Booking.start_date.asc())
        .first()
    )

    return format_booking_dates(next_booking) if next_booking else None


def format_booking_dates(booking):
    booking.start_date_formatted = format_date(booking.start_date)
    booking.end_date_formatted = format_date(booking.end_date)
    return booking


def format_date(date):
    return date.strftime("%d.%m.%Y %H:%M")


def render_search_form_with_errors(form):
    errors = form.errors
    return render_template(SEARCH_AVAIALBLE_CARS_TEMPLATE, form=form, errors=errors)
