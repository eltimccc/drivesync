import os
from datetime import timedelta
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "my")
    # SQLALCHEMY_DATABASE_URI = os.getenv(
    #     "DATABASE_URL",
    # )
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "instance/app.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = os.getenv("FLASK_ENV")
    TEMPLATES_AUTO_RELOAD = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=2)
    REMEMBER_COOKIE_DURATION = timedelta(days=2)
