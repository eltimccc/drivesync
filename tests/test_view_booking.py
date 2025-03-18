# tests/test_view_booking.py
import pytest
from datetime import datetime
from unittest.mock import patch
from flask import url_for
from app.models import Booking

@pytest.fixture
def booking(db):
    with patch('app.utils.utils_db.create_backup'):  # Мокируем create_backup
        booking = Booking(
            id=1000,
            status="confirmed",
            created_at=datetime(2023, 1, 1, 12, 0, 0),  # Используем datetime
            start_date=datetime(2023, 1, 1, 10, 0, 0),   # Пример start_date
            end_date=datetime(2023, 1, 1, 14, 0, 0),     # Пример end_date
            car_id=1,                                    # Пример car_id
            user_id=1,                                   # Пример user_id
            phone="+1234567890",                         # Пример phone
            description="Test booking"                   # Пример description
        )
        db.session.add(booking)
        db.session.commit()
        return booking

def test_view_booking(authenticated_client, booking):
    response = authenticated_client.get(url_for('booking.view_booking', booking_id=booking.id))
    assert response.status_code == 200
    assert b"Booking Details" in response.data

def test_view_booking_ajax(authenticated_client, booking):
    headers = {'X-Requested-With': 'XMLHttpRequest'}
    response = authenticated_client.get(url_for('booking.view_booking', booking_id=booking.id), headers=headers)
    assert response.status_code == 200
    assert b"Booking Details" in response.data