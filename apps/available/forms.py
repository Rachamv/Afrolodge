from flask_wtf import FlaskForm
from wtforms import DateTimeField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Optional, NumberRange

class AvailabilityForm(FlaskForm):
    date = DateTimeField('Date', validators=[DataRequired()])
    available = BooleanField('Available', validators=[DataRequired()])
    availability_30 = IntegerField('Availability for 30 days', validators=[Optional(), NumberRange(min=0)])
    availability_60 = IntegerField('Availability for 60 days', validators=[Optional(), NumberRange(min=0)])
    availability_90 = IntegerField('Availability for 90 days', validators=[Optional(), NumberRange(min=0)])
    availability_365 = IntegerField('Availability for 365 days', validators=[Optional(), NumberRange(min=0)])
    listing_id = IntegerField('Listing ID', validators=[DataRequired()])
