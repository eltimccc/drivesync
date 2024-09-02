from app import db


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    car_number = db.Column(db.String(20), unique=True, nullable=False)
    transmission = db.Column(db.String(100), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Car('{self.brand}', '{self.car_number}')"
