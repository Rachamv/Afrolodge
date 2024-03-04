from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, FloatField, IntegerField
from wtforms.validators import DataRequired, Optional, NumberRange

class ListingForm(FlaskForm):
    asset_id = IntegerField('Asset ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    summary = StringField('Summary', validators=[Optional()])
    description = StringField('Description', validators=[Optional()])
    accommodates = IntegerField('Accommodates', validators=[DataRequired()])
    listing_image = StringField('Picture', validators=[Optional()])
    currency = StringField('Currency', validators=[Optional()])
    price = FloatField('Price', validators=[Optional(), NumberRange(min=0.01)])
    instant_bookable = BooleanField('Instant Bookable', validators=[Optional()])
    overall_satisfaction = FloatField('Overall Satisfaction', validators=[Optional(), NumberRange(min=0, max=5)])
