def serialize_bookings(bookings):

    return [
        {
            "car_id": booking.car.id,
            "car_brand": booking.car.brand,
            "car_number": booking.car.car_number,
            "booking_id": booking.id,
            "start_date": booking.start_date.strftime("%d.%m.%Y %H:%M"),
            "end_date": booking.end_date.strftime("%d.%m.%Y %H:%M"),
            "status": booking.status,
        }
        for booking in bookings
    ]
