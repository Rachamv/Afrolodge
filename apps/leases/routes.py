from flask import request, jsonify, render_template, Blueprint, flash, redirect, url_for
from flask_login import current_user, login_required
from apps import db
from apps.leases import blueprint
from apps.leases.models import Listing
from apps.leases.forms import ListingForm, AssetsMetadataForm, AdditionalFieldForm


@blueprint.route('/listings', methods=['POST'])
@login_required
def create_listing():
    data = request.form.to_dict()
    try:
        new_listing = Listing(**data)
        new_listing.save_to_db()
        return jsonify({'message': 'Listing created successfully', 'id': new_listing.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@blueprint.route('/listings', methods=['GET'])
@login_required
def view_listings():
    try:
        listings = Listing.search_listings()
        return render_template('listings_view.html', listings=listings)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@blueprint.route('/listings/<int:listing_id>/edit', methods=['GET'])
@login_required
def update_listing_form(listing_id):
    existing_listing = Listing.find_by_id(listing_id)
    return render_template('update_listing.html', listing=existing_listing)

@blueprint.route('/listings/<int:listing_id>', methods=['PUT'])
@login_required
def update_listing(listing_id):
    data = request.form.to_dict()
    existing_listing = Listing.find_by_id(listing_id)

    if existing_listing:
        try:
            existing_listing.update_listing(data)
            return jsonify({'message': 'Listing updated successfully', 'id': existing_listing.id})
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'message': 'Listing not found'}), 404

@blueprint.route('/listings/<int:listing_id>', methods=['DELETE'])
@login_required
def delete_listing(listing_id):
    existing_listing = Listing.find_by_id(listing_id)

    if existing_listing:
        try:
            existing_listing.delete_listing()
            return jsonify({'message': 'Listing deleted successfully', 'id': listing_id})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'message': 'Listing not found'}), 404
