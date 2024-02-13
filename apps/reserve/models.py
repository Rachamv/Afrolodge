from apps import db
from sqlalchemy import Column, Integer, DateTime, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from apps.leases.models import Listing
from apps.authentication.models import Users
from datetime import datetime

class Booking(db.Model):
    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listing.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    checkin_date = Column(DateTime, nullable=False)
    checkout_date = Column(DateTime, nullable=False)
    num_guests = Column(Integer, nullable=False)
    total_price = Column(Float)
    status = Column(String, nullable=False, default="Pending")

    listing = relationship("Listing", back_populates="bookings")
    user = relationship("Users", back_populates="bookings")


    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error saving to the database: {e}")

    def calculate_total_price(self):
        if self.listing:
            self.total_price = self.listing.calculate_total_price(
                str(self.checkin_date), str(self.checkout_date), self.num_guests)
        else:
            raise ValueError("Booking must be associated with a valid listing")

    def update_status(self, new_status):
        if new_status not in ["Pending", "Confirmed", "Cancelled"]:
            raise ValueError("Invalid booking status")
        self.status = new_status

    def confirm_booking(self):
        if self.status == "Pending":
            self.update_status("Confirmed")
        else:
            raise ValueError("Booking cannot be confirmed in its current state.")

    def cancel_booking(self):
        if self.status == "Pending":
            self.update_status("Cancelled")
        else:
            raise ValueError("Booking cannot be cancelled in its current state.")

    @classmethod
    def find_bookings_by_date_range(cls, start_date, end_date):
        start_datetime = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")
        return cls.query.filter(cls.checkin_date >= start_datetime, cls.checkout_date <= end_datetime).all()

    @classmethod
    def find_bookings_by_status(cls, status):
        if status not in ["Pending", "Confirmed", "Cancelled"]:
            raise ValueError("Invalid booking status")
        return cls.query.filter_by(status=status).all()
