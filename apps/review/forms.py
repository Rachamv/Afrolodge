from flask_wtf import FlaskForm
from wtforms import DateTimeField, FloatField, TextAreaField
from wtforms.validators import DataRequired

class ReviewForm(FlaskForm):
    date = DateTimeField('Date', validators=[DataRequired()])
    reviewer_id = IntegerField('Reviewer ID', validators=[DataRequired()])
    rating = FloatField('Rating', validators=[DataRequired()])
    comments = TextAreaField('Comments')
