from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from apps import db
from apps.leases.models import Listing
from apps.leases import blueprint
from apps.leases.forms import ListingForm, UpdateListingForm
from apps.authentication.models import Users
from apps.assets.models import Assets
from apps.utils import get_greeting

@blueprint.route('/create_list', methods=['GET', 'POST'])
@login_required
def create_listing():
    form = ListingForm()
    print(form.data)
    form_valid = form.validate_on_submit()
    print(f"Form is valid: {form_valid}")
    if form_valid:
        # Check if the provided asset_id belongs to the current user
        owned_assets = Assets.query.filter_by(user_id=current_user.id).all()
        asset_ids = [asset.id for asset in owned_assets]

        if form.asset_id.data not in asset_ids:
            flash('You can only create listings for your own assets.', 'error')
            return redirect(url_for('leases.create_listing'))

        new_listing = Listing(
            user_id=current_user.id,
            asset_id=form.asset_id.data,
            name=form.name.data,
            summary=form.summary.data,
            description=form.description.data,
            listing_image=form.listing_image.data,
            currency=form.currency.data,
            price=form.price.data,
            instant_bookable=form.instant_bookable.data,
            overall_satisfaction=form.overall_satisfaction.data
        )

        try:
            db.session.add(new_listing)
            db.session.commit()
            flash('Listing created successfully!', 'success')
            print("Redirecting to dashboard...")
            return redirect(url_for('authentication_blueprint.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating listing: {str(e)}', 'error')
    print(f"Form errors: {form.errors}")
    return render_template('leases/create_listing.html', form=form)


@blueprint.route('/listing/<int:listing_id>', methods=['GET'])
@login_required
def view_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    return render_template('leases/listing_detail.html', listing=listing, greeting=get_greeting(), user=current_user)

@blueprint.route('/listing/<int:listing_id>', methods=['PUT'])
@login_required
def update_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    form = UpdateListingForm(obj=listing)

    if form.validate_on_submit():
        form.populate_obj(listing)

        try:
            db.session.commit()
            flash('Listing updated successfully!', 'success')
            return redirect(url_for('leases.view_listings'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating listing: {str(e)}', 'error')

    return render_template('leases/update_listing.html', form=form, listing=listing)

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

def get_listings(user_id):
    listing_info = None
    user = Users.query.get(user_id)
    print(user)

    if user:
        print(user.listing)

        if user.listing:
            listing_info = Listing.query.filter_by(user_id=user_id).with_entities(Listing.id, Listing.name).all()
            print(listing_info)
    return listing_info



