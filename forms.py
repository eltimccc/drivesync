from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField
from wtforms.validators import DataRequired

class EditBookingForm(FlaskForm):
    start_datetime = DateTimeField('Start Date and Time', validators=[DataRequired()])
    end_datetime = DateTimeField('End Date and Time', validators=[DataRequired()])
    car_id = StringField('Car ID', validators=[DataRequired()])
    description = StringField('Description')



