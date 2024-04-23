import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.static_folder = "static"
app.config["TEMPLATES_AUTO_RELOAD"] = True
load_dotenv()

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
db = SQLAlchemy(app)


from routes import *

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    extra_files = ["./templates/"]
    app.run(debug=True, extra_files=extra_files)
