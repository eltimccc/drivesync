from flask import Blueprint, render_template, request, current_app

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def page_not_found(e):
    current_app.logger.warning(f'PAGE NOT FOUND: {request.url}')
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(500)
def internal_server_error(e):
    current_app.logger.error(f'INTERNAL SERVER ERROR at {request.url}: {e}')
    return render_template('errors/500.html'), 500
