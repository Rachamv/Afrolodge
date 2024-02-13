from apps import db
from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Availability(db.Model):
    """Availability model for representing the availability of listings."""
    __tablename__ = 'availability'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    available = Column(Boolean, nullable=False)
    availability_30 = Column(Integer)
    availability_60 = Column(Integer)
    availability_90 = Column(Integer)
    availability_365 = Column(Integer)
    listing_id = Column(Integer, ForeignKey('listing.id'))

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
    def validate(date, available):
        """Validate the date and availability."""
        Availability.validate_date(date)
        Availability.validate_available(available)

    @staticmethod
    def validate_date(date):
        """Validate the date format."""
        # validate_date_format(date)
        pass

    @staticmethod
    def validate_available(available):
        """Validate the availability format."""
        # validate_available_format(available)
        pass

    @classmethod
    def calculate_total_available_days(cls, listing_id, start_date, end_date):
        """Calculate the total available days within a date range."""
        cls.validate_date(start_date)
        cls.validate_date(end_date)

        total_available_days = cls.query.filter(
            Availability.listing_id == listing_id,
            Availability.date.between(start_date, end_date),
            Availability.available == True
        ).with_entities(db.func.sum(Availability.availability_30)).scalar() or 0

        return total_available_days

    @classmethod
    def find_by_date_range(cls, listing_id, start_date, end_date):
        """Find availability records within a date range."""
        cls.validate_date(start_date)
        cls.validate_date(end_date)

        return cls.query.filter(
            Availability.listing_id == listing_id,
            Availability.date.between(start_date, end_date)
        ).all()
