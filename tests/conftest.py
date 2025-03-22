import random
from flask import url_for
import pytest
from flask_bcrypt import Bcrypt
from app import create_app, db
from app.models.user import User
from tests.test_config import TestConfig


@pytest.fixture(scope="session")
def app():
    """Создает тестовый экземпляр Flask-приложения с тестовой БД."""
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="session")
def client(app):
    """Тестовый клиент Flask."""
    return app.test_client()


@pytest.fixture(scope="function")
def db_session(app):
    """Создает чистую БД перед каждым тестом."""
    with app.app_context():
        db.session.begin_nested()
        yield db.session
        db.session.rollback()


@pytest.fixture
def test_user(db_session, app):
    """Очищает таблицу пользователей и создает нового тестового пользователя."""
    db_session.query(User).delete()
    db_session.commit()

    bcrypt = Bcrypt(app)
    password = "password123"
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(
        username="testuser",
        email="testuser@example.com",
        telegram_id=str(random.randint(10000, 99999)),
        password=hashed_password,
    )
    db_session.add(user)
    db_session.commit()

    return user

@pytest.fixture
def authenticated_user(client, test_user):
    """
    Фикстура для авторизации тестового пользователя.
    Возвращает клиент с активной сессией авторизованного пользователя.
    """
    # Авторизуем пользователя
    client.post(
        url_for("auth.login"),
        data={"username": test_user.username, "password": "password123"},
        follow_redirects=True,
    )
    return client
