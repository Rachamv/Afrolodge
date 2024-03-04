from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, Optional

class CreateAssetForm(FlaskForm):
    assets_type = StringField('Asset Type', validators=[DataRequired()])
    accommodates = IntegerField('Accommodates', validators=[DataRequired()])
    bathrooms = FloatField('Bathrooms', validators=[DataRequired()])
    bedrooms = IntegerField('Bedrooms', validators=[DataRequired()])
    beds = IntegerField('Beds', validators=[DataRequired()])
    amenities = StringField('Amenities')
    description = StringField('Description', validators=[Optional()])
    minimum_nights = IntegerField('Minimum Nights')
    location_id = IntegerField('Location ID', validators=[DataRequired()])
