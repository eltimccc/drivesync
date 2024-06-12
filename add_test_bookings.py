from datetime import datetime, timedelta, timezone
from random import randint
from app import create_app, db
from app.models import Booking


def create_test_bookings(car_id=1, num_bookings=100):
    start_date = datetime(2024, 6, 6, tzinfo=timezone.utc)

    for i in range(num_bookings):
        days_to_add = randint(0, 30)
        duration_days = randint(1, 14)

        booking_start = start_date + timedelta(days=days_to_add)
        booking_end = booking_start + timedelta(days=duration_days)

        booking = Booking(
            car_id=car_id,
            user_id=randint(
                1, 10
            ),
            phone=f"8921{randint(1000000, 9999999)}",
            description=f"Test booking {i+1}",
            start_date=booking_start,
            end_date=booking_end,
            status="Аренда",
            created_at=datetime.now(timezone.utc),
        )

        db.session.add(booking)

    db.session.commit()
    print(f"{num_bookings} test bookings added.")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        create_test_bookings()
