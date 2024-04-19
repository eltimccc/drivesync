from app import app, db  # Импортируем объект app из вашего модуля app.py
from models import Car

def add_cars():
    with app.app_context():
        cars_data = [
            {"brand": "Hyundai Creta", "car_number": "467"},
            {"brand": "Kia Rio", "car_number": "116"},
            {"brand": "Kia Rio", "car_number": "157"},
            {"brand": "Kia Rio", "car_number": "088"},
            {"brand": "Kia Rio", "car_number": "355"},
            {"brand": "Hyundai Solaris АКПП", "car_number": "181"},
            {"brand": "Hyundai Solaris МКПП", "car_number": "325"},
            {"brand": "Hyundai Solaris МКПП", "car_number": "645"},
            {"brand": "Hyundai Solaris 1.4", "car_number": "627"},
            {"brand": "Renault Logan", "car_number": "777"},
            {"brand": "Renault Logan", "car_number": "017"},
            {"brand": "Renault Logan", "car_number": "371"},
            {"brand": "Renault Logan", "car_number": "393"},
            {"brand": "Renault Logan", "car_number": "455"},
            {"brand": "Renault Logan", "car_number": "473"},
            {"brand": "Renault Logan", "car_number": "712"},
            {"brand": "Renault Logan", "car_number": "750"},
            {"brand": "Lada Largus", "car_number": "440"},
            {"brand": "Lada Granta АКПП", "car_number": "235"},
            {"brand": "Lada Granta АКПП", "car_number": "283"},
            {"brand": "Lada Granta C+", "car_number": "664"},
            {"brand": "Lada Granta C+", "car_number": "354"},
            {"brand": "Lada Granta C+", "car_number": "011"},
            {"brand": "Lada Granta C+", "car_number": "656"},
            {"brand": "Lada Granta C+", "car_number": "887"},
            {"brand": "Lada Granta", "car_number": "105"},
            {"brand": "Lada Granta C+", "car_number": "277"},
            {"brand": "Lada Granta C+", "car_number": "014"},
        ]

        for car_info in cars_data:
            car = Car(**car_info)
            db.session.add(car)

        db.session.commit()
        print("Автомобили успешно добавлены.")

if __name__ == "__main__":
    add_cars()