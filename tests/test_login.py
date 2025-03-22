import pytest
import random
from flask_bcrypt import Bcrypt
from flask import url_for
from app.models import User


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


@pytest.mark.parametrize(
    "username, password, expected_status, expected_message",
    [
        ("testuser", "wrongpassword", 200, "Неполучилось"),
        ("testuser", "password123", 200, "Бронирования"),
    ],
)
def test_login(
    client, db_session, test_user, username, password, expected_status, expected_message
):
    """Параметризованный тест входа в систему."""
    response = client.post(
        url_for("auth.login"),
        data={"username": username, "password": password},
        follow_redirects=True,
    )

    assert response.status_code == expected_status
    assert (
        expected_message.encode("utf-8") in response.data
    )

    if password == "password123":
        response = client.get(url_for("main.get_bookings"))
        assert response.status_code == 200


def test_authenticated_session(client, db_session, test_user):
    """Проверка, что после успешного входа пользователь аутентифицирован."""
    response = client.post(
        url_for("auth.login"),
        data={"username": "testuser", "password": "password123"},
        follow_redirects=True,
    )
    assert response.status_code == 200

    response = client.get(url_for("main.get_bookings"))
    assert response.status_code == 200


def test_logout(client, db_session, test_user):
    """Проверка выхода из системы и недоступности защищенных страниц."""

    response = client.post(
        url_for("auth.login"),
        data={"username": "testuser", "password": "password123"},
        follow_redirects=True,
    )
    assert response.status_code == 200

    response = client.get(url_for("main.get_bookings"))
    assert response.status_code == 200  # Доступно

    response = client.get(url_for("auth.logout"), follow_redirects=True)
    assert response.status_code == 200

    # После выхода защищенная страница недоступна (должен быть редирект на логин)
    response = client.get(url_for("main.get_bookings"), follow_redirects=False)
    assert response.status_code in [
        302,
        401,
    ]
