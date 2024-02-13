
from flask import render_template, redirect, url_for, flash, request, abort
from apps.assets import blueprint
from flask_login import login_required, current_user
from apps.assets.forms import CreateAssetForm
from apps.area.models import Location
from apps.assets.models import Assets
from apps.review.models import Review
from apps import db
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError


@blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_asset():
    form = CreateAssetForm()
    if form.validate_on_submit():
        location = Location.query.get(form.location_id.data)

        if not location:
            flash('Location not found.', 'error')
            return redirect(url_for('some_location_form'))

        new_asset = Assets(
            user=current_user,
            location=location,
            assets_type=form.assets_type.data,
            house_type=form.room_type.data,
            accommodates=form.accommodates.data,
            bathrooms=form.bathrooms.data,
            bedrooms=form.bedrooms.data,
            beds=form.beds.data,
            bed_type=form.bed_type.data,
            amenities=form.amenities.data,
            square_feet=form.square_feet.data,
            guests_included=form.guests_included.data,
            extra_people=form.extra_people.data,
            minimum_nights=form.minimum_nights.data,
            maximum_nights=form.maximum_nights.data,
            rate_type=form.rate_type.data
        )

        try:
            db.session.add(new_asset)
            db.session.commit()
            flash('Asset created successfully!', 'success')
            return redirect(url_for('assets.details', assets_id=new_asset.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating asset: {str(e)}', 'error')

    return render_template('assets/create_asset_form.html', form=form)
#/assets/create

@blueprint.route('/assets/<int:assets_id>', methods=['GET'])
def details(assets_id):
    asset = Assets.query.get_or_404(assets_id)
    recent_reviews = Review.query.filter_by(asset_id=assets_id).order_by(desc(Review.timestamp)).limit(10).all()
    return render_template('assets/asset_details.html', asset=asset, recent_reviews=recent_reviews)

@blueprint.route('/assets/<int:assets_id>/edit', methods=['GET', 'POST'])
@login_required
def update_assets_form(assets_id):
    asset = Assets.query.get_or_404(assets_id)

    if asset.user != current_user:
        abort(403)

    # Check authorized user permission (if applicable)
    if not current_user.has_permission('edit_asset', asset):
        flash('Unauthorized to edit this asset.', 'error')
        return redirect(url_for('home'))

    form = CreateAssetForm(obj=asset)
    if form.validate_on_submit():
        try:
            # Use relationship property for direct update (if applicable)
            if hasattr(asset, 'assets_type'):
                asset.assets_type = form.assets_type.data
                asset.house_type = form.room_type.data
                asset.accommodates=form.accommodates.data,
                asset.bathrooms=form.bathrooms.data,
                asset.bedrooms=form.bedrooms.data,
                asset.beds=form.beds.data,
                asset.bed_type=form.bed_type.data,
                asset.amenities=form.amenities.data,
                asset.square_feet=form.square_feet.data,
                asset.guests_included=form.guests_included.data,
                asset.extra_people=form.extra_people.data,
                asset.minimum_nights=form.minimum_nights.data,
                asset.maximum_nights=form.maximum_nights.data,
                asset.rate_type=form.rate_type.data
            else:
                form.populate_obj(asset)

            db.session.commit()
            flash('Asset updated successfully!', 'success')
            return redirect(url_for('assets.details', assets_id=assets_id))

        except IntegrityError as e:
            db.session.rollback()
            flash('Error updating asset: Database constraint violated. '
                  f'Please check your data and try again.', 'error')
        except Exception as e:  # Catch other exceptions
            db.session.rollback()
            flash(f'Error updating asset: {str(e)}', 'error')

    return render_template('assets/update_asset_form.html', form=form, asset=asset)


@blueprint.route('/assets/<int:assets_id>', methods=['DELETE'])
def delete_assets(assets_id):
    asset = Assets.query.get_or_404(assets_id)

    try:
        db.session.delete(asset)
        db.session.commit()
        flash('Asset deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting asset: {str(e)}', 'error')

    return redirect(url_for('home'))
