from flask import Blueprint, render_template, url_for

from app.models import Booking
from app.utils.utils import BOOKING_STATUSES
from app.constants import BOOKING_VIEW_BOOKING_ROUTE, MAIN_TEMPLATE

main = Blueprint('main', __name__)


@main.route("/", methods=["GET"])
def get_bookings():
    bookings = Booking.query.all()
    formatted_bookings = []

    for booking in bookings:
        car_brand = booking.car.brand
        car_number = booking.car.car_number

        formatted_booking = {
            "id": booking.id,
            "car": f"{car_brand}: {car_number}",
            "start": booking.start_date,
            "end": booking.end_date,
            "url": url_for(BOOKING_VIEW_BOOKING_ROUTE, booking_id=booking.id),
            "status_color": BOOKING_STATUSES.get(booking.status, "#007bff"),
        }
        formatted_bookings.append(formatted_booking)

    return render_template(
        MAIN_TEMPLATE,
        bookings=formatted_bookings,
        BOOKING_STATUSES=BOOKING_STATUSES,
    )