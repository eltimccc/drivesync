from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.api.serializers.booking import serialize_bookings
from app.api.services.booking_services import get_bookings_for_date, get_selected_date


bookings_api = Blueprint("bookings_api", __name__)


@bookings_api.route("/api/bookings/today", methods=["GET", "POST"])
@jwt_required()
def bookings_today_api():
    """
    API-метод для получения списка бронирований на указанную дату.

    - GET: получает дату из параметров запроса.
    - POST: получает дату из тела запроса в формате JSON.

    Если дата не указана, возвращает бронирования на текущую дату.

    Returns:
        json: Список бронирований на выбранную дату, разделенный на pick_ups и drop_offs.
    """

    date_str = (
        request.get_json().get("selected_date")
        if request.method == "POST"
        else request.args.get("selected_date")
    )

    selected_date, error = get_selected_date(date_str)
    if error:
        return jsonify({"error": error}), 400

    pick_ups, drop_offs = get_bookings_for_date(selected_date)

    return (
        jsonify(
            {
                "selected_date": selected_date.strftime("%d.%m.%Y"),
                "pick_ups": serialize_bookings(pick_ups),
                "drop_offs": serialize_bookings(drop_offs),
            }
        ),
        200,
    )
