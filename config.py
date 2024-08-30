import os
from datetime import timedelta
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "secret_4_me")
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "instance/app.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = os.getenv("FLASK_ENV")
    TEMPLATES_AUTO_RELOAD = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=5)
    REMEMBER_COOKIE_DURATION = timedelta(days=5)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret_4_jwt")
