from flask import (
    Blueprint,
    abort,
    redirect,
    render_template,
    request,
    url_for,
    current_app,
)
from flask_login import login_required
from sqlalchemy import select

from app.constants import (
    CAR_ADD_BP_ROUTE,
    CAR_ADD_TEMPLATE,
    CAR_BP_NAME_ROUTE,
    CAR_DELETE_BP_ROUTE,
    CAR_DETAIL_BP_ROUTE,
    CAR_DETAIL_TEMPLATE,
    CAR_EDIT_BP_ROUTE,
    CAR_EDIT_TEMPLATE,
    CAR_URL_PREFIX,
    CARS_BP_ROUTE,
    CARS_GET,
    CARS_GET_ROUTE,
)
from app.forms.forms import CarForm, EditCarForm
from app.models import Booking
from app.models import Car
from app import db


car_blueprint = Blueprint(CAR_BP_NAME_ROUTE, __name__, url_prefix=CAR_URL_PREFIX)


@car_blueprint.route(CAR_ADD_BP_ROUTE, methods=["GET", "POST"])
@login_required
def add_car():
    form = CarForm()
    if form.validate_on_submit() and request.method == "POST":
        new_car = Car(
            brand=form.brand.data,
            car_number=form.car_number.data,
            transmission=form.transmission.data,
        )
        db.session.add(new_car)
        db.session.commit()
        current_app.logger.info(f"New car added: {new_car}")
        return redirect(url_for(CARS_GET_ROUTE))

    return render_template(CAR_ADD_TEMPLATE, form=form)


@car_blueprint.route(CARS_BP_ROUTE)
@login_required
def get_cars():
    current_app.logger.info("Accessed get cars page")
    is_deleted_param = request.args.get("is_deleted")

    cars = db.session.scalars(
        select(Car).where(Car.is_deleted == (is_deleted_param == "true"))
    ).all()

    return render_template(CARS_GET, cars=cars)


@car_blueprint.route(CAR_DETAIL_BP_ROUTE, methods=["GET"])
@login_required
def car_detail(car_id):
    current_app.logger.info(f"Accessed detail car page for car ID: {car_id}")
    sort_by = request.args.get("sort_by", "start_date")
    sort_order = request.args.get("sort_order", "desc")

    car = db.session.get(Car, car_id)
    if car is None:
        abort(404)

    stmt = select(Booking).where(Booking.car_id == car_id)

    order_column = getattr(Booking, sort_by)
    if sort_order == "desc":
        stmt = stmt.order_by(order_column.desc())
    else:
        stmt = stmt.order_by(order_column.asc())

    bookings = db.session.execute(stmt).scalars().all()

    return render_template(
        CAR_DETAIL_TEMPLATE,
        car=car,
        bookings=bookings,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@car_blueprint.route(CAR_EDIT_BP_ROUTE, methods=["GET", "POST"])
@login_required
def edit_car(car_id):
    current_app.logger.info(f"Accessed edit car page with car ID: {car_id}")

    car = db.session.get(Car, car_id)
    if not car:
        abort(404)

    form = EditCarForm(obj=car)

    if form.validate_on_submit():
        form.populate_obj(car)
        db.session.commit()
        current_app.logger.info(f"Edited car with ID: {car_id}")
        return redirect(url_for(CARS_GET_ROUTE))

    return render_template(CAR_EDIT_TEMPLATE, form=form, car=car)


@car_blueprint.route(CAR_DELETE_BP_ROUTE, methods=["POST"])
@login_required
def delete_car(car_id):
    car = db.session.get(Car, car_id)
    if not car:
        abort(404)

    car.is_deleted = True
    db.session.commit()

    current_app.logger.warning(f"DELETED car with ID: {car_id}")
    return redirect(url_for(CARS_GET_ROUTE))
