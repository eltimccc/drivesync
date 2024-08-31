import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt


env_dir = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.abspath(os.path.join(env_dir, '..', '..', '..', '..'))

load_dotenv(os.path.join(basedir, ".env"))

bcrypt = Bcrypt()

def create_superuser(db, bcrypt):
    """
    Создает суперпользователя в базе данных, если он еще не существует.

    Args:
        db: Объект базы данных для взаимодействия с хранилищем данных.
        bcrypt: Объект для хеширования паролей.

    Примечание:
        Адрес электронной почты и пароль суперпользователя берутся из
        жестко заданного значения и переменной окружения соответственно.
    """
    from app.models import User

    if not User.query.filter_by(email="eltimccc@gmail.com", is_superuser=True).first():
        hashed_password = bcrypt.generate_password_hash(os.getenv("PASSWORD")).decode("utf-8")
        superuser = User(
            username="admin",
            email="eltimccc@gmail.com",
            password=hashed_password,
            is_superuser=True,
        )
        db.session.add(superuser)
        db.session.commit()
        print("Superuser created.")
