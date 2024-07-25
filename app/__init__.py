import os
import logging
import time

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_talisman import Talisman
from flask_limiter.util import get_remote_address
from logging.handlers import RotatingFileHandler

from app.utils.security import create_superuser
from app.utils.security.limiter_config import limiter
from app.utils.utils_db import register_event_listeners
from app.utils.security.csp_config import csp


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"

os.environ["TZ"] = "Europe/Moscow"
time.tzset()

csp_directives = {k: " ".join(v) for k, v in csp.items()}


def create_app(config_class="config.Config"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    app.secret_key = "supersecretkey"

    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.remember_cookie_duration = app.config["REMEMBER_COOKIE_DURATION"]

    @app.before_request
    def make_session_permanent():
        session.permanent = True
        app.permanent_session_lifetime = app.config["PERMANENT_SESSION_LIFETIME"]

    limiter.init_app(app)

    @app.after_request
    def log_limit_exceeded(response):
        if response.status_code == 429:
            ip_address = get_remote_address()
            app.logger.warning(f"Rate limit exceeded by IP: {ip_address}")
        return response

    Talisman(app, content_security_policy=csp_directives)

    from app.views.main import main_blueprint

    app.register_blueprint(main_blueprint)

    from app.views.booking import booking_blueprint

    app.register_blueprint(booking_blueprint)

    from app.views.car import car_blueprint

    app.register_blueprint(car_blueprint)

    from app.views.report import report_blueprint

    app.register_blueprint(report_blueprint)

    from app.views.auth import auth_blueprint

    app.register_blueprint(auth_blueprint)

    from app.views.errors import errors_blueprint

    app.register_blueprint(errors_blueprint)

    with app.app_context():
        db_path = os.path.join(
            app.instance_path,
            app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", ""),
        )
        if not os.path.exists(db_path):
            db.create_all()
            create_superuser(db, bcrypt)
        else:
            app.logger.info("Database already exists! Skipping creation.")
            print("Database already exists. Skipping creation.")

        register_event_listeners(app, db)

    if not app.debug:
        if not os.path.exists("logs"):
            os.makedirs("logs", exist_ok=True)
        file_handler = RotatingFileHandler(
            "logs/flask_app.log", maxBytes=102400, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("Flask App Started")

    return app
