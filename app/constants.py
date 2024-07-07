# Имена шаблонов
MAIN_TEMPLATE = "calendar_with_bookings.html"

# Blueprint маршруты MAIN
MAIN_BP_NAME_ROUTE = "main"

# Имена шаблонов CAR
CAR_EDIT_TEMPLATE = "edit_car.html"
CAR_DETAIL_TEMPLATE = "car_detail.html"
CAR_ADD_TEMPLATE = "add_car.html"
CAR_ADD_MODAL_TEMPLATE = "add_car_modal.html"
CARS_GET = "cars.html"

# Именованные маршруты CAR
CARS_GET_ROUTE = "car.get_cars"

# Blueprint маршруты CAR
CAR_BP_NAME_ROUTE = "car"
CAR_URL_PREFIX = "/car"
CAR_ADD_BP_ROUTE = "/add_car"
CARS_BP_ROUTE = "/cars"
CAR_DETAIL_BP_ROUTE = "/<int:car_id>"
CAR_EDIT_BP_ROUTE = "/<int:car_id>/edit"
CAR_DELETE_BP_ROUTE = "/<int:car_id>/delete"

# Имена шаблонов BOOKING
BOOKING_DETAIL_MODAL_TEMPLATE = "view_booking_modal.html"
BOOKING_DETAIL_TEMPLATE = "view_booking.html"
BOOKING_EDIT_TEMPLATE = "edit_booking.html"
BOOKING_ADD_TEMPLATE = "add_booking.html"
BOOKING_ALL_TEMPLATE = "all_bookings.html"
BOOKING_MODAL_TEMPLATE = "add_booking_modal.html"

# Именованные маршруты BOOKING
BOOKING_GET_ROUTE = "booking.get_bookings"
BOOKING_VIEW_BOOKING_ROUTE = "booking.view_booking"
BOOKING_EDIT_BOOKING_ROUTE = "booking.edit_booking"
BOOKING_MAIN_ROUTE = "main.get_bookings"
BOOKING = "booking.add_booking"
BOOKING_ALL_BOOKING_ROUTE = "booking.all_bookings"

# Blueprint маршруты BOOKING
BOOKING_BP_NAME_ROUTE = "booking"
BOOKING_VIEW_BP_ROUTE = "/<int:booking_id>"
BOOKING_ADD_BP_ROUTE = "/add_booking"
BOOKING_EDIT_BP_ROUTE = "/<int:booking_id>/edit"
BOOKING_DELETE_BP_ROUTE = "/delete_booking/<int:booking_id>/"
BOOKING_ALL_ROUTE = "/all_bookings"
BOOKING_URL_PREFIX = "/booking"

# Имена шаблонов REPORT
REPORT_BOOKING_PERIOD_TEMPLATE = "reports/bookings_for_period.html"
REPORT_PAGE_TEMPLATE = "reports/reports.html"
REPORT_RENTCAR_AMOUNT_TEMPLATE = "reports/report_rent_amount.html"
REPORT_STATUS_RENT_TEMPLATE = "reports/report_status_rent.html"
REPORT_BOOKING_DURATION_TEMPLATE = "reports/report_booking_duration.html"

SEARCH_AVAIALBLE_CARS_TEMPLATE = "available_cars.html"

# Blureprint маршруты REPORT
REPORT_BOOKING_PERIOD_BP_ROUTE = "/bookings_for_period"
REPORT_RENTCAR_AMOUNT_BP_ROUTE = "/report_rent_amount"
REPORT_STATUS_RENT_BP_ROUTE = "/report_status_rent"
REPORT_BOOKING_DURATION_BP_ROUTE = "/report_booking_duration"

SEARCH_CARS_BP_ROUTE = "/search_cars"

# Blureprint маршруты AUTH
AUTH_BP_NAME_ROUTE = "auth"
AUTH_URL_PREFIX = "/auth"
AUTH_REGISTER_BP_ROUTE = "/register"
AUTH_LOGIN_BP_ROUTE = "/login"
AUTH_LOGOUT_BP_ROUTE = "/logout"
AUTH_LIST_BP_ROUTE = "/users"

# Именованные маршруты AUTH
AUTH_REGISTER_ROUTE = "auth.register"

# Имена шаблонов AUTH
AUTH_REGISTER_TEMPLATE = "register.html"
AUTH_LOGIN_TEMPLATE = "login.html"
AUTH_LIST_TEMPLATE = "list_users.html"
