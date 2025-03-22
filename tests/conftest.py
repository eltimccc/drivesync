import pytest
from app import create_app, db
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
