"""
Конфигурация и инициализация лимитера запросов для Flask приложения.

Использует Flask-Limiter для ограничения числа запросов с одного IP-адреса
в минуту. Лимиты на запросы и хранилище настроены в соответствии с параметрами
из констант.
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.constants import LIMITS

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{LIMITS} per minute"],
    storage_uri="memory://",
)
