from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, FloatField, TimeField, StringField
from wtforms.validators import DataRequired, Optional, NumberRange

class CalendarForm(FlaskForm):
    listing_id = IntegerField('Listing ID', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    booked_by_user_id = IntegerField('Booked By User ID', validators=[DataRequired()])
    number_of_guests = IntegerField('Number of Guests', validators=[Optional(), NumberRange(min=1)])
    total_price = FloatField('Total Price', validators=[Optional()])
    check_in_time = TimeField('Check-in Time', validators=[Optional()])
    check_out_time = TimeField('Check-out Time', validators=[Optional()])
    booking_status = StringField('Booking Status', validators=[Optional()])
