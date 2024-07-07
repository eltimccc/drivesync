from datetime import datetime, timezone
from app import create_app, db
from app.models import Booking


def generate_fixed_bookings():
    bookings = [
        {
            "user_id": 1,
            "car_id": 1,
            "start_date": "26.06.2024 10:00",
            "end_date": "29.06.2024 10:00",
            "phone": "89117157791",
            "description": "Никифоров Сергей (ждем доки)",
        },
        {
            "user_id": 1,
            "car_id": 6,
            "start_date": "26.06.2024 23:20",
            "end_date": "28.06.2024 23:20",
            "phone": "89812490734",
            "description": "Ждем доки подтвердить",
        },
        {
            "user_id": 1,
            "car_id": 4,
            "start_date": "10.06.2024 18:30",
            "end_date": "10.07.2024 23:20",
            "phone": "8123456",
            "description": "Андрюковская - продляет",
        },
        {
            "user_id": 1,
            "car_id": 5,
            "start_date": "10.06.2024 18:30",
            "end_date": "01.07.2024 23:20",
            "phone": "8123456",
            "description": "Зевякин Игорь - продляет",
        },
        {
            "user_id": 1,
            "car_id": 7,
            "start_date": "20.06.2024 18:30",
            "end_date": "30.06.2024 23:20",
            "phone": "+37129293641",
            "description": "Андрей - продляет",
        },
        {
            "user_id": 1,
            "car_id": 8,
            "start_date": "25.06.2024 18:30",
            "end_date": "28.06.2024 23:20",
            "phone": "8123456",
            "description": "Гаврилова Ксения",
        },
        {
            "user_id": 1,
            "car_id": 9,
            "start_date": "22.06.2024 17:00",
            "end_date": "25.06.2024 17:00",
            "phone": "8123456",
            "description": "Король Анна",
        },
        {
            "user_id": 1,
            "car_id": 9,
            "start_date": "26.06.2024 17:00",
            "end_date": "29.06.2024 17:00",
            "phone": "+31634136945",
            "description": "Алена Рошильдина",
        },
        {
            "user_id": 1,
            "car_id": 10,
            "start_date": "15.06.2024 17:00",
            "end_date": "29.06.2024 18:20",
            "phone": "8123456",
            "description": "Неизвестно",
        },
        {
            "user_id": 1,
            "car_id": 11,
            "start_date": "24.06.2024 09:00",
            "end_date": "26.06.2024 09:00",
            "phone": "+31634136945",
            "description": "Алена Рошильдина",
        },
        {
            "user_id": 1,
            "car_id": 21,
            "start_date": "04.07.2024 09:00",
            "end_date": "06.07.2024 09:00",
            "phone": "89044921250",
            "description": "Козинцев Дмитрий",
        },
        {
            "user_id": 1,
            "car_id": 20,
            "start_date": "03.07.2024 09:00",
            "end_date": "05.07.2024 16:00",
            "phone": "8123456",
            "description": "Любимова Звенигородская жена",
        },
        {
            "user_id": 1,
            "car_id": 20,
            "start_date": "03.07.2024 16:00",
            "end_date": "05.07.2024 16:00",
            "phone": "8123456",
            "description": "Ушаков Виктор",
        },
        {
            "user_id": 1,
            "car_id": 20,
            "start_date": "10.07.2024 20:10",
            "end_date": "20.07.2024 16:00",
            "phone": "89211031313",
            "description": "Сергей Иванов сдача Аэропорт +бустер + кресло",
        },
        {
            "user_id": 1,
            "car_id": 13,
            "start_date": "01.07.2024 16:00",
            "end_date": "30.07.2024 16:00",
            "phone": "8123456",
            "description": "Гутковский",
        },
        {
            "user_id": 1,
            "car_id": 14,
            "start_date": "01.07.2024 16:00",
            "end_date": "31.07.2024 14:00",
            "phone": "8123456",
            "description": "Иванов",
        },
        {
            "user_id": 1,
            "car_id": 15,
            "start_date": "01.07.2024 16:00",
            "end_date": "30.07.2024 16:00",
            "phone": "8123456",
            "description": "ООО Континент",
        },
        {
            "user_id": 1,
            "car_id": 16,
            "start_date": "20.06.2024 11:00",
            "end_date": "07.07.2024 11:00",
            "phone": "8123456",
            "description": "Елена Смелова",
        },
        {
            "user_id": 1,
            "car_id": 18,
            "start_date": "20.06.2024 11:00",
            "end_date": "30.07.2024 11:00",
            "phone": "8123456",
            "description": "ООО Континент",
        },
        {
            "user_id": 1,
            "car_id": 12,
            "start_date": "20.06.2024 11:00",
            "end_date": "30.07.2024 11:00",
            "phone": "8123456",
            "description": "ООО Континент",
        },
        {
            "user_id": 1,
            "car_id": 22,
            "start_date": "01.07.2024 11:00",
            "end_date": "22.07.2024 11:00",
            "phone": "89113666442",
            "description": "Мария 5%",
        },
        {
            "user_id": 1,
            "car_id": 23,
            "start_date": "01.07.2024 21:00",
            "end_date": "06.07.2024 21:00",
            "phone": "8123456",
            "description": "Павел",
        },
        {
            "user_id": 1,
            "car_id": 21,
            "start_date": "29.07.2024 14:00",
            "end_date": "05.08.2024 09:00",
            "phone": "+37254790603",
            "description": "Михайлов Борис",
        },
        {
            "user_id": 1,
            "car_id": 1,
            "start_date": "04.07.2024 11:00",
            "end_date": "10.07.2024 18:00",
            "phone": "8123456",
            "description": "Федоров Дмитрий",
        },
        {
            "user_id": 1,
            "car_id": 1,
            "start_date": "13.07.2024 09:00",
            "end_date": "16.07.2024 09:00",
            "phone": "89113719410",
            "description": "Петрова Наталья",
        },
        {
            "user_id": 1,
            "car_id": 3,
            "start_date": "04.06.2024 11:00",
            "end_date": "06.07.2024 18:00",
            "phone": "8123456",
            "description": "Кузьмин",
        },
        {
            "user_id": 1,
            "car_id": 6,
            "start_date": "01.07.2024 09:00",
            "end_date": "04.07.2024 18:00",
            "phone": "8123456",
            "description": "Павел",
        },
        {
            "user_id": 1,
            "car_id": 6,
            "start_date": "06.07.2024 09:00",
            "end_date": "11.07.2024 14:00",
            "phone": "8123456",
            "description": "Малашина Надежда (после обеда)",
        },
        {
            "user_id": 1,
            "car_id": 4,
            "start_date": "01.07.2024 09:00",
            "end_date": "07.07.2024 15:00",
            "phone": "8123456",
            "description": "Абакин Павел",
        },
        {
            "user_id": 1,
            "car_id": 4,
            "start_date": "07.07.2024 21:00",
            "end_date": "08.07.2024 21:00",
            "phone": "89114694389",
            "description": "Тищук",
        },
        {
            "user_id": 1,
            "car_id": 4,
            "start_date": "09.07.2024 21:00",
            "end_date": "16.07.2024 21:00",
            "phone": "8123456",
            "description": "Андрюковская 5%",
        },
        {
            "user_id": 1,
            "car_id": 5,
            "start_date": "04.07.2024 09:00",
            "end_date": "05.07.2024 09:00",
            "phone": "89113723452",
            "description": "Сулейманова",
        },
        {
            "user_id": 1,
            "car_id": 5,
            "start_date": "06.07.2024 09:00",
            "end_date": "08.07.2024 09:00",
            "phone": "89113723452",
            "description": "Борланов",
        },
        {
            "user_id": 1,
            "car_id": 5,
            "start_date": "08.07.2024 10:00",
            "end_date": "20.07.2024 10:00",
            "phone": "89113723452",
            "description": "Зевякин",
        },
        {
            "user_id": 1,
            "car_id": 7,
            "start_date": "04.07.2024 18:30",
            "end_date": "13.07.2024 23:20",
            "phone": "+37258169062",
            "description": "Резану Сергей",
        },
        {
            "user_id": 1,
            "car_id": 7,
            "start_date": "15.07.2024 18:30",
            "end_date": "22.07.2024 23:20",
            "phone": "8123456",
            "description": "Семенюга ...",
        },
        {
            "user_id": 1,
            "car_id": 8,
            "start_date": "01.07.2024 18:30",
            "end_date": "05.07.2024 15:00",
            "phone": "8123456",
            "description": "Удовенко Сергей",
        },
        {
            "user_id": 1,
            "car_id": 8,
            "start_date": "06.07.2024 18:30",
            "end_date": "22.07.2024 15:00",
            "phone": "8123456",
            "description": "Вера Савельева",
        },
        {
            "user_id": 1,
            "car_id": 9,
            "start_date": "07.07.2024 08:30",
            "end_date": "08.07.2024 08:30",
            "phone": "8123456",
            "description": "Зевякин",
        },
        {
            "user_id": 1,
            "car_id": 9,
            "start_date": "11.07.2024 09:00",
            "end_date": "13.07.2024 09:00",
            "phone": "89166140220",
            "description": "Юлия Солнцев Андрей",
        },
        {
            "user_id": 1,
            "car_id": 10,
            "start_date": "05.07.2024 11:00",
            "end_date": "30.08.2024 11:00",
            "phone": "8123456",
            "description": "Сергей Игонин 25 дней",
        },
    ]

    return bookings


def add_bookings():
    app = create_app()  # Создаем экземпляр приложения
    with app.app_context():
        bookings_data = (
            generate_fixed_bookings()
        )  # Используем фиксированные бронирования

        for booking_info in bookings_data:
            start_date = datetime.strptime(
                booking_info["start_date"], "%d.%m.%Y %H:%M"
            ).replace(tzinfo=timezone.utc)
            end_date = datetime.strptime(
                booking_info["end_date"], "%d.%m.%Y %H:%M"
            ).replace(tzinfo=timezone.utc)
            booking = Booking(
                user_id=booking_info["user_id"],
                car_id=booking_info["car_id"],
                start_date=start_date,
                end_date=end_date,
                phone=booking_info["phone"],
                description=booking_info["description"],
                status="Аренда",
            )
            db.session.add(booking)

        db.session.commit()
        print("Бронирования успешно добавлены.")


if __name__ == "__main__":
    add_bookings()
