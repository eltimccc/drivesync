from datetime import datetime
from flask import Blueprint, render_template, request, current_app
from flask_login import login_required

from app import db
from app.models import Booking
from app.models import Car
from app.utils.booking_filters import get_sorting_parameters
from app.constants import BOOKING_ALL_TEMPLATE, MAIN_BP_NAME_ROUTE
from app.utils.utils import BOOKING_STATUSES


main_blueprint = Blueprint(MAIN_BP_NAME_ROUTE, __name__, url_prefix="/")


@main_blueprint.route("/", methods=["GET"])
@login_required
def get_bookings():
    """
    Для главной страницы.
    Отображает список всех бронирований с возможностью сортировки.

    Маршрут доступен только для аутентифицированных пользователей. 
    Сортировка бронирований производится на основе GET-параметров 'sort_by' и 'sort_order'.
    В шаблон передаются список бронирований, параметры сортировки, текущая дата и статусы бронирований.
    """

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
        sort_by=request.args.get("sort_by", "start_date"),
        sort_order=request.args.get("sort_order", "asc"),
        today=today,
        BOOKING_STATUSES=BOOKING_STATUSES,
    )