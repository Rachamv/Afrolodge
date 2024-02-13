from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, FloatField, IntegerField
from wtforms.validators import DataRequired, Optional, NumberRange

class ListingForm(FlaskForm):
    asset_id = IntegerField('Asset ID', validators=[DataRequired()])
    location_id = IntegerField('Location ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    summary = StringField('Summary')
    description = StringField('Description')
    experiences_offered = StringField('Experiences Offered')
    neighborhood_overview = StringField('Neighborhood Overview')
    notes = StringField('Notes')
    transit = StringField('Transit')
    access = StringField('Access')
    interaction = StringField('Interaction')
    house_rules = StringField('House Rules')
    picture_url = StringField('Picture URL')
    currency = StringField('Currency')
    price = FloatField('Price', validators=[Optional()])
    daily_price = FloatField('Daily Price', validators=[Optional()])
    weekly_price = FloatField('Weekly Price', validators=[Optional()])
    monthly_price = FloatField('Monthly Price', validators=[Optional()])
    security_deposit = FloatField('Security Deposit', validators=[Optional()])
    cleaning_fee = FloatField('Cleaning Fee', validators=[Optional()])
    instant_bookable = BooleanField('Instant Bookable', validators=[Optional()])
    overall_satisfaction = FloatField('Overall Satisfaction', validators=[Optional(), NumberRange(min=0, max=5)])

class AssetsMetadataForm(FlaskForm):
    license = StringField('License')
    cancellation_policy = StringField('Cancellation Policy')
    require_guest_profile_picture = BooleanField('Require Guest Profile Picture')
    require_guest_phone_verification = BooleanField('Require Guest Phone Verification')
    listing_id = IntegerField('Listing ID', validators=[DataRequired()])
    user_id = IntegerField('User ID', validators=[DataRequired()])

class AdditionalFieldForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    value = StringField('Value', validators=[DataRequired()])
    assets_metadata_id = IntegerField('Assets Metadata ID', validators=[DataRequired()])
