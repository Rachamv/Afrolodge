from flask import render_template, redirect, request, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from apps import db
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm, ChangePasswordForm, UpdateProfileForm
from apps.authentication.models import Users
from apps.authentication.util import verify_pass, hash_pass
from apps.utils import get_greeting
from apps.leases.routes import get_listings
from apps.assets.routes import get_assets
from apps.area.routes import get_location


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

        new_user = Users(username=username,  name=name, phone=phone, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('login'))

    return render_template('accounts/register.html', form=create_account_form)

@blueprint.route('/dashboard')
@login_required
def dashboard():
    # Retrieve user information
    user_id = current_user.id
    welcome_message = f"Welcome, {current_user.name}!"

    # Get information if available
    location_info = get_location(user_id)
    listing_info = get_listings(user_id)
    asset_info = get_assets(user_id)

    # Debugging print statements
    print("Listing info:", listing_info)

    return render_template('home/profile.html',
                           user_id=user_id,
                           welcome_message=welcome_message,
                           user=current_user,
                           location_info=location_info,
                           listing_info=listing_info,
                           asset_info=asset_info,
                           greeting=get_greeting())


@blueprint.route('/dashboard/edit_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    update_profile_form = UpdateProfileForm(obj=current_user)

    if update_profile_form.validate_on_submit():
        # Update user information
        current_user.name = update_profile_form.name.data
        current_user.phone = update_profile_form.phone.data
        current_user.email = update_profile_form.email.data
        current_user.about = update_profile_form.about.data
        current_user.profile_pic = update_profile_form.profile_pic.data
        current_user.response_time = update_profile_form.response_time.data

        db.session.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('authentication_blueprint.dashboard'))

    return render_template('accounts/update_profile.html', form=update_profile_form)

@blueprint.route('/dashboard/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    change_password_form = ChangePasswordForm()

    if change_password_form.validate_on_submit():
        current_password = change_password_form.current_password.data
        new_password = change_password_form.new_password.data

        # Verify the current password
        if not verify_pass(current_password, current_user.password):
            flash('Current password is incorrect', 'error')
            return redirect(url_for('authentication_blueprint.change_password'))

        # Update the password
        current_user.password = hash_pass(new_password)
        db.session.commit()

        flash('Password changed successfully!', 'success')
        return redirect(url_for('authentication_blueprint.login'))

    return render_template('accounts/change_password.html', form=change_password_form)
