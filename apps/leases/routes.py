from flask import request, render_template, Blueprint, flash, redirect, url_for
from flask_login import login_required, current_user
from apps import db
from apps.leases import blueprint
from apps.leases.models import Listing, AssetsMetadata, AdditionalField
from apps.leases.forms import ListingForm, AssetsMetadataForm, AdditionalFieldForm
from apps.area.models import Location
from apps.assets.models import Assets
from apps.utils import get_greeting

@blueprint.route('/create_list', methods=['GET', 'POST'])
@login_required
def create_listing():
    form = ListingForm()
    if form.validate_on_submit():
        # Retrieve the location object based on the location_id from the form
        location = Location.query.get(form.location_id.data)
        assets = Assets.query.get(form.asset_id.data)

        if not assets:
            flash('Asset not found.', 'error')
            return redirect(url_for('assets/create_asset_form.html'))

        if not location:
            flash('Location not found.', 'error')
            return redirect(url_for('area/edit_location_form.html'))

        new_listing = Listing(
            asset_id=form.asset_id.data,
            location_id=form.location_id.data,
            name=form.name.data,
            summary=form.summary.data,
            description=form.description.data,
            experiences_offered=form.experiences_offered.data,
            neighborhood_overview=form.neighborhood_overview.data,
            notes=form.notes.data,
            transit=form.transit.data,
            access=form.access.data,
            interaction=form.interaction.data,
            house_rules=form.house_rules.data,
            picture_url=form.picture_url.data,
            currency=form.currency.data,
            price=form.price.data,
            daily_price=form.daily_price.data,
            weekly_price=form.weekly_price.data,
            monthly_price=form.monthly_price.data,
            security_deposit=form.security_deposit.data,
            cleaning_fee=form.cleaning_fee.data,
            instant_bookable=form.instant_bookable.data,
            overall_satisfaction=form.overall_satisfaction.data

        )

        try:
            db.session.add(new_listing)
            db.session.commit()
            flash('Listing created successfully!', 'success')
            return redirect(url_for('authentication_blueprint.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating listing: {str(e)}', 'error')

    return render_template('leases/create_listing.html', form=form)

@blueprint.route('/create_assets_metadata', methods=['POST'])
@login_required
def create_assets_metadata():
    form = AssetsMetadataForm(request.form)
    if form.validate_on_submit():
        new_assets_metadata = AssetsMetadata()
        form.populate_obj(new_assets_metadata)

        try:
            db.session.add(new_assets_metadata)
            db.session.commit()
            flash('Assets metadata created successfully!', 'success')
            return redirect(url_for('leases.view_assets_metadata'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating assets metadata: {str(e)}', 'error')

    return render_template('assets/create_assets_metadata_form.html', form=form)

@blueprint.route('/create_additional_field', methods=['POST'])
@login_required
def create_additional_field():
    form = AdditionalFieldForm(request.form)
    if form.validate_on_submit():
        new_additional_field = AdditionalField()
        form.populate_obj(new_additional_field)

        try:
            db.session.add(new_additional_field)
            db.session.commit()
            flash('Additional field created successfully!', 'success')
            return redirect(url_for('leases.view_additional_fields'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating additional field: {str(e)}', 'error')

    return render_template('assets/create_additional_field_form.html', form=form)

# @blueprint.route('/listing/<int:listing_id>', methods=['GET'])
# @login_required
# def view_listing(listing_id):
#     listing = Listing.query.get_or_404(listing_id)
#     listings = Listing.query.offset(offset).limit(per_page).all()
#     return render_template('home/assets_detail.html', listing=listing, greeting=get_greeting(), user=current_user)

@blueprint.route('/listings/<int:listing_id>', methods=['PUT'])
@login_required
def update_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    form = ListingForm(request.form)
    if form.validate():
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

@blueprint.route('/listings/<int:listing_id>', methods=['DELETE'])
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
