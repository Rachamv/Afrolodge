from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from apps import db
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm, UpdateProfileForm, ChangePasswordForm, ForgotPasswordForm
from apps.authentication.models import Users
from apps.area.models import Location
from apps.leases.models import Listing
from apps.assets.models import Assets
from apps.authentication.util import verify_pass
from apps.utils import get_greeting

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)

    if request.method == 'POST' and login_form.validate():
        username = login_form.username.data
        password = login_form.password.data
        remember = login_form.remember.data

        user = Users.query.filter_by(username=username).first()

        if user and verify_pass(password, user.password):
            login_user(user, remember_me=remember)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home_blueprint.home'))
        else:
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

        # Check username, email, and phone uniqueness
        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            return render_template('accounts/register.html', msg='Username already registered', success=False, form=create_account_form)

        existing_email = Users.query.filter_by(email=email).first()
        if existing_email:
            return render_template('accounts/register.html', msg='Email already registered', success=False, form=create_account_form)

        existing_phone = Users.query.filter_by(phone=phone).first()
        if existing_phone:
            return render_template('accounts/register.html', msg='Phone Number already registered', success=False, form=create_account_form)

        # Check if passwords match
        if password != confirm_password:
            return render_template('accounts/register.html', msg='Passwords do not match', success=False, form=create_account_form)

        new_user = Users(username=username, name=name, phone=phone, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('authentication_blueprint.login'))

    return render_template('accounts/register.html', form=create_account_form)

@blueprint.route('/dashboard')
@login_required
def dashboard():
    user_id = current_user.id
    welcome_message = f"Welcome, {current_user.name}!"
    location_info = Location.query.get(current_user.location_id) if current_user.location_id else None
    listings_info = Listing.query.with_entities(Listing.id, Listing.name).all()
    assets_info = Assets.query.with_entities(Assets.id, Assets.assets_type).all()

    return render_template('home/profile.html',
                           user_id=user_id,
                           welcome_message=welcome_message,
                           user=current_user,
                           location_info=location_info,
                           listings_info=listings_info,
                           assets_info=assets_info,
                           greeting=get_greeting())

@blueprint.route('/dashboard/edit_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    form = UpdateProfileForm(request.form)

    if request.method == 'POST' and form.validate():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.about = form.about.data
        current_user.location_id = form.location_id.data
        current_user.response_time = form.response_time.data

        if form.profile_pic.data:
            picture_data = form.profile_pic.data.read()
            current_user.set_profile_picture(picture_data)

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('authentication_blueprint.dashboard'))

    return render_template('accounts/edit_profile.html', form=form)


@blueprint.route('/dashboard/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm(request.form)

    if request.method == 'POST' and form.validate():
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data

        # Verify if the current password is correct
        if not verify_pass(current_password, current_user.password):
            flash('Incorrect current password. Please try again.', 'error')
            return redirect(url_for('authentication_blueprint.change_password'))

        # Verify if the new password matches the confirm password
        if new_password != confirm_password:
            flash('New password and confirm password do not match.', 'error')
            return redirect(url_for('authentication_blueprint.change_password'))

        # Update the password
        current_user.update_password(new_password)
        db.session.commit()

        flash('Password changed successfully!', 'success')
        return redirect(url_for('authentication_blueprint.dashboard'))

    return render_template('accounts/change_password.html', form=form)

