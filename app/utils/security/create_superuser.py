from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def create_superuser(db, bcrypt):
    from app.models import User

    if not User.query.filter_by(username="admin").first():
        hashed_password = bcrypt.generate_password_hash("11Superpassword11").decode(
            "utf-8"
        )
        superuser = User(
            username="admin",
            email="eltimccc@gmail.com",
            password=hashed_password,
            is_superuser=True,
        )
        
        db.session.add(superuser)
        db.session.commit()
        print("admin created.")

    else:
        print("admin already exists.")
