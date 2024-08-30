from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import create_access_token
from flask_login import login_user, current_user
from app.models import User
from app import bcrypt, db

login_api = Blueprint('login_api', __name__)


@login_api.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    telegram_id = data.get('telegram_id')
    username = data.get('username')
    password = data.get('password')

    if telegram_id:
        user = User.query.filter_by(telegram_id=telegram_id).first()
        if user:
            access_token = create_access_token(identity={'username': user.username})
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"msg": "Telegram ID не найден"}), 401

    elif username and password:
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity={'username': user.username})
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"msg": "Неверный логин или пароль"}), 401

    return jsonify({"msg": "Пожалуйста, предоставьте необходимые данные для входа"}), 400

