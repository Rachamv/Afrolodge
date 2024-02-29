from flask import request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from apps import db
from apps.leases import blueprint
from apps.leases.models import Listing
from apps.leases.forms import ListingForm
from apps.area.models import Location
from apps.assets.models import Assets
from apps.utils import get_greeting

@blueprint.route('/create_listing', methods=['GET', 'POST'])
@login_required
def create_listing():
    form = ListingForm()
    if form.validate_on_submit():
        location = Location.query.get(form.location_id.data)
        assets = Assets.query.get(form.asset_id.data)

        if not assets:
            flash('Asset not found.', 'error')
            return redirect(url_for('assets.create_asset_form'))

        if not location:
            flash('Location not found.', 'error')
            return redirect(url_for('area.edit_location_form'))

        new_listing = Listing(
            asset_id=form.asset_id.data,
            location_id=form.location_id.data,
            name=form.name.data,
            summary=form.summary.data,
            description=form.description.data,
            accommodates=form.accommodates.data,
            price=form.price.data,
            instant_bookable=form.instant_bookable.data,
            overall_satisfaction=form.overall_satisfaction.data
        )

        try:
            db.session.add(new_listing)
            db.session.commit()
            flash('Listing created successfully!', 'success')
            return redirect(url_for('authentication.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating listing: {str(e)}', 'error')

    return render_template('leases/create_listing.html', form=form)


@blueprint.route('/listing/<int:listing_id>', methods=['GET'])
@login_required
def view_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    return render_template('home/assets_detail.html', listing=listing, greeting=get_greeting(), user=current_user)

@blueprint.route('/listing/<int:listing_id>', methods=['PUT'])
@login_required
def update_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    form = ListingForm()
    if form.validate_on_submit():
        form.populate_obj(listing)
        try:
            db.session.commit()
            flash('Listing updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating listing: {str(e)}', 'error')
    else:
        flash('Form validation failed!', 'error')
    return redirect(url_for('leases.view_listings'))

@blueprint.route('/listing/<int:listing_id>', methods=['DELETE'])
@login_required
def delete_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    try:
        db.session.delete(listing)
        db.session.commit()
        flash('Listing deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting listing: {str(e)}', 'error')
    return redirect(url_for('leases.view_listings'))
