from datetime import datetime
from typing import Dict, Optional, Tuple
from app.models import Booking, Car
from app import db


class BookingService:
    """Сервис для работы с бронированиями, включая пересадки между машинами"""
    
    @staticmethod
    def update_booking(booking: Booking, form_data: Dict, move_data: Dict) -> Dict:
        """
        Обновляет бронирование:
        - Для статуса "Аренда": позволяет пересадку с разделением брони
        - Для других статусов: простая смена машины
        
        Args:
            booking: Объект бронирования для обновления
            form_data: Основные данные формы (даты, статус и т.д.)
            move_data: Данные для смены машины (и пересадки если статус "Аренда")
            
        Returns:
            Словарь с результатом операции и новым бронированием (если была пересадка)
            
        Raises:
            ValueError: При ошибках валидации
        """
        new_car_id = BookingService._parse_car_id(move_data)
        
        BookingService._validate_dates(form_data['start_date'], form_data['end_date'])
        
        if not new_car_id or new_car_id == booking.car_id:
            BookingService._update_booking_data(booking, form_data)
            return {'message': f"Бронирование ID {booking.id} обновлено", 'new_booking': None}
        
        if 'description' in form_data:
            booking.description = form_data['description']
            
        # Для статуса "Аренда" - проверяем пересадку
        if booking.status == "Аренда":
            move_start, move_end = BookingService._parse_transfer_dates(move_data)
            
            if move_start and move_start != booking.start_date:  # Нужна пересадка
                BookingService._validate_transfer(booking, move_start, move_end, new_car_id)
                new_booking = BookingService._create_transfer_booking(
                    booking, new_car_id, move_start, move_end, form_data
                )
                return {
                    'message': f'Пересадка в бронировании ID {booking.id} оформлена!',
                    'new_booking': new_booking
                }
        
        # Для всех статусов - простая смена машины
        BookingService._change_car(booking, new_car_id)
        return {'message': 'Машина успешно изменена', 'new_booking': None}

    @staticmethod
    def _should_create_transfer(booking: Booking, new_start: Optional[datetime]) -> bool:
        """Определяет, нужно ли создавать новое бронирование для пересадки"""
        # Упрощенная версия, так как проверка статуса теперь в основном методе
        return new_start is not None and new_start != booking.start_date

    @staticmethod
    def _parse_car_id(move_data: Dict) -> Optional[int]:
        """Парсит ID машины из данных пересадки"""
        try:
            return int(move_data['car_id']) if move_data.get('car_id') else None
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _parse_transfer_dates(move_data: Dict) -> Tuple[datetime, datetime]:
        """Парсит даты пересадки из данных формы"""
        try:
            move_start = datetime.strptime(move_data['move_start'], '%d.%m.%Y %H:%M') if move_data.get('move_start') else None
            move_end = datetime.strptime(move_data['move_end'], '%d.%m.%Y %H:%M') if move_data.get('move_end') else None
            return move_start, move_end
        except (ValueError, TypeError) as e:
            raise ValueError('Неверный формат даты пересадки') from e

    @staticmethod
    def _validate_dates(start_date: datetime, end_date: datetime) -> None:
        """Проверяет корректность дат бронирования"""
        if not start_date or not end_date:
            raise ValueError('Укажите обе даты')
        if end_date < start_date:
            raise ValueError('Дата окончания не может быть раньше даты начала')

    @staticmethod
    def _should_create_transfer(booking: Booking, new_start: Optional[datetime]) -> bool:
        """Определяет, нужно ли создавать новое бронирование для пересадки"""
        if booking.status != "Аренда":
            raise ValueError('Пересадка возможна только для броней со статусом "Аренда"')
        return new_start is not None and new_start != booking.start_date

    @staticmethod
    def _validate_transfer(booking: Booking, move_start: datetime, move_end: datetime, new_car_id: int) -> None:
        """Проверяет валидность данных для пересадки"""
        if not move_start or not move_end:
            raise ValueError('Для пересадки укажите даты начала и окончания')
        
        if move_end < move_start:
            raise ValueError('Дата окончания пересадки не может быть раньше даты начала')
        
        if move_start < booking.start_date:
            raise ValueError('Дата начала пересадки не может быть раньше даты начала бронирования')
        
        if not BookingService.is_car_available(new_car_id, move_start, move_end, booking.id):
            raise ValueError('Новая машина занята в указанный период')

    @staticmethod
    def _change_car(booking: Booking, new_car_id: int) -> None:
        """Изменяет машину в бронировании с проверкой доступности"""
        if not BookingService.is_car_available(new_car_id, booking.start_date, booking.end_date, booking.id):
            raise ValueError('Новая машина занята на указанные даты бронирования')
        
        new_car = Car.query.get_or_404(new_car_id)
        booking.car_id = new_car_id
        booking.description = f"{booking.description or ''}\nИзменение на {new_car.brand} {new_car.car_number} |"

    @staticmethod
    def _create_transfer_booking(
        booking: Booking,
        new_car_id: int,
        move_start: datetime,
        move_end: datetime,
        form_data: Dict
    ) -> Booking:
        """Создает новое бронирование для пересадки и обновляет исходное"""
        new_car = Car.query.get_or_404(new_car_id)
        new_booking = Booking(
            car_id=new_car_id,
            user_id=booking.user_id,
            start_date=move_start,
            end_date=move_end,
            status=form_data.get('status', booking.status),
            description=f"{booking.description or ''}\nПересадка с ID {booking.id}, {booking.car.brand} {booking.car.car_number} |",
            phone=form_data.get('phone', booking.phone),
            created_at=datetime.now()
        )
        
        db.session.add(new_booking)
        booking.end_date = move_start
        
        return new_booking

    @staticmethod
    def _update_booking_data(booking: Booking, form_data: Dict) -> None:
        """Обновляет основные данные бронирования"""
        for key, value in form_data.items():
            if hasattr(booking, key):
                setattr(booking, key, value)
        
        if booking.status == "Отказ":
            booking.end_date = booking.start_date

    @staticmethod
    def is_car_available(
        car_id: int,
        start_date: datetime,
        end_date: datetime,
        exclude_booking_id: Optional[int] = None
    ) -> bool:
        """
        Проверяет доступность машины в указанный период
        
        Args:
            car_id: ID машины для проверки
            start_date: Начало периода
            end_date: Окончание периода
            exclude_booking_id: ID бронирования, которое нужно исключить из проверки
            
        Returns:
            True если машина доступна, False если занята
        """
        BookingService._validate_dates(start_date, end_date)
        
        query = Booking.query.filter(
            Booking.car_id == car_id,
            Booking.start_date <= end_date,
            Booking.end_date >= start_date
        )
        
        if exclude_booking_id:
            query = query.filter(Booking.id != exclude_booking_id)
            
        return not query.first()