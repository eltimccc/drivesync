# update_status_back.py
from app import create_app, db
from app.models import Booking

app = create_app()

with app.app_context():
    db.session.query(Booking).filter_by(status="reserved").update({"status": "Бронь"})
    db.session.commit()
    print("Statuses updated successfully.")
