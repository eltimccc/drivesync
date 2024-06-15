# import os
# from dotenv import load_dotenv

# basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, ".env"))


# class Config:
#     SECRET_KEY = os.getenv("SECRET_KEY")
#     SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
#         basedir, "instance", "db.sqlite3"
#     )
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     TEMPLATES_AUTO_RELOAD = True

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/drivesync_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = os.getenv("FLASK_ENV")
    TEMPLATES_AUTO_RELOAD = True
