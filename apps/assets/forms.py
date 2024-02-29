from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Optional

class CreateAssetForm(FlaskForm):
    assets_type = StringField('Asset Type', validators=[DataRequired()])
    accommodates = IntegerField('Accommodates', validators=[DataRequired()])
    bathrooms = IntegerField('Bathrooms', validators=[DataRequired()])
    bedrooms = IntegerField('Bedrooms', validators=[DataRequired()])
    description = StringField('Description', validators=[Optional()])
    amenities = StringField('Amenities', validators=[Optional()])
    minimum_nights = IntegerField('Minimum Nights', validators=[Optional()])
    location_id = IntegerField('Location ID', validators=[DataRequired()])