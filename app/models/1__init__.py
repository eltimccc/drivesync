from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .booking import Booking, DeletedBooking
from .car import Car