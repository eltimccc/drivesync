from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_required, login_user, current_user, logout_user
from app import db, bcrypt, login_manager
from app.constants import (
    AUTH_BP_NAME_ROUTE,
    AUTH_LIST_BP_ROUTE,
    AUTH_LIST_TEMPLATE,
    AUTH_LOGIN_BP_ROUTE,
    AUTH_LOGIN_TEMPLATE,
    AUTH_LOGOUT_BP_ROUTE,
    AUTH_REGISTER_BP_ROUTE,
    AUTH_REGISTER_ROUTE,
    AUTH_REGISTER_TEMPLATE,
    AUTH_URL_PREFIX,
    BOOKING_MAIN_ROUTE,
)
from app.utils.decorators import superuser_required
from app.models import User
from app.forms.forms import EditUserForm, HiddenForm, RegistrationForm, LoginForm

auth_blueprint = Blueprint(AUTH_BP_NAME_ROUTE, __name__, url_prefix=AUTH_URL_PREFIX)


@login_manager.user_loader
def load_user(user_id):
    return User.query.session.get(User, int(user_id))


@auth_blueprint.route(AUTH_REGISTER_BP_ROUTE, methods=["GET", "POST"])
@superuser_required
def register():
    current_app.logger.info("Accessed registration page.")
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data,
            email=form.email.data,
            telegram_id=form.telegram_id.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash("Новый пользователь был создан!", "success")
        current_app.logger.info(f"New user registered with username: {user.username}")
        return redirect(url_for(AUTH_REGISTER_ROUTE))
    else:
        current_app.logger.warning("Registration form validation failed.")
    return render_template(AUTH_REGISTER_TEMPLATE, title="Register", form=form)


@auth_blueprint.route(AUTH_LOGIN_BP_ROUTE, methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        current_app.logger.info(
            f"User {current_user.username} is already authenticated."
        )
        return redirect(url_for(BOOKING_MAIN_ROUTE))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            current_app.logger.info(f"User {user.username} logged in successfully.")
            return redirect(url_for(BOOKING_MAIN_ROUTE))
        else:
            flash("Неполучилось, проверьте введенные данные", "danger")
            current_app.logger.warning("Failed login attempt.")
    return render_template(AUTH_LOGIN_TEMPLATE, title="Login", form=form)


@auth_blueprint.route(AUTH_LOGOUT_BP_ROUTE)
@login_required
def logout():
    current_app.logger.info(f"User {current_user.username} logged out.")
    logout_user()
    return redirect(url_for(BOOKING_MAIN_ROUTE))


@auth_blueprint.route(AUTH_LIST_BP_ROUTE, methods=["GET"])
@login_required
@superuser_required
def list_users():
    form = HiddenForm()
    users = User.query.all()
    return render_template(AUTH_LIST_TEMPLATE, users=users, form=form)


@auth_blueprint.route("/delete_user/<int:user_id>", methods=["POST"])
@login_required
@superuser_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("Пользователь был удален!", "success")
    return redirect(url_for("auth.list_users"))


@auth_blueprint.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
@login_required
@superuser_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.telegram_id = form.telegram_id.data
        if form.password.data:
            user.password = bcrypt.generate_password_hash(form.password.data).decode(
                "utf-8"
            )
        user.is_superuser = form.is_superuser.data
        db.session.commit()
        flash("Информация пользователя была обновлена!", "success")
        return redirect(url_for("auth.list_users"))
    return render_template("edit_user.html", form=form, user=user)
