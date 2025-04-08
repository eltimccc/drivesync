from datetime import datetime, timedelta
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    current_app,
)
from flask_login import current_user, login_required

from app import db
from app.constants import (
    BOOKING_ADD_BP_ROUTE,
    BOOKING_ADD_TEMPLATE,
    BOOKING_BP_NAME_ROUTE,
    BOOKING_CALENDAR_TEMPLATE,
    BOOKING_DELETE_BP_ROUTE,
    BOOKING_DETAIL_MODAL_ROUTE,
    BOOKING_DETAIL_MODAL_TEMPLATE,
    BOOKING_DETAIL_TEMPLATE,
    BOOKING_EDIT_BOOKING_ROUTE,
    BOOKING_EDIT_BP_ROUTE,
    BOOKING_EDIT_TEMPLATE,
    BOOKING_MAIN_ROUTE,
    BOOKING_MODAL_TEMPLATE,
    BOOKING_URL_PREFIX,
    BOOKING_VIEW_BOOKING_ROUTE,
    BOOKING_VIEW_BP_ROUTE,
    BOOKINGS_TODAY,
    BOOKINGS_TODAY_TEMPLATE,
)
from app.services.booking_service import BookingService
from app.utils.booking_helpers import handle_successful_booking, log_form_errors, prepopulate_form_from_request
from app.forms.forms import BookingForm, BookingUpdateForm
from app.models import Booking
from app.models import Car
from app.utils.calendar_utils import get_available_cars, get_bookings_in_range, get_start_date_from_request, get_week_dates, get_week_title, map_bookings_to_dates
from app.utils.utils import BOOKING_STATUSES


booking_blueprint = Blueprint(
    BOOKING_BP_NAME_ROUTE, __name__, url_prefix=BOOKING_URL_PREFIX
)


@booking_blueprint.route(BOOKING_VIEW_BP_ROUTE, methods=["GET"])
@login_required
def view_booking(booking_id):
    current_app.logger.info(f"Accessed view booking with ID: {booking_id}")
    booking = Booking.query.get_or_404(booking_id)
    status_color = BOOKING_STATUSES.get(booking.status, "#ffffff")

    formatted_created_at = booking.created_at.strftime("%d.%m.%Y %H:%M")

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        current_app.logger.debug(
            f"Rendering booking detail modal for booking ID: {booking_id}"
        )
        return render_template(
            BOOKING_DETAIL_MODAL_TEMPLATE,
            booking=booking,
            status_color=status_color,
            formatted_created_at=formatted_created_at,
        )
    else:
        current_app.logger.debug(
            f"Rendering booking detail page for booking ID: {booking_id}"
        )
        return render_template(
            BOOKING_DETAIL_TEMPLATE,
            booking=booking,
            status_color=status_color,
            formatted_created_at=formatted_created_at,
        )


@booking_blueprint.route(BOOKING_DETAIL_MODAL_ROUTE, methods=["GET"])
@login_required
def view_booking_modal(booking_id):
    current_app.logger.info(
        f"Accessed view booking modal with ID: {booking_id}")
    booking = Booking.query.get_or_404(booking_id)
    status_color = BOOKING_STATUSES.get(booking.status, "#ffffff")

    formatted_created_at = booking.created_at.strftime("%d.%m.%Y %H:%M")

    current_app.logger.debug(
        f"Rendering booking detail modal for booking ID: {booking_id}"
    )
    return render_template(
        BOOKING_DETAIL_MODAL_TEMPLATE,
        booking=booking,
        status_color=status_color,
        formatted_created_at=formatted_created_at,
    )


@booking_blueprint.route(BOOKINGS_TODAY, methods=["GET"])
@login_required
def bookings_today():
    date_str = request.args.get("date")
    if date_str:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        selected_date = datetime.today().date()

    pick_ups = (
        db.session.query(Booking)
        .join(Car)
        .filter(
            db.func.date(
                Booking.start_date) == selected_date, Booking.status != "Отказ"
        )
        .all()
    )
    drop_offs = (
        db.session.query(Booking)
        .join(Car)
        .filter(
            db.func.date(
                Booking.end_date) == selected_date, Booking.status != "Отказ"
        )
        .all()
    )

    return render_template(
        BOOKINGS_TODAY_TEMPLATE,
        pick_ups=pick_ups,
        drop_offs=drop_offs,
        today=selected_date,
    )


@booking_blueprint.route(BOOKING_ADD_BP_ROUTE, methods=["POST", "GET"])
@login_required
def add_booking():
    current_app.logger.info(
        f"User {current_user.username} accessed add booking endpoint."
    )
    form = BookingForm()
    cars = Car.query.filter_by(is_deleted=False).all()

    if request.method == "GET":
        prepopulate_form_from_request(form)

    if form.validate_on_submit():
        return handle_successful_booking(form, current_user)
    else:
        log_form_errors(form, current_user)

    return render_template(BOOKING_ADD_TEMPLATE, form=form, cars=cars)


@booking_blueprint.route(BOOKING_EDIT_BP_ROUTE, methods=["GET", "POST"])
@login_required
def edit_booking(booking_id):
    current_app.logger.info(f"User {current_user.username} editing booking ID: {booking_id}")
    booking = Booking.query.get_or_404(booking_id)
    form = BookingUpdateForm(obj=booking)
    form.status.choices = [(key, key) for key in BOOKING_STATUSES.keys()]
    cars = Car.query.filter_by(is_deleted=False).all()

    if request.method == 'POST':
        try:
            form_data = {
                'description': form.description.data,
                'phone': form.phone.data,
                'status': form.status.data,
                'start_date': form.start_date.data,
                'end_date': form.end_date.data
            }
            
            move_data = {
                'car_id': request.form.get('car'),
                'move_start': request.form.get('move_start'),
                'move_end': request.form.get('move_end_date')
            }

            result = BookingService.update_booking(booking, form_data, move_data)
            flash(result['message'], 'success')
            
            db.session.commit()
            
            # Перенаправляем обратно на редактирование (нового бронирования, если была пересадка)
            booking_id_to_edit = result['new_booking'].id if result['new_booking'] else booking.id
            return redirect(url_for(BOOKING_EDIT_BOOKING_ROUTE, booking_id=booking_id_to_edit))

        except ValueError as e:
            db.session.rollback()
            flash(str(e), 'danger')
            return render_template(BOOKING_EDIT_TEMPLATE, 
                               booking=booking, 
                               form=form,
                               cars=cars)
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating booking {booking_id}: {str(e)}", exc_info=True)
            flash(f'Произошла ошибка: {str(e)}', 'danger')

    return render_template(BOOKING_EDIT_TEMPLATE, 
                         booking=booking, 
                         form=form, 
                         move_start_date=booking.start_date, 
                         move_end_date=booking.end_date, 
                         cars=cars)



@booking_blueprint.route(BOOKING_DELETE_BP_ROUTE, methods=["POST"])
@login_required
def delete_booking(booking_id):
    current_app.logger.info(
        f"User {current_user.username} accessed delete booking with ID: {booking_id}"
    )
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    current_app.logger.warning(
        f"User {current_user.username} deleted booking with ID: {booking_id}"
    )
    return redirect(url_for(BOOKING_MAIN_ROUTE))


@booking_blueprint.route('/calendar', methods=["GET"])
@login_required
def calendar_view():
    cars = get_available_cars()

    start_date = get_start_date_from_request()
    current_week_title = get_week_title(start_date)

    dates = get_week_dates(start_date)
    last_day = start_date + timedelta(days=10)

    bookings = get_bookings_in_range(start_date, last_day)
    bookings_dict = map_bookings_to_dates(bookings, start_date, last_day)

    for car in cars:
        bookings_dict.setdefault(car.id, {})

    prev_start_date = start_date - timedelta(days=10)
    next_start_date = start_date + timedelta(days=10)

    return render_template(
        BOOKING_CALENDAR_TEMPLATE,
        cars=cars,
        dates=dates,
        current_week=current_week_title,
        bookings_dict=bookings_dict,
        prev_start_date=prev_start_date.strftime('%Y-%m-%d'),
        next_start_date=next_start_date.strftime('%Y-%m-%d'),
        BOOKING_STATUSES=BOOKING_STATUSES  # Передаем статусы в шаблон
    )
