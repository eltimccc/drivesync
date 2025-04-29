# test_config.py
import os
from datetime import timedelta


class TestConfig:
    TESTING = True
    SECRET_KEY = "test_secret_key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=5)
    REMEMBER_COOKIE_DURATION = timedelta(days=5)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    JWT_SECRET_KEY = "test_jwt_secret_key"
