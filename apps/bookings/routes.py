from apps import db
from apps.leases.models import Booking
from apps.bookings import blueprint
from flask import flash, render_template, request, redirect, url_for
from apps.utils import get_greeting
from apps.leases.models import Listing
from flask_login import login_required, current_user
from apps.authentication.models import Users
from flask_mail import Message


def send_booking_email(user, booking):
   message = Message('Booking Confirmation',
                recipients=[user.email])
   mail.send(message)

@blueprint.route('/create', methods=['GET', 'POST'])
def create_booking():
    if request.method == 'POST':
        try:
            listing_id = request.form['listing_id']
            checkin_date = request.form['checkin_date']
            checkout_date =  request.form['checkout_date']
            guests = request.form['guests']

            listing = Listing.query.get(listing_id)
            price_per_day = listing.price

            # Calculate total booking price
            days = (checkout_date - checkin_date).days
            total_price = price_per_day * days

            if listing.availability == False:
                flash('Listing is not available for selected dates')

                return redirect(url_for('listings'))

            # Create booking object
            booking = Booking(listing_id=listing_id,
                            name=current_user.name,
                            email=current_user.email,
                            checkin_date=checkin_date,
                            checkout_date=checkout_date,
                            guests=guests,
                            total_price=total_price)

            send_booking_email(current_user, booking)

            # Save to db
            db.session.add(booking)
            db.session.commit()

            flash('Booking created successfully!')
            return render_template('confirmation.html', booking=booking)

        except Exception as e:
            # Log the error or handle it in a better way for your application
            print(f"Error creating booking: {e}")
            flash('An error occurred while creating the booking. Please try again.')
            return redirect(url_for('listings'))


    return render_template('create_booking.html')