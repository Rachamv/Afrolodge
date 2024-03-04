from apps import db
from sqlalchemy.orm import validates
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    bookings = db.relationship('Booking', back_populates='user')

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    availability = db.Column(db.Boolean)
    bookings = db.relationship('Booking', back_populates='listing')

    picture = db.Column(db.String()) 
    description = db.Column(db.Text())

    @validates('total_price')
    def validate_price(self, key, total_price):
        if total_price <= 0:  
            print('Price must be greater than 0')
            return None
        return total_price

 
class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'))
    name = db.Column(db.String)
    email = db.Column(db.String)
    checkin_date = db.Column(db.String)
    checkout_date = db.Column(db.String)
    guests = db.Column(db.Integer)
    total_price = db.Column(db.Integer)
    status = db.Column(db.String)
    listing = db.relationship('Listing', back_populates='bookings')

    user_id = db.Column(db.Integer, ForeignKey('user.id'))

    user = db.relationship('User')
    
    @validates('email')
    def validate_email(self, key, email):
        if "@" not in email:
            raise ValueError("Email must contain @")

        if "." not in email:
            raise ValueError("Email must contain .")

        if len(email) <= 3:
            raise ValueError("Invalid email length")

        return email

@validates('checkin_date')
def validate_checkin_date(self, key, checkin_date):
    today = datetime.datetime.now().date()
    if checkin_date <= today:
        print("Checkin date must be a future date")
        return None
    return checkin_date

@validates('checkout_date') 
def validate_checkout(self, key, checkout_date, checkin_date):
    if checkout_date <= checkin_date:
            print("Checkout date must be after checkin date")
            return None

    today = datetime.datetime.now().date()  
        if checkout_date <= today: 
            print("Checkout date must be a future date")
            return None

        return checkout_date
