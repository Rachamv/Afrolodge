from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, BooleanField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class ListingForm(FlaskForm):
    """Form for creating a new listing."""
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    summary = StringField('Summary', validators=[DataRequired(), Length(max=255)])
    description = StringField('Description', validators=[DataRequired(), Length(max=1000)])
    accommodates = IntegerField('Accommodates', validators=[DataRequired(), NumberRange(min=1)])
    picture = StringField('Picture', validators=[DataRequired(), Length(max=255)])
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=0)])
    instant_bookable = BooleanField('Instant Bookable')
    overall_satisfaction = FloatField('Overall Satisfaction', validators=[Optional(), NumberRange(min=1, max=5)])

class BookingForm(FlaskForm):
    """Form for making a booking."""
    checkin_date = DateField('Check-in Date', validators=[DataRequired()])
    checkout_date = DateField('Check-out Date', validators=[DataRequired()])
    num_guests = IntegerField('Number of Guests', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Book Now')

class AvailabilityForm(FlaskForm):
    """Form for updating availability."""
    date = DateField('Date', validators=[DataRequired()])
    available = BooleanField('Available')
    submit = SubmitField('Update Availability')
