from flask import Flask, jsonify, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    car_number = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"Car('{self.brand}', '{self.number_plate}')"
    

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    car = db.relationship('Car', backref=db.backref('bookings', lazy=True))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=True)
    extendable = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"Booking('{self.car.number_plate}', '{self.start_date}', '{self.end_date}')"



with app.app_context():
    db.create_all()

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



if __name__ == '__main__':
    app.run(debug=True)
