from collections import defaultdict
from datetime import date
import calendar
from flask import (
    flash,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
)
from datetime import datetime, timedelta

from sqlalchemy import and_
from app import app, db
from forms import BookingForm, CarForm, EditCarForm
from models import Booking, Car
from utils import BOOKING_STATUSES, add_booking_get, add_booking_post
from validators import validate_booking_data


@app.route("/", methods=["GET"])
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
            "url": url_for("view_booking", booking_id=booking.id),
            "status_color": BOOKING_STATUSES.get(booking.status, "#007bff"),
        }
        formatted_bookings.append(formatted_booking)

    return render_template(
        "calendar_with_bookings.html",
        bookings=formatted_bookings,
        BOOKING_STATUSES=BOOKING_STATUSES,
    )


@app.route("/add_booking", methods=["GET", "POST"])
def add_booking():
    if request.method == "POST":
        return add_booking_post()
    else:
        return add_booking_get()


@app.route("/delete_booking/<int:booking_id>/", methods=["POST"])
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    return redirect(url_for("get_bookings"))


@app.route("/booking/<int:booking_id>/edit", methods=["GET", "POST"])
def edit_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    cars = Car.query.filter_by(is_deleted=False).all()
    status_choices = list(BOOKING_STATUSES.keys())
    errors = {}

    if request.method == "POST":
        try:
            description = request.form["description"]
            phone = request.form["phone"]
            start_date = datetime.strptime(request.form["start_date"], "%Y-%m-%dT%H:%M")
            end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%dT%H:%M")
            car_id = request.form.get("car")
            car = Car.query.get(car_id)
            new_status = request.form.get("status")

            # validate_booking_data(start_date, end_date, car)

            booking.description = description
            booking.phone = phone
            booking.start_date = start_date
            booking.end_date = end_date
            booking.car = car

            if new_status in status_choices:
                booking.status = new_status
                booking.color = BOOKING_STATUSES[new_status]
                if booking.color == BOOKING_STATUSES["Отказ"]:
                    booking.end_date = booking.start_date

            db.session.commit()
            flash("Бронирование успешно обновлено", "success")
            return redirect(url_for("get_bookings", booking_id=booking.id))

        except ValueError as e:
            errors["validation_error"] = str(e)

    return render_template(
        "edit_booking.html",
        booking=booking,
        cars=cars,
        status_choices=status_choices,
        booking_statuses=BOOKING_STATUSES,
        errors=errors,
    )


@app.route("/add_car", methods=["GET", "POST"])
def add_car():
    form = CarForm()
    if form.validate_on_submit() and request.method == "POST":
        try:
            new_car = Car(
                brand=form.brand.data,
                car_number=form.car_number.data,
                transmission=form.transmission.data,
            )
            db.session.add(new_car)
            db.session.commit()
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"message": "Машина успешно добавлена!"})
            else:
                return redirect(url_for("get_cars"))
        except Exception as e:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"error": str(e)}), 500
            else:
                return redirect(url_for("get_cars"))
    else:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return render_template("add_car_modal.html", form=form)
        else:
            return render_template("add_car.html", form=form)


@app.route("/cars")
def get_cars():
    is_deleted_param = request.args.get("is_deleted")

    if is_deleted_param == "true":
        cars = Car.query.filter_by(is_deleted=True).all()
    else:
        cars = Car.query.filter_by(is_deleted=False).all()

    return render_template("cars.html", cars=cars)


@app.route("/car/<int:car_id>")
def car_detail(car_id):
    car = Car.query.get(car_id)

    bookings = Booking.query.filter_by(car_id=car_id).all()

    return render_template("car_detail.html", car=car, bookings=bookings)


# @app.route("/cars/<int:car_id>/edit", methods=["GET", "POST"])
# def edit_car(car_id):
#     car = Car.query.get_or_404(car_id)
#     if request.method == "POST":
#         car.brand = request.form["brand"]
#         car.car_number = request.form["car_number"]
#         car.transmission = request.form["transmission"]

#         is_deleted = request.form.get("is_deleted", "0")
#         car.is_deleted = is_deleted == "1"

#         db.session.commit()
#         return redirect(url_for("get_cars"))
#     return render_template("edit_car.html", car=car)

@app.route("/cars/<int:car_id>/edit", methods=["GET", "POST"])
def edit_car(car_id):
    car = Car.query.get_or_404(car_id)
    form = EditCarForm(obj=car)
    if form.validate_on_submit():
        form.populate_obj(car)
        db.session.commit()
        return redirect(url_for("get_cars"))
    return render_template("edit_car.html", form=form, car=car)


@app.route("/cars/<int:car_id>/delete", methods=["POST"])
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    car.is_deleted = True
    db.session.commit()
    return redirect(url_for("get_cars"))


@app.route("/booking/<int:booking_id>", methods=["GET"])
def view_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    status_color = BOOKING_STATUSES.get(booking.status, "#ffffff")
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render_template(
            "view_booking_modal.html", booking=booking, status_color=status_color
        )
    else:
        return render_template(
            "view_booking.html", booking=booking, status_color=status_color
        )


@app.template_filter("month_name")
def month_name(month_number):
    return calendar.month_name[month_number]


@app.route("/c")
def booking_calendar():
    cars = Car.query.all()
    bookings = Booking.query.all()

    current_date = datetime.now()

    num_months = 12
    months = []
    for i in range(num_months):
        year = current_date.year
        month = current_date.month + i
        if month > 12:
            month -= 12
            year += 1
        days_in_month = calendar.monthrange(year, month)[1]
        months.append(
            {
                "year": year,
                "month": month,
                "days": range(1, days_in_month + 1),
                "name": calendar.month_name[month],
            }
        )

    return render_template(
        "booking_table.html",
        cars=cars,
        bookings=bookings,
        months=months,
        num_months=num_months,
        booking_statuses_colors=BOOKING_STATUSES,
    )


def generate_dates():
    today = datetime.today()
    start_date_past = today - timedelta(days=365)
    end_date_future = today + timedelta(days=183)

    dates = []

    while start_date_past < today:
        dates.append(start_date_past.strftime("%a, %d, %Y "))

        start_date_past += timedelta(days=1)

    while today < end_date_future:
        dates.append(today.strftime("%a, %d, %Y"))
        today += timedelta(days=1)

    return dates


@app.route("/q", methods=["GET"])
def q():
    dates = generate_dates()
    today = datetime.today()
    current_year = today.year
    current_month = today.strftime("%B")
    cars = Car.query.all()

    return render_template(
        "q.html",
        dates=dates,
        today=today,
        current_year=current_year,
        current_month=current_month,
        cars=cars,
    )


@app.route("/report_all_bookings", methods=["GET", "POST"])
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
            "reports/report_all_bookings.html",
            start_date=start_date_formatted,
            end_date=end_date_formatted,
            bookings_count=len(bookings),
            bookings_completed=bookings_completed,
            bookings_by_status=bookings_by_status,
            booking_statuses=BOOKING_STATUSES,
        )

    return render_template("reports/report_all_bookings.html")


@app.route("/report_rent_amount", methods=["GET", "POST"])
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
            "reports/report_rent_amount.html",
            start_date=start_date_formatted,
            end_date=end_date_formatted,
            cars_booked=cars_booked,
        )

    return render_template("reports/report_rent_amount.html")


@app.route("/report_status_rent", methods=["GET", "POST"])
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
            "reports/report_status_rent.html",
            start_date=start_date_formatted,
            end_date=end_date_formatted,
            cars_status=cars_status,
        )

    return render_template("reports/report_status_rent.html")


@app.route("/report_booking_duration", methods=["GET", "POST"])
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
                Booking.end_date >= start_date
            ).all()

            car_duration = timedelta()
            for booking in bookings:
                intersection_start = booking.start_date if booking.start_date >= start_date else start_date
                intersection_end = booking.end_date if booking.end_date <= end_date else end_date
                duration = intersection_end - intersection_start
                car_duration += duration

            cars_duration[car] = car_duration
            total_duration += car_duration

        total_hours = total_duration.total_seconds() // 3600
        total_minutes = (total_duration.total_seconds() % 3600) // 60
        total_duration_str = f"{int(total_hours)} часов {int(total_minutes)} минут"

        return render_template(
            "reports/report_booking_duration.html",
            start_date=start_date_str,
            end_date=end_date_str,
            cars_duration=cars_duration,
            total_duration=total_duration_str
        )

    return render_template("reports/report_booking_duration.html")


@app.route("/reports_page", methods=["GET"])
def reports_page():
    return render_template("reports/reports.html")


@app.route("/search_cars", methods=["GET", "POST"])
def search_cars():
    if request.method == "POST":
        start_date = datetime.fromisoformat(request.form.get("start_date"))
        end_date = datetime.fromisoformat(request.form.get("end_date"))

        # Находим доступные автомобили на заданный период
        available_cars = Car.query.filter(~Car.bookings.any(
            (Booking.start_date <= end_date) & (Booking.end_date >= start_date)
        )).all()

        # Для каждого автомобиля находим последнее бронирование перед start_date
        for car in available_cars:
            last_booking = Booking.query.filter(
                Booking.car_id == car.id,
                Booking.end_date < start_date
            ).order_by(Booking.end_date.desc()).first()

            if last_booking:
                # Форматируем даты последнего бронирования
                last_booking.start_date_formatted = last_booking.start_date.strftime("%d.%m.%Y %H:%M")
                last_booking.end_date_formatted = last_booking.end_date.strftime("%d.%m.%Y %H:%M")

                # Добавляем информацию о последнем бронировании к объекту автомобиля
                car.last_booking_info = last_booking

            # Находим следующее бронирование после end_date
            next_booking = Booking.query.filter(
                Booking.car_id == car.id,
                Booking.start_date >= end_date
            ).order_by(Booking.start_date.asc()).first()

            if next_booking:
                # Форматируем даты следующего бронирования
                next_booking.start_date_formatted = next_booking.start_date.strftime("%d.%m.%Y %H:%M")
                next_booking.end_date_formatted = next_booking.end_date.strftime("%d.%m.%Y %H:%M")

                # Добавляем информацию о следующем бронировании к объекту автомобиля
                car.next_booking_info = next_booking

        start_date_formatted = start_date.strftime("%d.%m.%Y %H:%M")
        end_date_formatted = end_date.strftime("%d.%m.%Y %H:%M")
        
        return render_template("available_cars.html", cars=available_cars, start_date=start_date_formatted, end_date=end_date_formatted)
    else:
        # Если метод GET, просто отображаем форму без автомобилей
        return render_template("available_cars.html")

