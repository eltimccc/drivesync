from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(60), nullable=False)
    telegram_id = db.Column(db.String(100), unique=True, nullable=True)
    is_superuser = db.Column(db.Boolean, default=False)

    def repr(self):
        return f"User('{self.username}', '{self.email}')"
