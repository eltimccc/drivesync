# conftest.py
from flask_login import login_user
import pytest
from sqlalchemy import event
from app import create_app
from app import db as _db
from flask import Flask
from flask.testing import FlaskClient

from app.models.user import User

@pytest.fixture(scope='session')
def app():
    app = create_app(config_class="config.TestConfig")
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        yield app

@pytest.fixture
def authenticated_user(db):
    user = User(
        id=1,
        username="testuser",
        password="testpassword",  # Пароль должен быть хэширован
        email="test@example.com"
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def authenticated_client(client, authenticated_user):
    with client:
        login_user(authenticated_user)
        yield client

@pytest.fixture(scope='session')
def db(app):
    _db.create_all()
    yield _db
    _db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture(scope='function')
def session(db):
    connection = db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session_ = db.create_scoped_session(options=options)
    db.session = session_
    yield session_
    transaction.rollback()
    connection.close()