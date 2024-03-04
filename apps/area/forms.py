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
    is_location_exact = BooleanField('Is Location Exact')
