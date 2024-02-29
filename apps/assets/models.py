from apps import db
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class Assets(db.Model):
    __tablename__ = 'assets'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    assets_type = Column(String(255))
    accommodates = Column(Integer)
    bathrooms = Column(Float, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    description = Column(String(1000), nullable=False)
    amenities = Column(String)
    minimum_nights = Column(Integer)
    location_id = Column(Integer, ForeignKey('location.id'))
    reviews_id = Column(Integer, ForeignKey('review.id'))

    user = relationship("Users", back_populates="assets")
    location = relationship("Location")
    reviews = relationship("Review")

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error saving to the database: {e}")

    @classmethod
    def find_by_id(cls, assets_id):
        return cls.query.get(assets_id)

    def associate_user(self, user):
        self.user = user

    def associate_location(self, location):
        self.location = location

    def associate_reviews(self, reviews):
        self.reviews = reviews

    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error updating assets: {e}")

    @classmethod
    def search_properties(cls, location_id=None, assets_type=None, amenities=None):
        query = cls.query

        if location_id is not None:
            query = query.filter_by(location_id=location_id)

        if assets_type is not None:
            query = query.filter_by(assets_type=assets_type)

        if amenities is not None:
            query = query.filter(cls.amenities.contains(amenities))

        return query.all()

    def get_average_rating(self):
        if not self.reviews:
            return None

        total_rating = sum(review.rating for review in self.reviews)
        return total_rating / len(self.reviews)

    def get_specific_reviews(self, count=5):
        return self.reviews[:count]
