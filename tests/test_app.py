import pytest
from app import create_app, db, bcrypt
from app.models import User


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app()
    flask_app.config.from_object("tests.config_test.TestConfig")

    testing_client = flask_app.test_client()

    with flask_app.app_context():
        db.create_all()
        yield testing_client
        db.drop_all()


def test_home_page(test_client):
    response = test_client.get("/")
    assert response.status_code == 302


def test_superuser_creation(test_client):
    with test_client.application.app_context():
        superuser = User.query.filter_by(is_superuser=True).first()
        assert superuser is not None
        assert superuser.username == "admin"


def test_non_superuser_cannot_access_register_page(test_client):
    hashed_password = bcrypt.generate_password_hash("userpassword").decode("utf-8")
    user = User(
        username="regularuser",
        email="regularuser@example.com",
        password=hashed_password,
        is_superuser=False,
    )
    db.session.add(user)
    db.session.commit()

    login_response = test_client.post(
        "/auth/login",
        data=dict(email="regularuser@example.com", password="userpassword"),
        follow_redirects=True,
    )
    assert login_response.status_code == 200

    response = test_client.get("/auth/register", follow_redirects=True)

    assert response.status_code == 500


def test_superuser_can_login(test_client):
    login_response = test_client.post(
        "/auth/login",
        data=dict(email="admin@example.com", password="superpassword"),
        follow_redirects=True,
    )

    assert login_response.status_code == 200
