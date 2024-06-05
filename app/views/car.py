from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import login_required

from app.constants import (
    CAR_ADD_BP_ROUTE,
    CAR_ADD_MODAL_TEMPLATE,
    CAR_ADD_TEMPLATE,
    CAR_DELETE_BP_ROUTE,
    CAR_DETAIL_BP_ROUTE,
    CAR_DETAIL_TEMPLATE,
    CAR_EDIT_BP_ROUTE,
    CAR_EDIT_TEMPLATE,
    CARS_BP_ROUTE,
    CARS_GET,
    CARS_GET_ROUTE,
)
from app.forms import CarForm, EditCarForm
from app.models import Booking, Car
from app import db


car_blueprint = Blueprint("car", __name__, url_prefix="/car")


@car_blueprint.route(CAR_ADD_BP_ROUTE, methods=["GET", "POST"])
@login_required
def add_car():
    form = CarForm()
    if form.validate_on_submit() and request.method == "POST":
        try:
            new_car = Car(
                brand=form.brand.data,
                car_number=form.car_number.data,
                transmission=form.transmission.data,
            )
            db.session.add(new_car)
            db.session.commit()
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"message": "Машина успешно добавлена!"})
            else:
                return redirect(url_for(CARS_GET_ROUTE))
        except Exception as e:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"error": str(e)}), 500
            else:
                return redirect(url_for(CARS_GET_ROUTE))
    else:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return render_template(CAR_ADD_MODAL_TEMPLATE, form=form)
        else:
            return render_template(CAR_ADD_TEMPLATE, form=form)


@car_blueprint.route(CARS_BP_ROUTE)
@login_required
def get_cars():
    is_deleted_param = request.args.get("is_deleted")

    if is_deleted_param == "true":
        cars = Car.query.filter_by(is_deleted=True).all()
    else:
        cars = Car.query.filter_by(is_deleted=False).all()

    return render_template(CARS_GET, cars=cars)


# @car_blueprint.route(CAR_DETAIL_BP_ROUTE)
# @login_required
# def car_detail(car_id):
#     car = Car.query.get(car_id)

#     bookings = Booking.query.filter_by(car_id=car_id).all()

#     return render_template(CAR_DETAIL_TEMPLATE, car=car, bookings=bookings)
@car_blueprint.route('/car/<int:car_id>', methods=["GET"])
@login_required
def car_detail(car_id):
    sort_by = request.args.get('sort_by', 'start_date')
    sort_order = request.args.get('sort_order', 'desc')

    if sort_order == 'desc':
        bookings = Booking.query.filter_by(car_id=car_id).order_by(getattr(Booking, sort_by).desc()).all()
    else:
        bookings = Booking.query.filter_by(car_id=car_id).order_by(getattr(Booking, sort_by).asc()).all()

    car = Car.query.get_or_404(car_id)

    return render_template('car_detail.html', car=car, bookings=bookings, sort_by=sort_by, sort_order=sort_order)

@car_blueprint.route(CAR_EDIT_BP_ROUTE, methods=["GET", "POST"])
@login_required
def edit_car(car_id):
    car = Car.query.get_or_404(car_id)
    form = EditCarForm(obj=car)
    if form.validate_on_submit():
        form.populate_obj(car)
        db.session.commit()
        return redirect(url_for(CARS_GET_ROUTE))
    return render_template(CAR_EDIT_TEMPLATE, form=form, car=car)


@car_blueprint.route(CAR_DELETE_BP_ROUTE, methods=["POST"])
@login_required
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    car.is_deleted = True
    db.session.commit()
    return redirect(url_for(CARS_GET_ROUTE))
