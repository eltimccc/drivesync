from app import db

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    car_number = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"Car('{self.brand}', '{self.car_number}')"

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    car = db.relationship('Car', backref=db.backref('bookings', lazy=True))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=True)
    extendable = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"Booking('{self.car.car_number}', '{self.start_date}', '{self.end_date}')"