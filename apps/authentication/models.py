import os
from flask_login import UserMixin
from apps import db
from sqlalchemy.orm import relationship
from apps.authentication.util import hash_pass
from apps.area.models import Location
from apps.review.models import Review
from apps.assets.models import Assets
from apps.leases.models import Booking
from apps.leases.models import Listing
from datetime import datetime
from werkzeug.utils import secure_filename
import imghdr
class Users(db.Model, UserMixin):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.LargeBinary)
    registration_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    last_login_date = db.Column(db.DateTime)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    about = db.Column(db.Text)
    response_time = db.Column(db.Float)
    profile_image = relationship("ProfileImage", uselist=False, back_populates="user")
    remember_me = db.Column(db.Boolean, default=False)
    listings_count = db.Column(db.Integer, default=0)
    assets_count = db.Column(db.Integer, default=0)
    reviews_count = db.Column(db.Integer, default=0)
    bookings_count = db.Column(db.Integer, default=0)

    bookings = relationship("Booking", back_populates="user")
    reviews = relationship("Review", back_populates="reviewer")
    assets = relationship("Assets", back_populates="user")

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            if attr == "password":
                value = hash_pass(value)
            setattr(self, attr, value)

    def __repr__(self):
        return f"<User {self.username}>"

    def update_password(self, new_password):
        self.password = hash_pass(new_password)

    def get_location(self):
        if self.location_id:
            return Location.query.get(self.location_id)
        return None

    def get_profile_picture(self):
        if self.profile_image:
            return self.profile_image.filename
        return None

    def get_reviews(self):
        return Review.query.filter_by(reviewer_id=self.id).all()

    def get_listings(self):
        return Listing.query.filter_by(user_id=self.id).all()

    def get_assets(self):
        return Assets.query.filter_by(user_id=self.id).all()

    def get_bookings(self):
        return Booking.query.filter_by(user_id=self.id).all()

    def update_profile(self, **kwargs):
        valid_fields = [
            "name", "email", "phone", "about", "location_id", "response_time", "profile_pic", "password"
        ]
        for field, value in kwargs.items():
            if field not in valid_fields:
                raise ValueError(f"Invalid field: {field}")
            setattr(self, field, value)
        db.session.commit()

    def set_profile_picture(self, picture_data):
        if not picture_data:
            raise ValueError("No picture data provided")

        try:
            filename = secure_filename(f"{self.username}_profile_pic.jpg")
            file_path = os.path.join('profile_pics', filename)
            with open(file_path, 'wb') as f:
                f.write(picture_data)
            profile_image = ProfileImage(filename=filename, user=self)
            db.session.add(profile_image)
            db.session.commit()
            print("Profile picture set successfully")
        except Exception as e:
            print(f"Error setting profile picture: {e}")
            db.session.rollback()

    def delete_profile_picture(self):
        if self.profile_image:
            try:
                file_path = os.path.join('uploads', self.profile_image.filename)
                os.remove(file_path)
                db.session.delete(self.profile_image)
                db.session.commit()
                print("Profile picture deleted successfully")
            except Exception as e:
                print(f"Error deleting profile picture: {e}")
                db.session.rollback()
        else:
            print("User does not have a profile picture")



class ProfileImage(db.Model):
    __tablename__ = 'profile_images'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user = relationship("Users", back_populates="profile_image")

    def __init__(self, filename):
        self.filename = filename

    @staticmethod
    def save_image(file, user_id):
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename)
            image_format = imghdr.what(file_path)
            if not image_format:
                raise ValueError("Invalid image format")
            file.save(file_path)
            image = ProfileImage(filename=filename, user_id=user_id)
            db.session.add(image)
            db.session.commit()
            return image
        return None
