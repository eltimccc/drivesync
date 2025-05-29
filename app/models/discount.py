from datetime import datetime, timezone
from app import db


class CarDiscount(db.Model):
    __tablename__ = 'car_discount'

    id = db.Column(db.Integer, primary_key=True)

    car_id = db.Column(db.Integer, db.ForeignKey("car.id"), nullable=False)
    car = db.relationship("Car", backref=db.backref("discounts", lazy=True))

    discount_percent = db.Column(db.Integer, nullable=False, default=5)
    reason = db.Column(db.String(255), default="Простой более 10 дней")

    start_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    end_date = db.Column(db.DateTime, nullable=False)

    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<CarDiscount car_id={self.car_id} {self.discount_percent}% active={self.is_active}>"
