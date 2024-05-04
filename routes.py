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
from app import app, db
from forms import BookingForm, CarForm
from models import Booking, Car
from utils import BOOKING_STATUSES, add_booking_get, add_booking_post


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
    cars = Car.query.all()
    status_choices = list(BOOKING_STATUSES.keys())

    if request.method == "POST":
        booking.description = request.form["description"]
        booking.phone = request.form["phone"]
        booking.start_date = datetime.strptime(
            request.form["start_date"], "%Y-%m-%dT%H:%M"
        )
        booking.end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%dT%H:%M")
        car_id = request.form.get("car")
        booking.car = Car.query.get(car_id)

        new_status = request.form.get("status")

        if new_status in status_choices:
            booking.status = new_status
            booking.color = BOOKING_STATUSES[new_status]
            if booking.color == BOOKING_STATUSES["Отказ"]:
                booking.end_date = booking.start_date

        db.session.commit()
        return redirect(url_for("get_bookings", booking_id=booking.id))

    return render_template(
        "edit_booking.html",
        booking=booking,
        cars=cars,
        status_choices=status_choices,
        booking_statuses=BOOKING_STATUSES,
    )


@app.route("/add_car", methods=["GET", "POST"])
def add_car():
    form = CarForm()
    if form.validate_on_submit() and request.method == "POST":
        try:
            new_car = Car(
                brand=form.brand.data,
                car_number=form.car_number.data,
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


@app.route("/cars/<int:car_id>/edit", methods=["GET", "POST"])
def edit_car(car_id):
    car = Car.query.get_or_404(car_id)
    if request.method == "POST":
        car.brand = request.form["brand"]
        car.car_number = request.form["car_number"]

        is_deleted = request.form.get("is_deleted", "0")
        car.is_deleted = is_deleted == "1"

        db.session.commit()
        return redirect(url_for("get_cars"))
    return render_template("edit_car.html", car=car)


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


@app.route("/me", methods=["GET"])
def get_me():
    return render_template("index.html")


from datetime import date


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

    return render_template(
        "q.html",
        dates=dates,
        today=today,
        current_year=current_year,
        current_month=current_month,
    )
