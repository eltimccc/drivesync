import os
import logging
from logging.handlers import RotatingFileHandler

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

    from app.views.errors import errors
    app.register_blueprint(errors)

    with app.app_context():
        db.create_all()
        create_superuser()

    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/flask_app.log', maxBytes=102400, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Flask App Started')

    return app
