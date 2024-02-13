from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired, EqualTo

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
