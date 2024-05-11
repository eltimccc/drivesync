from drivesync.app import app, db  # Импортируем объект app из вашего модуля app.py
from drivesync.models import Car


def add_cars():
    with app.app_context():
        cars_data = [
            {"brand": "Hyundai Creta", "car_number": "467", "transmission": "АКПП"},
            {"brand": "Kia Rio", "car_number": "116", "transmission": "АКПП"},
            {"brand": "Kia Rio", "car_number": "157", "transmission": "АКПП"},
            {"brand": "Kia Rio", "car_number": "088", "transmission": "АКПП"},
            {"brand": "Kia Rio", "car_number": "355", "transmission": "АКПП"},
            {"brand": "Hyundai Solaris АКПП", "car_number": "181", "transmission": "АКПП"},
            {"brand": "Hyundai Solaris МКПП", "car_number": "325", "transmission": "МКПП"},
            {"brand": "Hyundai Solaris МКПП", "car_number": "645", "transmission": "МКПП"},
            {"brand": "Hyundai Solaris 1.4", "car_number": "627", "transmission": "МКПП"},
            {"brand": "Renault Logan", "car_number": "777", "transmission": "МКПП"},
            {"brand": "Renault Logan", "car_number": "017", "transmission": "МКПП"},
            {"brand": "Renault Logan", "car_number": "371", "transmission": "МКПП"},
            {"brand": "Renault Logan", "car_number": "393", "transmission": "МКПП"},
            {"brand": "Renault Logan", "car_number": "455", "transmission": "МКПП"},
            {"brand": "Renault Logan", "car_number": "473", "transmission": "МКПП"},
            {"brand": "Renault Logan", "car_number": "712", "transmission": "МКПП"},
            {"brand": "Renault Logan", "car_number": "750", "transmission": "МКПП"},
            {"brand": "Lada Largus", "car_number": "440", "transmission": "МКПП"},
            {"brand": "Lada Granta АКПП", "car_number": "235", "transmission": "АКПП"},
            {"brand": "Lada Granta АКПП", "car_number": "283", "transmission": "АКПП"},
            {"brand": "Lada Granta C+", "car_number": "664", "transmission": "МКПП"},
            {"brand": "Lada Granta C+", "car_number": "354", "transmission": "МКПП"},
            {"brand": "Lada Granta C+", "car_number": "011", "transmission": "МКПП"},
            {"brand": "Lada Granta C+", "car_number": "656", "transmission": "МКПП"},
            {"brand": "Lada Granta C+", "car_number": "887", "transmission": "МКПП"},
            {"brand": "Lada Granta", "car_number": "105", "transmission": "МКПП"},
            {"brand": "Lada Granta C+", "car_number": "277", "transmission": "МКПП"},
            {"brand": "Lada Granta C+", "car_number": "014", "transmission": "МКПП"},
        ]

        for car_info in cars_data:
            car = Car(**car_info)
            db.session.add(car)

        db.session.commit()
        print("Автомобили успешно добавлены.")


if __name__ == "__main__":
    add_cars()
