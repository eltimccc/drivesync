from flask import render_template, request, jsonify, redirect, url_for
from datetime import datetime
from app import app, db
from models import Booking, Car


@app.route('/', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()
    formatted_bookings = []

    for booking in bookings:
        car_brand = booking.car.brand
        car_number = booking.car.car_number

        formatted_booking = {
            'id': booking.id,
            'car': f'{car_brand}: {car_number}',
            'start': booking.start_date,
            'end': booking.end_date,
            'url': url_for('view_booking', booking_id=booking.id)
        }
        formatted_bookings.append(formatted_booking)

    return render_template('calendar_with_bookings.html', bookings=formatted_bookings)
    

@app.route('/add_booking', methods=['GET', 'POST'])
def add_booking():
    if request.method == 'POST':
        try:
            start_datetime = request.form.get('start_datetime')
            start_datetime = datetime.strptime(start_datetime, '%Y-%m-%dT%H:%M')

            end_datetime = request.form.get('end_datetime')
            end_datetime = datetime.strptime(end_datetime, '%Y-%m-%dT%H:%M')

            car_id = request.form.get('car_id')
            description = request.form.get('description')

            car = Car.query.get(car_id)

            if car is None:
                raise ValueError('Car not found')

            new_booking = Booking(start_date=start_datetime, end_date=end_datetime, car=car, description=description)
            db.session.add(new_booking)
            db.session.commit()
            return jsonify({'message': 'Booking added successfully'}), 200
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


@app.route('/booking/<int:booking_id>')
def view_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template('view_booking.html', booking=booking)



@app.route('/me', methods=['GET'])
def get_me():
    return render_template('index.html') 
