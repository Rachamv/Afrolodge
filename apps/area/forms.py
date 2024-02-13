from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField
from wtforms.validators import DataRequired, NumberRange

class LocationForm(FlaskForm):
    house_number = StringField('House Number', validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    neighborhood = StringField('Neighborhood', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zipcode = StringField('Zipcode', validators=[DataRequired()])
    market = StringField('Market')
    country_code = StringField('Country Code', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    latitude = FloatField('Latitude', validators=[NumberRange(min=-90, max=90)])
    longitude = FloatField('Longitude', validators=[NumberRange(min=-180, max=180)])
    is_location_exact = BooleanField('Is Location Exact')
