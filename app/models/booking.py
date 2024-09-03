from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime, timezone

db = SQLAlchemy()

class BookingBase(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey("car.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    phone = db.Column(db.String(20), default="89212124050")
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="Бронь")
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    @declared_attr
    def car(cls):
        return db.relationship("Car", backref=db.backref("bookings", lazy=True))

    @declared_attr
    def user(cls):
        return db.relationship("User", backref=db.backref("bookings", lazy=True))

class Booking(BookingBase):
    __tablename__ = 'bookings'

    def update_status(self, new_status):
        self.status = new_status

    def __repr__(self):
        return f"'{self.start_date}', '{self.end_date}', '{self.status}'"

class DeletedBooking(BookingBase):
    __tablename__ = 'deleted_bookings'

    original_booking_id = db.Column(db.Integer, nullable=False)
    deleted_by_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    deleted_by_user = db.relationship("User")
    deleted_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
