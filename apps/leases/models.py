from apps import db
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship


# Base class for shared functionality
class BaseModel(db.Model):
    __abstract__ = True

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error saving object to database: {e}")

    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Error updating object: {e}")


# Listing model
class Listing(BaseModel):
    """Listing model for representing Airbnb-like listings."""

    __tablename__ = "listing"

    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey('assets.id'))
    user_id = Column(Integer, ForeignKey('Users.id'))
    name = Column(String(255))
    summary = Column(String(255))
    description = Column(String(1000))
    listing_image = Column(String(255))
    currency = Column(String(3))
    price = Column(Float)
    instant_bookable = Column(Boolean)
    overall_satisfaction = Column(Float)
    assets = relationship("Assets", backref="listing")
    user = relationship("Users", back_populates="listing")
    availability = relationship("Availability", back_populates="listing")

    @classmethod
    def create(cls, data):
        """Creates a new Listing instance and saves it to the database."""
        listing = cls(**data)
        listing.save_to_db()
        return listing

    @classmethod
    def find_by_name(cls, name):
        """Finds a listing by its name."""
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, listing_id):
        """Finds a listing by its ID."""
        return cls.query.get(listing_id)

class Booking(BaseModel):
    """Booking model for representing bookings."""

    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listing.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    checkin_date = Column(DateTime, nullable=False)
    checkout_date = Column(DateTime, nullable=False)
    num_guests = Column(Integer, nullable=False)
    total_price = Column(Float)
    status = Column(String, nullable=False, default="Pending")

    listing = relationship("Listing", backref="bookings")
    user = relationship("Users", back_populates="bookings")


    def save_to_db(self):
        """Save the booking to the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error saving to the database: {e}")

    def calculate_total_price(self):
        """Calculate the total price."""
        if self.listing:
            self.total_price = self.listing.calculate_total_price(
                str(self.checkin_date), str(self.checkout_date), self.num_guests)
        else:
            raise ValueError("Booking must be associated with a valid listing")

    def update_status(self, new_status):
        """Update the booking status."""
        if new_status not in ["Pending", "Confirmed", "Cancelled"]:
            raise ValueError("Invalid booking status")
        self.status = new_status

    def confirm_booking(self):
        """Confirm the booking."""
        if self.status == "Pending":
            self.update_status("Confirmed")
        else:
            raise ValueError("Booking cannot be confirmed in its current state.")

    def cancel_booking(self):
        """Cancel the booking."""
        if self.status == "Pending":
            self.update_status("Cancelled")
        else:
            raise ValueError("Booking cannot be cancelled in its current state.")

    @classmethod
    def find_bookings_by_date_range(cls, start_date, end_date):
        """Find bookings within a date range."""
        start_datetime = DateTime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
        end_datetime = DateTime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")
        return cls.query.filter(cls.checkin_date >= start_datetime, cls.checkout_date <= end_datetime).all()

    @classmethod
    def find_bookings_by_status(cls, status):
        """Find bookings by status."""
        if status not in ["Pending", "Confirmed", "Cancelled"]:
            raise ValueError("Invalid booking status")
        return cls.query.filter_by(status=status).all()


class Availability(BaseModel):
    """Availability model for representing the availability of listings."""

    __tablename__ = 'availability'

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listing.id'), nullable=False)
    date = Column(Date, nullable=False)
    available = Column(Boolean, nullable=False)

    listing = relationship("Listing", back_populates="availability")

    def save_to_db(self):
        """Save the availability record to the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error saving to the database: {e}")

    def update(self):
        """Update the availability record in the database."""
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error updating availability: {e}")

    @staticmethod
    def check_availability(listing_id, date):
        """Check availability for a listing on a given date."""
        return Availability.query.filter_by(listing_id=listing_id, date=date).first() is not None

    @staticmethod
    def get_booking_status(listing_id, date):
        """Get the booking status for a listing on a given date."""
        availability_entry = Availability.query.filter_by(listing_id=listing_id, date=date).first()
        return availability_entry.available if availability_entry else None

