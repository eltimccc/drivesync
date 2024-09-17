from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .car import Car
from .booking import Booking
from .user import User