from datetime import datetime

from flask import jsonify, redirect, render_template, request, url_for

from forms import BookingForm
from models import Booking, Car
from app import db
from validators import validate_booking_data

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

        car_id = request.form.get("car")
        car = Car.query.get(car_id)
        description = request.form.get("description")
        phone = request.form.get("phone")

        validate_booking_data(start_datetime, end_datetime, car)

        new_booking = Booking(
            start_date=start_datetime,
            end_date=end_datetime,
            car=car,
            phone=phone,
            description=description,
        )
        db.session.add(new_booking)
        db.session.commit()

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"success": "Booking added successfully"})
        else:
            return redirect(url_for("get_bookings"))
    except ValueError as e:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"error": str(e)}), 400
        else:
            return render_template("add_booking.html", error=str(e)), 400
    except Exception as e:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({"error": "An error occurred"}), 500
        else:
            return render_template("add_booking.html", error="An error occurred"), 500


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
