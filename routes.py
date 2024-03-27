from flask import render_template, request, jsonify, redirect, url_for
from datetime import datetime
from app import app, db
from models import Booking, Car

@app.route('/', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()
    for booking in bookings:
        booking.date = datetime.strptime(booking.date, '%d.%m.%Y')
    return render_template('calendar_with_bookings.html', bookings=bookings) 

@app.route('/add_booking', methods=['GET', 'POST'])
def add_booking():
    if request.method == 'POST':
        try:
            booking_date = request.form.get('date')
            booking_date = datetime.strptime(booking_date, '%d.%m.%Y')
            formatted_date = booking_date.strftime('%d.%m.%Y')

            new_booking = Booking(date=formatted_date)
            db.session.add(new_booking)
            db.session.commit()
            return redirect(url_for('get_bookings'))
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return render_template('add_booking.html')

@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        try:
            brand = request.form['brand']
            car_number = request.form['car_number']

            new_car = Car(brand=brand, car_number=car_number)
            db.session.add(new_car)
            db.session.commit()

            return redirect(url_for('get_bookings'))
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return render_template('add_car.html')

@app.route('/me', methods=['GET'])
def get_me():
    return render_template('index.html') 
