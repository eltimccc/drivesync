from app import create_app, db
from app.models import Car

def add_cars():
    app = create_app()
    with app.app_context():
        cars_data = [
            {"brand": "Hyundai Solaris", "car_number": "С515ТА", "transmission": "АКПП"},
            {"brand": "Baic U5", "car_number": "Т748СМ", "transmission": "АКПП"},
            {"brand": "Hyundai Creta", "car_number": "Х467НУ", "transmission": "АКПП"},
            {"brand": "Kia Rio", "car_number": "В116ОУ", "transmission": "АКПП"},
            {"brand": "Kia Rio", "car_number": "У157РУ", "transmission": "АКПП"},
            {"brand": "Kia Rio", "car_number": "Т088МУ", "transmission": "АКПП"},
            {"brand": "Kia Rio", "car_number": "О355МУ", "transmission": "АКПП"},
            {"brand": "Hyundai Solaris", "car_number": "Р181НУ", "transmission": "АКПП"},
            {"brand": "Hyundai Solaris", "car_number": "К325НУ", "transmission": "МКПП"},
            {"brand": "Hyundai Solaris", "car_number": "К645НУ", "transmission": "МКПП"},
            {"brand": "Hyundai Solaris 1.4", "car_number": "Е627КУ", "transmission": "МКПП"},
            {"brand": "Renault Logan", "car_number": "С777ВС", "transmission": "МКПП"},
            {"brand": "Renault Logan", "car_number": "А017УУ", "transmission": "МКПП"},
            {"brand": "Renault Logan", "car_number": "Х371ОУ", "transmission": "МКПП"},
            {"brand": "Renault Logan", "car_number": "Х393ОУ", "transmission": "МКПП"},
            {"brand": "Renault Logan", "car_number": "В455РУ", "transmission": "МКПП"},
            {"brand": "Renault Logan", "car_number": "Т024МУ", "transmission": "МКПП"},
            {"brand": "Renault Logan", "car_number": "Х712ОУ", "transmission": "МКПП"},
            {"brand": "Renault Logan", "car_number": "Т750МУ", "transmission": "МКПП"},
            {"brand": "Lada Vesta", "car_number": "В850ТА", "transmission": "АКПП"},
            {"brand": "Lada Vesta", "car_number": "Е421ТА", "transmission": "АКПП"},
            {"brand": "Lada Largus", "car_number": "Т440НУ", "transmission": "МКПП"},
            {"brand": "Lada Granta", "car_number": "Е235МУ", "transmission": "АКПП"},
            {"brand": "Lada Granta C+", "car_number": "О664УК", "transmission": "МКПП"},
            {"brand": "Lada Granta C+", "car_number": "Х354СМ", "transmission": "МКПП"},
            {"brand": "Lada Granta C+", "car_number": "Х011СМ", "transmission": "МКПП"},
            {"brand": "Lada Granta C+", "car_number": "О656УК", "transmission": "МКПП"},
            {"brand": "Lada Granta C+", "car_number": "К877СМ", "transmission": "МКПП"},
            {"brand": "Lada Granta C+", "car_number": "К277ТА", "transmission": "МКПП"},
            {"brand": "Lada Granta C+", "car_number": "В105УУ", "transmission": "МКПП"},
            {"brand": "Lada Granta C+", "car_number": "М084ТА", "transmission": "МКПП"},
            {"brand": "Lada Granta C+", "car_number": "А793ТА", "transmission": "МКПП"},
            {"brand": "Lada Granta C+", "car_number": "С651ТА", "transmission": "МКПП"},
            {"brand": "Lada Granta C+", "car_number": "О175УУ", "transmission": "МКПП"},
            {"brand": "Lada Granta C+", "car_number": "М509ТА", "transmission": "МКПП"},
            {"brand": "Lada Granta C+", "car_number": "К036ТА", "transmission": "МКПП"},
            {"brand": "Lada Granta C+", "car_number": "Т257ТА", "transmission": "МКПП"},
        ]

        for car_info in cars_data:
            car = Car(**car_info)
            db.session.add(car)

        db.session.commit()
        print("Автомобили успешно добавлены.")

if __name__ == "__main__":
    add_cars()
