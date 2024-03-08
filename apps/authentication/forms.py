from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField
from wtforms.validators import Email, DataRequired, EqualTo, Length

# login and registration


class LoginForm(FlaskForm):
    username = StringField('Username',
                           id='username_login',
                           validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = StringField('Username',
                           id='username_create',
                           validators=[DataRequired()])
    name = StringField('Fullname',
                       id='name_create',
                       validators=[DataRequired()])
    phone = StringField('Phone',
                        id='phone_create',
                        validators=[DataRequired()])
    email = StringField('Email',
                        id='email_create',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     id='confirm_pwd_create',
                                     validators=[DataRequired(), EqualTo('password')])

class UpdateProfileForm(FlaskForm):
    name = StringField('Fullname', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    about = StringField('About')
    profile_pic = StringField('Profile Picture URL')
    response_time = FloatField('Response Time')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])