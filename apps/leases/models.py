from apps import db
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from apps.authentication.models import Users

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
    location_id = Column(Integer, ForeignKey('location.id'))
    name = Column(String(255))
    summary = Column(String(255))
    description = Column(String(1000))
    experiences_offered = Column(String(255))
    neighborhood_overview = Column(String(1000))
    notes = Column(String(1000))
    transit = Column(String(255))
    access = Column(String(255))
    interaction = Column(String(255))
    house_rules = Column(String(1000))
    picture_url = Column(String(255))
    currency = Column(String(3))
    price = Column(Float)
    daily_price = Column(Float)
    weekly_price = Column(Float)
    monthly_price = Column(Float)
    security_deposit = Column(Float)
    cleaning_fee = Column(Float)
    instant_bookable = Column(Boolean)
    overall_satisfaction = Column(Float)

    assets = relationship("Assets", backref="listing")
    location = relationship("Location", backref="listing")
    asset_metadata = relationship("AssetsMetadata", backref="listing", uselist=False)

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


# Assets Metadata model
class AssetsMetadata(BaseModel):
    __tablename__ = 'assets_metadata'

    id = Column(Integer, primary_key=True)
    license = Column(String)
    cancellation_policy = Column(String)
    require_guest_profile_picture = Column(Boolean)
    require_guest_phone_verification = Column(Boolean)
    listing_id = Column(Integer, ForeignKey("listing.id"))
    user_id = Column(Integer, ForeignKey("Users.id"))

    user = relationship("Users", backref="assets_metadata")
    additional_fields = relationship("AdditionalField", backref="assets_metadata")

    def associate_listing(self, listing):
        if not isinstance(listing, Listing):
            raise ValueError("Invalid Listing object")
        self.listing = listing

    def associate_user(self, user):
        if not isinstance(user, Users):
            raise ValueError("Invalid User object")
        self.user = user


# Additional Field model
class AdditionalField(BaseModel):
    __tablename__ = 'additional_field'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(String)
    assets_metadata_id = Column(Integer, ForeignKey("assets_metadata.id"))
