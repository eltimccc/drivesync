import pytest
from flask import url_for
from app.models import Car
from app.forms.forms import CarForm


def test_add_car_unauthenticated(client):
    """
    Проверка, что неавторизованный пользователь не может получить доступ к странице добавления машины.
    """
    response = client.get(url_for("car.add_car"), follow_redirects=False)
    assert response.status_code == 302  # Ожидаем редирект на страницу входа
    assert url_for("auth.login") in response.headers["Location"]  # Проверка редиректа на страницу входа


def test_add_car_authenticated_get(authenticated_user):
    """
    Проверка, что авторизованный пользователь может получить доступ к странице добавления машины (GET-запрос).
    """
    client = authenticated_user
    response = client.get(url_for("car.add_car"))
    assert response.status_code == 200  # Проверка успешного доступа
    assert "Добавить".encode("utf8") in response.data  # Проверка, что отображается форма добавления машины
