from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def create_superuser(db, bcrypt):
    from app.models import User

    if not User.query.filter_by(is_superuser=True).first():
        hashed_password = bcrypt.generate_password_hash("superpassword").decode("utf-8")
        superuser = User(
            username="admin",
            email="admin@example.com",
            password=hashed_password,
            is_superuser=True,
        )
        db.session.add(superuser)
        db.session.commit()
        print("Superuser created.")
