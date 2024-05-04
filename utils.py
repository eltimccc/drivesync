from datetime import datetime, timedelta

from flask import jsonify, redirect, render_template, request, url_for

from forms import BookingForm
from models import Booking, Car
from app import db

BOOKING_STATUSES = {
    "Аренда": "#007bff",  # Синий цвет
    "Завершено": "#28a745",  # Зеленый цвет
    "Отказ": "#dc3545",  # Красный цвет
    "Ожидание": "#ffc107",  # Желтый цвет
}


def add_booking_post():
    try:
        start_datetime = request.form.get("start_datetime")
        start_datetime = datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M")

        end_datetime = request.form.get("end_datetime")
        end_datetime = datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M")

        current_datetime = datetime.now()
        current_datetime = current_datetime.replace(
            second=0, microsecond=0, minute=0, hour=0
        )

        if start_datetime < current_datetime:
            raise ValueError(
                "Дата начала бронирования не может быть раньше текущей даты"
            )

        if start_datetime >= end_datetime:
            raise ValueError(
                "Дата начала не может быть больше даты окончания бронирования "
            )

        car_id = request.form.get("car")
        description = request.form.get("description")
        phone = request.form.get("phone")
        car = Car.query.get(car_id)

        if car is None:
            raise ValueError("Нужно выбрать машину")

        new_booking = Booking(
            start_date=start_datetime,
            end_date=end_datetime,
            car=car,
            phone=phone,
            description=description,
        )
        db.session.add(new_booking)
        db.session.commit()
        return redirect(url_for("get_bookings"))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred"}), 500


# def add_booking_post():
#     form = BookingForm()
#     if form.validate_on_submit():
#         try:
#             new_booking = Booking(
#                 start_date=form.start_datetime.data,
#                 end_date=form.end_datetime.data,
#                 car_id=form.car_id.data,
#                 phone=form.phone.data,
#                 description=form.description.data
#             )
#             db.session.add(new_booking)
#             db.session.commit()
#             return jsonify({"success": "Booking added successfully"}), 200
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({"error": "An error occurred"}), 500
#     else:
#         errors = {field: error[0] for field, error in form.errors.items()}
#         return jsonify({"errors": errors}), 400


def add_booking_get():
    car_id = request.args.get("car_id")
    start_datetime = request.args.get("start_datetime")
    end_datetime = request.args.get("end_datetime")
    cars = Car.query.filter_by(is_deleted=False).all()

    if car_id and start_datetime and end_datetime:
        return render_template(
            "add_booking.html",
            cars=cars,
            car_id=car_id,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )
    elif request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render_template("add_booking_modal.html", cars=cars)
    else:
        return render_template("add_booking.html", cars=cars, bootstrap=True)
