from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired

# class EditBookingForm(FlaskForm):
#     start_datetime = DateTimeField('Start Date and Time', validators=[DataRequired()])
#     end_datetime = DateTimeField('End Date and Time', validators=[DataRequired()])
#     car_id = StringField('Car ID', validators=[DataRequired()])
#     description = StringField('Description')


class EditBookingForm(FlaskForm):
    description = TextAreaField('Description', validators=[DataRequired()])
    start_date = DateTimeField('Start Date and Time', format='%Y-%m-%dT%H:%M',
                               validators=[DataRequired()], default=datetime.now)
    end_date = DateTimeField('End Date and Time', format='%Y-%m-%dT%H:%M',
                             validators=[DataRequired()], default=datetime.now)
    