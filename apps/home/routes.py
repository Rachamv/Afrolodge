from apps.home import blueprint
from flask import render_template, request
from apps.utils import get_greeting
from apps.leases.models import Listing
from flask_login import current_user

from flask import request

@blueprint.route('/', methods=['GET'])
def home():
    try:
        page = int(request.args.get('page', 1))
        per_page = 20
        offset = (page - 1) * per_page
        listings = Listing.query.offset(offset).limit(per_page).all()
        return render_template('home/index.html', listings=listings, greeting=get_greeting(), user=current_user, page=page)
    except Exception as e:
        print(f"Error fetching listings: {e}")
        return render_template('home/page-404.html', error="Error loading listings", greeting=get_greeting(), user=current_user)
