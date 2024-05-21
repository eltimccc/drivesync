from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    from .views.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.views.booking import booking_blueprint
    app.register_blueprint(booking_blueprint)

    from app.views.car import car_blueprint
    app.register_blueprint(car_blueprint)

    from app.views.report import report_blueprint
    app.register_blueprint(report_blueprint)

    with app.app_context():
        db.create_all()

    return app
