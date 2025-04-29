import pytest
from flask import url_for


@pytest.mark.parametrize(
    "username, password, expected_redirect",
    [
        ("testuser", "wrongpassword", "auth.login"),
        ("wrongtestuser", "wrongpassword", "auth.login"),
        ("testuser", "password123", "main.get_bookings"),
    ],
)
def test_login(client, test_user, username, password, expected_redirect):
    """Параметризованный тест входа в систему."""

    client.get(url_for("auth.logout"))

    response = client.post(
        url_for("auth.login"),
        data={"username": username, "password": password},
        follow_redirects=True,
    )
    assert url_for(expected_redirect) in response.request.path
    assert response.status_code == 200


def test_authenticated_user_access(authenticated_user):
    """
    Проверка, что аутентифицированный пользователь может получить доступ к защищенной странице.
    """
    response = authenticated_user.get(url_for("main.get_bookings"))

    assert response.status_code == 200
    assert "Бронирования".encode("utf8") in response.data
    with authenticated_user.session_transaction() as session:
        assert "_user_id" in session


def test_authenticated_session(authenticated_user):
    """Проверка, что после успешного входа пользователь аутентифицирован."""
    client = authenticated_user

    response = client.get(url_for("main.get_bookings"))
    assert response.status_code == 200
    assert "Бронирования".encode("utf8") in response.data


def test_logout(authenticated_user):
    """Проверка выхода из системы и недоступности защищенных страниц."""
    client = authenticated_user

    response = client.get(url_for("main.get_bookings"))
    assert response.status_code == 200

    response = client.get(url_for("auth.logout"), follow_redirects=True)
    assert response.status_code == 200

    response = client.get(url_for("main.get_bookings"), follow_redirects=False)
    assert response.status_code in [302, 401]

    response = client.get(url_for("auth.register"), follow_redirects=False)
    assert response.status_code == 403
