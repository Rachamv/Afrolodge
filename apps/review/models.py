from apps import db
from sqlalchemy import Column, Integer, DateTime, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    reviewer_id = Column(Integer, ForeignKey('Users.id'))
    rating = Column(Float)
    comments = Column(Text)

    reviewer = relationship("Users", back_populates="reviews")

    def __init__(self, date=None, reviewer_id=None, rating=None, comments=None):
        self.date = date or datetime.utcnow()
        self.reviewer_id = reviewer_id
        self.rating = rating
        self.comments = comments

    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error saving to the database: {e}")

    def associate_user(self, user):
        from apps.authentication.models import Users
        if not isinstance(user, Users):
            raise ValueError("Invalid User object")
        self.reviewer = user

    def update(self):
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error updating review: {e}")

    @classmethod
    def fetch_reviews_by_reviewer(cls, reviewer_id):
        return cls.query.filter_by(reviewer_id=reviewer_id).all()

    @classmethod
    def calculate_average_rating_for_listing(cls, listing_id):
        ratings = [review.rating for review in cls.query.filter_by(listing_id=listing_id).all() if review.rating is not None]

        if not ratings:
            return None

        total_rating = sum(ratings)
        return total_rating / len(ratings)
