from flask import request

from app.models import Booking, Car


def get_sorting_parameters():
    """
    Получает параметры сортировки из запроса и возвращает SQLAlchemy объект для сортировки.

    Параметры сортировки берутся из GET-параметров 'sort_by' и 'sort_order'. 
    Если указанные параметры невалидны, используется сортировка по умолчанию 
    по полю 'created_at' в порядке убывания.

    Returns:
        sqlalchemy.sql.elements.UnaryExpression: Объект для сортировки запроса.
    """

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
