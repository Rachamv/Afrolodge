from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from apps import db
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users
from apps.area.models import Location
from apps.authentication.util import verify_pass, save_user_to_db


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)

    if request.method == 'POST' and login_form.validate():
        username = login_form.username.data
        password = login_form.password.data
        user = Users.query.filter_by(username=username).first()

        if user and verify_pass(password, user.password):
            login_user(user, remember=True)

        flash('Wrong username or password', 'error')

    if not current_user.is_authenticated:
        registration_msg = flash('Registration successful!', 'success')
        return render_template('accounts/login.html', form=login_form, registration_msg=registration_msg)

    return redirect(url_for('home_blueprint.home'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('authentication_blueprint.login'))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if create_account_form.validate_on_submit():
        username = create_account_form.username.data
        name = create_account_form.name.data
        phone = create_account_form.phone.data
        email = create_account_form.email.data
        password = create_account_form.password.data
        confirm_password = create_account_form.confirm_password.data


        # Check username exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)
        # Check phone exists
        user = Users.query.filter_by(phone=phone).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Phone Number already registered',
                                   success=False,
                                   form=create_account_form)

        # Check if passwords match
        if password != confirm_password:
            return render_template('accounts/register.html',
                                   msg='Passwords do not match',
                                   success=False,
                                   form=create_account_form)

        # Add logic to create a new user (using your model, e.g., Users)
        new_user = Users(username=username,  name=name, phone=phone, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('authentication_blueprint.login'))

    return render_template('accounts/register.html', form=create_account_form)

@blueprint.route('/dashboard')
@login_required
def dashboard():
    # Retrieve user information
    user_id = current_user.id
    welcome_message = f"Welcome, {current_user.name}!"

    # Get location information if available
    location_info = None
    if current_user.location_id:
        location_info = Location.query.get(current_user.location_id)

    return render_template('home//profile.html',
                           user_id=user_id,
                           welcome_message=welcome_message,
                           user=current_user,
                           location_info=location_info)



# @blueprint.route('/dashboard/edit_profile', methods=['GET', 'POST'])
# @login_required
# def update_profile():

# @blueprint.route('/dashboard/change_password', methods=['GET', 'POST'])
# @login_required
# def change_password():
