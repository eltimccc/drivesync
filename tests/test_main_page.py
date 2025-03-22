from flask import url_for


def test_main_page(client):
    """Тест главной страницы."""
    client.get(url_for("auth.logout"))

    response = client.get(url_for("main.get_bookings"))
    assert response.status_code == 302
    assert response.location.startswith(url_for("auth.login", _external=False))


def test_login_page_get(client):
    """Тест доступности страницы логина."""
    response = client.get(url_for("auth.login"))
    assert response.status_code == 200
    assert b"Login" in response.data
