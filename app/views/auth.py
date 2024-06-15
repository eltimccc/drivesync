from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt, login_manager
from app.constants import AUTH_BP_NAME_ROUTE, AUTH_LOGIN_BP_ROUTE, AUTH_LOGIN_TEMPLATE, AUTH_LOGOUT_BP_ROUTE, AUTH_REGISTER_BP_ROUTE, AUTH_REGISTER_ROUTE, AUTH_REGISTER_TEMPLATE, AUTH_URL_PREFIX, BOOKING_MAIN_ROUTE
from app.utils.decorators import superuser_required
from app.models import User
from app.forms.forms import RegistrationForm, LoginForm

auth_blueprint = Blueprint(AUTH_BP_NAME_ROUTE, __name__, url_prefix=AUTH_URL_PREFIX)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_blueprint.route(AUTH_REGISTER_BP_ROUTE, methods=["GET", "POST"])
@superuser_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash("Новый пользователь был создан!", "success")
        return redirect(url_for(AUTH_REGISTER_ROUTE))
    return render_template(AUTH_REGISTER_TEMPLATE, title="Register", form=form)


@auth_blueprint.route(AUTH_LOGIN_BP_ROUTE, methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(BOOKING_MAIN_ROUTE))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for(BOOKING_MAIN_ROUTE))
        else:
            flash("Неполучилось, проверьте ввденные данные", "danger")
    return render_template(AUTH_LOGIN_TEMPLATE, title="Login", form=form)


@auth_blueprint.route(AUTH_LOGOUT_BP_ROUTE)
def logout():
    logout_user()
    return redirect(url_for(BOOKING_MAIN_ROUTE))
