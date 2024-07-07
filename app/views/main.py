from datetime import datetime
from flask import Blueprint, render_template, request, url_for, current_app
from flask_login import login_required

from app import db
from app.models import Booking, Car
from app.utils.booking_filters import get_sorting_parameters
from app.utils.utils import BOOKING_STATUSES
from app.constants import BOOKING_ALL_TEMPLATE, BOOKING_VIEW_BOOKING_ROUTE, MAIN_BP_NAME_ROUTE, MAIN_TEMPLATE

main = Blueprint(MAIN_BP_NAME_ROUTE, __name__)


# @main.route("/", methods=["GET"])
# @login_required
# def get_bookings():
#     current_app.logger.info("Accessed main page.")
#     bookings = Booking.query.all()
#     formatted_bookings = []

#     for booking in bookings:
#         car_brand = booking.car.brand
#         car_number = booking.car.car_number

#         formatted_booking = {
#             "id": booking.id,
#             "car": f"{car_brand}: {car_number}",
#             "start": booking.start_date,
#             "end": booking.end_date,
#             "url": url_for(BOOKING_VIEW_BOOKING_ROUTE, booking_id=booking.id),
#             "status_color": BOOKING_STATUSES.get(booking.status, "#007bff"),
#         }
#         formatted_bookings.append(formatted_booking)

#     return render_template(
#         MAIN_TEMPLATE,
#         bookings=formatted_bookings,
#         BOOKING_STATUSES=BOOKING_STATUSES,
#     )

@main.route("/", methods=["GET"])
@login_required
def all_bookings():
    current_app.logger.info("Accessed all bookings page.")
    sort_direction = get_sorting_parameters()
    current_app.logger.debug(f"Sorting bookings in {sort_direction} order")

    query = db.session.query(Booking).join(Car).order_by(sort_direction)
    bookings = query.all()

    current_app.logger.debug(f"Retrieved {len(bookings)} bookings")
    today = datetime.today().date()
    return render_template(
        BOOKING_ALL_TEMPLATE,
        bookings=bookings,
        sort_by=request.args.get("sort_by", "created_at"),
        sort_order=request.args.get("sort_order", "desc"),
        today=today,
    )