from datetime import datetime
from app.models import Booking
from app.models import Car
from app import db


def get_selected_date(date_str, date_format="%d.%m.%Y"):
    if date_str:
        try:
            return datetime.strptime(date_str, date_format).date(), None
        except ValueError:
            return None, "Invalid date format. Use '{}'.".format(date_format)
    return datetime.today().date(), None


def get_bookings_for_date(selected_date):
    pick_ups = (
        db.session.query(Booking)
        .join(Car)
        .filter(
            db.func.date(Booking.start_date) == selected_date, Booking.status != "Отказ"
        )
        .all()
    )

    drop_offs = (
        db.session.query(Booking)
        .join(Car)
        .filter(
            db.func.date(Booking.end_date) == selected_date, Booking.status != "Отказ"
        )
        .all()
    )

    return pick_ups, drop_offs
