from drivesync.app import db


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    car_number = db.Column(db.String(20), unique=True, nullable=False)
    transmission = db.Column(db.String(100), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Car('{self.brand}', '{self.car_number}')"


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey("car.id"), nullable=False)
    car = db.relationship("Car", backref=db.backref("bookings", lazy=True))
    phone = db.Column(db.String(20), default=89212124050)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Аренда")

    def update_status(self, new_status):
        self.status = new_status

    def __repr__(self):
        return f"'{self.start_date}', '{self.end_date}', '{self.status}'"