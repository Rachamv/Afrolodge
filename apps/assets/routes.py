from flask import render_template, redirect, url_for, flash, request, abort,  jsonify
from apps.assets import blueprint
from flask_login import login_required, current_user
from apps.assets.forms import CreateAssetForm
from apps.area.models import Location
from apps.authentication.models import Users
from apps.assets.models import Assets
from apps.review.models import Review
from apps import db
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from apps.utils import get_greeting


@blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_asset():
    form = CreateAssetForm()
    if form.validate_on_submit():
        location = Location.query.get(form.location_id.data)

        if not location:
            flash('Location not found.', 'error')
            return redirect(url_for('area/edit_location.html'))

        new_asset = Assets(
            user=current_user,
            location=location,
            assets_type=form.assets_type.data,
            accommodates=form.accommodates.data,
            bathrooms=form.bathrooms.data,
            bedrooms=form.bedrooms.data,
            beds=form.beds.data,
            description=form.description.data,
            amenities=form.amenities.data,
            minimum_nights=form.minimum_nights.data,
        )

        try:
            db.session.add(new_asset)
            db.session.commit()
            flash('Asset created successfully!', 'success')
            return redirect(url_for('authentication_blueprint.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating asset: {str(e)}', 'error')

    return render_template('assets/create_asset_form.html', form=form)


@blueprint.route('/assets/<int:assets_id>', methods=['GET'])
def details(assets_id):
    asset = Assets.query.get_or_404(assets_id)
    recent_reviews = Review.query.filter_by(asset_id=assets_id).order_by(desc(Review.timestamp)).limit(10).all()
    return render_template('assets/asset_details.html', asset=asset, recent_reviews=recent_reviews)

@blueprint.route('/assets/<int:assets_id>', methods=['GET'])
@login_required
def view_assets(assets_id):
    asset = Assets.query.get_or_404(assets_id)
    return render_template('assets/assets_detail.html', asset=asset, greeting=get_greeting(), user=current_user)

@blueprint.route('/update_assets_form/<int:assets_id>', methods=['GET', 'POST'])
@login_required
def update_assets_form(assets_id):
    asset = Assets.query.get_or_404(assets_id)

    if asset.user != current_user:
        abort(403)

    form = CreateAssetForm(obj=asset)
    if form.validate_on_submit():
        try:
            form.populate_obj(asset)
            db.session.commit()
            flash('Asset updated successfully!', 'success')
            return redirect(url_for('assets.details', assets_id=assets_id))
        except IntegrityError as e:
            db.session.rollback()
            flash('Error updating asset: Database constraint violated. '
                  'Please check your data and try again.', 'error')
        except Exception as e:
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


def get_assets(user_id):
    """
    Retrieve assets associated with the given user ID.
    """
    asset_info = None
    user = Users.query.get(user_id)
    if user:
        if user.assets:
            asset_info = Assets.query.filter_by(user_id=user_id).with_entities(Assets.id, Assets.assets_type).all()
    return asset_info
