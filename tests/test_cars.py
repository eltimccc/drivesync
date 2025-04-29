import pytest
from flask import request, url_for
from app.models import Car
from app.forms.forms import CarForm


def test_get_cars_unauthenticated(client):
    """
    Проверка отображения страницы логина для неавторизованного пользователя
    """
    response = client.get(url_for("car.get_cars"))

    assert response.status_code == 200

    assert b"Login" in response.data
    assert b"username" in response.data
    assert b"password" in response.data


def test_get_cars_unauthenticated(client):
    """
    Проверка редиректа для неавторизованного пользователя
    """
    response = client.get(url_for("car.get_cars"), follow_redirects=False)

    assert response.status_code == 302
    assert url_for("auth.login", _external=False) in response.headers["Location"]


def test_add_car_unauthenticated(client):
    """
    Проверка, что неавторизованный пользователь не может получить доступ к странице добавления машины.
    """
    response = client.get(url_for("car.add_car"), follow_redirects=False)
    assert response.status_code == 302
    assert url_for("auth.login") in response.headers["Location"]


def test_add_car_authenticated_get(authenticated_user):
    """
    Проверка, что авторизованный пользователь может получить доступ к странице добавления машины (GET-запрос).
    """
    client = authenticated_user
    response = client.get(url_for("car.add_car"))
    assert response.status_code == 200
    assert "Добавить".encode("utf8") in response.data


def test_add_car_success(authenticated_user, app):
    """
    Проверка успешного добавления машины с валидными данными.
    """
    client = authenticated_user

    test_data = {
        "brand": "Hyundai Solaris",
        "car_number": "А123МР",
        "transmission": "АКПП",
    }

    response = client.post(
        url_for("car.add_car"), data=test_data, follow_redirects=True
    )

    assert response.status_code == 200
    assert url_for("car.get_cars") in response.request.path

    with app.app_context():
        car = Car.query.filter_by(car_number=test_data["car_number"]).first()
        assert car is not None
        assert car.brand == test_data["brand"]
        assert car.transmission == test_data["transmission"]


def test_car_detail_not_found(authenticated_user):
    """
    Проверка обработки случая, когда машина не найдена.
    """
    client = authenticated_user

    response = client.get(url_for("car.car_detail", car_id=999999))

    assert response.status_code == 404
