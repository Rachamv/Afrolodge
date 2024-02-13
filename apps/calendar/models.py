from apps import db
from sqlalchemy import Column, Integer, Date, ForeignKey, Float, Time, Text
from sqlalchemy.orm import relationship
from apps.authentication.models import Users
from apps.leases.models import Listing

class Calendar(db.Model):

    __tablename__ = 'calendar'

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listing.id'), nullable=False)
    date = Column(Date, nullable=False)
    booked_by_user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    number_of_guests = Column(Integer)
    total_price = Column(Float)
    check_in_time = Column(Time)
    check_out_time = Column(Time)
    booking_status = Column(Text)

    user = relationship("Users", back_populates="bookings")
    listing = relationship("Listing", back_populates="calendar_bookings")


    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error saving to the database: {e}")

    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error updating calendar: {e}")

    @classmethod
    def check_availability(cls, listing_id, date):
        return cls.query.filter_by(listing_id=listing_id, date=date).first() is None

    @classmethod
    def get_booking_status(cls, listing_id, date):
        calendar_entry = cls.query.filter_by(listing_id=listing_id, date=date).first()
        return calendar_entry.booking_status if calendar_entry else None

    def calculate_total_price(self):
        if self.listing:
            return self.listing.total_price
        return None
