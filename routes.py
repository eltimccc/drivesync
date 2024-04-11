import calendar
from flask import (
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
)
from datetime import datetime
from app import app, db
from forms import BookingForm, EditBookingForm
from models import Booking, Car
from utils import BOOKING_STATUSES


# @app.route("/", methods=["GET"])
# def get_bookings():
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
#             "url": url_for("view_booking", booking_id=booking.id),
#         }
#         formatted_bookings.append(formatted_booking)

#     return render_template("calendar_with_bookings.html", bookings=formatted_bookings)
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
            "status_color": BOOKING_STATUSES.get(booking.status, '#007bff')  # Получение цвета статуса
        }
        formatted_bookings.append(formatted_booking)

    return render_template("calendar_with_bookings.html", bookings=formatted_bookings, BOOKING_STATUSES=BOOKING_STATUSES)



@app.route("/add_booking", methods=["GET", "POST"])
def add_booking():
    if request.method == "POST":
        try:
            start_datetime = request.form.get("start_datetime")
            start_datetime = datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M")

            end_datetime = request.form.get("end_datetime")
            end_datetime = datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M")

            car_id = request.form.get("car")
            description = request.form.get("description")

            car = Car.query.get(car_id)

            if car is None:
                raise ValueError("Car not found")

            new_booking = Booking(
                start_date=start_datetime,
                end_date=end_datetime,
                car=car,
                description=description,
            )
            db.session.add(new_booking)
            db.session.commit()
            return redirect(url_for("get_bookings"))
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            cars = Car.query.all()
            return render_template("add_booking_modal.html", cars=cars)
        else:
            cars = Car.query.all()
            return render_template("add_booking.html", cars=cars, bootstrap=True)


@app.route("/delete_booking/<int:booking_id>/", methods=["POST"])
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    return redirect(url_for("get_bookings"))


# @app.route("/booking/<int:booking_id>/edit", methods=["GET", "POST"])
# def edit_booking(booking_id):
#     booking = Booking.query.get_or_404(booking_id)
#     cars = Car.query.all()
#     new_status = None  # Инициализация переменной

#     if request.method == "POST":
#         booking.description = request.form["description"]
#         booking.start_date = datetime.strptime(
#             request.form["start_date"], "%Y-%m-%dT%H:%M"
#         )
#         booking.end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%dT%H:%M")
#         car_id = request.form.get("car")
#         booking.car = Car.query.get(car_id)

#         new_status = request.form.get("status")
        
#         print(new_status)
#         if new_status in BOOKING_STATUSES.values():
#             booking.status = new_status
#             print(new_status)
        
#         db.session.commit()
#         return redirect(url_for("get_bookings", booking_id=booking.id))

#     return render_template("edit_booking.html", booking=booking, cars=cars, status=new_status, booking_statuses=BOOKING_STATUSES)
@app.route("/booking/<int:booking_id>/edit", methods=["GET", "POST"])
def edit_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    cars = Car.query.all()
    status_choices = list(BOOKING_STATUSES.keys())  # Получение списка ключей (статусов) из словаря

    if request.method == "POST":
        booking.description = request.form["description"]
        booking.start_date = datetime.strptime(
            request.form["start_date"], "%Y-%m-%dT%H:%M"
        )
        booking.end_date = datetime.strptime(request.form["end_date"], "%Y-%m-%dT%H:%M")
        car_id = request.form.get("car")
        booking.car = Car.query.get(car_id)

        new_status = request.form.get("status")
        
        if new_status in status_choices:  # Проверка, что новый статус является допустимым выбором
            booking.status = new_status
            # Обновление цвета статуса
            booking.color = BOOKING_STATUSES[new_status]
        
        db.session.commit()
        return redirect(url_for("get_bookings", booking_id=booking.id))

    return render_template("edit_booking.html", booking=booking, cars=cars, status_choices=status_choices, booking_statuses=BOOKING_STATUSES)

@app.route("/add_car", methods=["GET", "POST"])
def add_car():
    if request.method == "POST":
        try:
            brand = request.form["brand"]
            car_number = request.form["car_number"]

            new_car = Car(brand=brand, car_number=car_number)
            db.session.add(new_car)
            db.session.commit()

            return redirect(url_for("get_bookings"))
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return render_template("add_car_modal.html")
        else:
            return render_template("add_car.html", bootstrap=True)


@app.route("/cars")
def view_cars():
    cars = Car.query.all()
    return render_template("cars.html", cars=cars)


@app.route('/car/<int:car_id>')
def car_detail(car_id):
    car = Car.query.get(car_id)

    bookings = Booking.query.filter_by(car_id=car_id).all()

    return render_template('car_detail.html', car=car, bookings=bookings)


@app.route("/booking/<int:booking_id>", methods=["GET", "POST"])
def view_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template("view_booking.html", booking=booking)


@app.route("/me", methods=["GET"])
def get_me():
    return render_template("index.html")

from datetime import date


# @app.route('/t')
# def booking_calendar():
#     # Получаем список всех автомобилей из базы данных
#     cars = Car.query.all()
#     # Получаем список всех бронирований из базы данных
#     bookings = Booking.query.all()

#     # Создаем список месяцев, которые будем отображать в календаре (например, 6 месяцев)
#     num_months = 6
#     today = date.today()
#     current_year = today.year
#     current_month = today.month
#     months = []
#     for i in range(num_months):
#         year = current_year + (current_month + i - 1) // 12
#         month = (current_month + i) % 12 or 12
#         days_in_month = calendar.monthrange(year, month)[1]  # Используем правильный модуль
#         months.append({'year': year, 'month': month, 'days': range(1, days_in_month + 1)})

#     return render_template('booking_table.html', cars=cars, bookings=bookings, months=months)
@app.template_filter('month_name')
def month_name(month_number):
    return calendar.month_name[month_number]

@app.route('/t')
def booking_calendar():
    # Получаем список всех автомобилей из базы данных
    cars = Car.query.all()
    # Получаем список всех бронирований из базы данных
    bookings = Booking.query.all()

    # Создаем список месяцев, которые будем отображать в календаре (например, 6 месяцев)
    num_months = 6
    today = date.today()
    current_year = today.year
    current_month = today.month
    months = []
    for i in range(num_months):
        year = current_year + (current_month + i - 1) // 12
        month = (current_month + i) % 12 or 12
        days_in_month = calendar.monthrange(year, month)[1]  # Используем правильный модуль
        months.append({'year': year, 'month': month, 'days': range(1, days_in_month + 1), 'name': month_name(month)})

    return render_template('booking_table.html', cars=cars, bookings=bookings, months=months)


