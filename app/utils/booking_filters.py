# from datetime import datetime
from flask import request

from app.models import Booking, Car


def get_sorting_parameters():
    sort_by = request.args.get("sort_by", "created_at")
    sort_order = request.args.get("sort_order", "desc")

    valid_sort_columns = {
        "created_at": Booking.created_at,
        "start_date": Booking.start_date,
        "end_date": Booking.end_date,
        "car_number": Car.car_number,
        "transmission": Car.transmission,
        "id": Booking.id,
        "car_id": Booking.car_id,
        "phone": Booking.phone,
        "user_id": Booking.user_id,
    }

    if sort_by not in valid_sort_columns:
        sort_by = "created_at"

    sort_column = valid_sort_columns[sort_by]
    sort_direction = sort_column.desc() if sort_order == "desc" else sort_column.asc()

    return sort_direction
