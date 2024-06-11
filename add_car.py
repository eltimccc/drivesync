from app import create_app, db
from app.models import Car

def create_test_cars(num_cars=30):
    for i in range(num_cars):
        car = Car(
            brand=f'TestBrand{i+1}',
            car_number=f'TESTCAR{i+1}',
            transmission='Automatic',  # Предположим, что все тестовые автомобили с автоматической коробкой передач
            is_deleted=False
        )
        
        db.session.add(car)
    
    db.session.commit()
    print(f'{num_cars} test cars added.')

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        create_test_cars()
