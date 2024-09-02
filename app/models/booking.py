from datetime import datetime, timezone
from app import db


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey("car.id"), nullable=False)
    car = db.relationship("Car", backref=db.backref("bookings", lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("bookings", lazy=True))
    phone = db.Column(db.String(20), default="89212124050")
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Бронь")
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)

    def update_status(self, new_status):
        self.status = new_status

    def __repr__(self):
        return f"'{self.start_date}', '{self.end_date}', '{self.status}'"
