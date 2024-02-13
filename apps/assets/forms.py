from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired

class CreateAssetForm(FlaskForm):
    assets_type = StringField('Asset Type', validators=[DataRequired()])
    house_type = StringField('Room Type', validators=[DataRequired()])
    accommodates = IntegerField('Accommodates', validators=[DataRequired()])
    bathrooms = FloatField('Bathrooms', validators=[DataRequired()])
    bedrooms = IntegerField('Bedrooms', validators=[DataRequired()])
    beds = IntegerField('Beds', validators=[DataRequired()])
    bed_type = StringField('Bed Type', validators=[DataRequired()])
    amenities = StringField('Amenities')
    square_feet = FloatField('Square Feet')
    guests_included = IntegerField('Guests Included', validators=[DataRequired()])
    extra_people = FloatField('Extra People', validators=[DataRequired()])
    minimum_nights = IntegerField('Minimum Nights')
    maximum_nights = IntegerField('Maximum Nights')
    location_id = IntegerField('Location ID', validators=[DataRequired()])
    rate_type = SelectField('Rate Type', choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], validators=[DataRequired()])
