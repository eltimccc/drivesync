from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


def create_superuser():
    from .models import User
    if not User.query.filter_by(is_superuser=True).first():
        hashed_password = bcrypt.generate_password_hash('superpassword').decode('utf-8')
        superuser = User(username='admin', email='admin@example.com', password=hashed_password, is_superuser=True)
        db.session.add(superuser)
        db.session.commit()
        print('Superuser created.')

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from .views.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.views.booking import booking_blueprint
    app.register_blueprint(booking_blueprint)

    from app.views.car import car_blueprint
    app.register_blueprint(car_blueprint)

    from app.views.report import report_blueprint
    app.register_blueprint(report_blueprint)

    from app.views.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    with app.app_context():
        db.create_all()
        create_superuser()

    return app
