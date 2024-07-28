from datetime import datetime, timedelta, timezone
import random
from app import create_app, db
from app.models import Booking


def generate_dates(start_date, num_days=130):
    bookings = []
    available_cars = list(range(1, 38))

    for day in range(num_days):
        # Количество свободных машин в текущий день (от 2 до 10)
        num_free_cars = random.randint(2, 10)
        booked_cars = random.sample(available_cars, len(available_cars) - num_free_cars)

        for car_id in booked_cars:
            # Продолжительность бронирования от 1 до 9 дней
            booking_duration = random.randint(1, 9)
            start_time = start_date + timedelta(days=day)
            end_time = start_time + timedelta(days=booking_duration)

            bookings.append(
                {
                    "car_id": car_id,
                    "user_id": (car_id % 10) + 1,  # Пример распределения пользователей
                    "phone": "89212124050",
                    "description": f"Booking for car {car_id}",
                    "start_date": start_time,
                    "end_date": end_time,
                    "status": "Аренда",
                }
            )

    return bookings


def add_bookings():
    app = create_app()  # Создаем экземпляр приложения
    with app.app_context():
        start_date = datetime.now(timezone.utc)
        bookings_data = generate_dates(
            start_date, 30
        )  # Генерация бронирований на 30 дней вперед

        for booking_info in bookings_data:
            booking = Booking(**booking_info)
            db.session.add(booking)

        db.session.commit()
        print("Бронирования успешно добавлены.")


if __name__ == "__main__":
    add_bookings()
