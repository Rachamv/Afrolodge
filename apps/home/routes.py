from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required, current_user
from apps import db
from apps.leases.models import Listing

@blueprint.route('/')
def home():
    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page

    try:
        listings = Listing.query.limit(per_page).offset(offset).all()
        return render_template('home/index.html', listings=listings, page=page, greeting=get_greeting(), user=current_user)
    except Exception as e:
        print(f"Error fetching listings: {e}")
        return render_template('home/page-404.html', error="Error loading listings", user=current_user)

@blueprint.route('/listing/<int:listing_id>', methods=['GET'])
@login_required
def view_listing(listing_id):
    try:
        listing = Listing.query.get_or_404(listing_id)
        return render_template('home/assetsdetail.html', listing=listing, greeting=get_greeting(), user=current_user)
    except Exception as e:
        print(f"Error fetching listing {listing_id}: {e}")
        return render_template('home/page-404.html', error="Listing not found", user=current_user)
    finally:
        db.session.close()

def get_greeting():
    return f"Welcome {current_user.username}" if current_user.is_authenticated else "Afrolodge your home"
