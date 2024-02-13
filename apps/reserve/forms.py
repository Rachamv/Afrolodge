from flask_wtf import FlaskForm
from wtforms import DateTimeField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from datetime import datetime

class BookingForm(FlaskForm):
    listing_id = IntegerField('Listing ID', validators=[DataRequired()])
    user_id = IntegerField('User ID', validators=[DataRequired()])
    checkin_date = DateTimeField('Check-in Date', format='%Y-%m-%dT%H:%M:%S', validators=[DataRequired()])
    checkout_date = DateTimeField('Check-out Date', format='%Y-%m-%dT%H:%M:%S', validators=[DataRequired()])
    num_guests = IntegerField('Number of Guests', validators=[DataRequired(), NumberRange(min=1)])

    def validate(self):
        if not super().validate():
            return False

        checkin_date = self.checkin_date.data
        checkout_date = self.checkout_date.data

        if checkin_date >= checkout_date:
            self.checkin_date.errors.append('Check-in date must be before check-out date')
            return False

        return True
