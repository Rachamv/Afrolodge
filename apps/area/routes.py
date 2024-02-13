from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from apps import db
from apps.area import blueprint
from apps.area.models import Location
from apps.area.forms import LocationForm

@blueprint.route('/edit_location', methods=['GET', 'POST'])
@login_required
def edit_location():
    form = LocationForm()

    if form.validate_on_submit():
        house_number = form.house_number.data
        street = form.street.data
        neighborhood = form.neighborhood.data
        city = form.city.data
        state = form.state.data
        zipcode = form.zipcode.data
        market = form.market.data
        country_code = form.country_code.data
        country = form.country.data
        latitude = form.latitude.data
        longitude = form.longitude.data
        is_location_exact = form.is_location_exact.data

        # Check if the user already has a location entry
        if current_user.location_id:
            location = Location.query.get(current_user.location_id)
        else:
            location = Location()

        location.house_number = house_number
        location.street = street
        location.neighborhood = neighborhood
        location.city = city
        location.state = state
        location.zipcode = zipcode
        location.market = market
        location.country_code = country_code
        location.country = country
        location.latitude = latitude
        location.longitude = longitude
        location.is_location_exact = is_location_exact

        db.session.add(location)
        db.session.commit()

        # Associate the location with the user
        current_user.location_id = location.id
        db.session.commit()

        flash('Location information updated successfully!', 'success')
        return redirect(url_for('authentication_blueprint.dashboard'))

    return render_template('area/edit_location.html', form=form)
