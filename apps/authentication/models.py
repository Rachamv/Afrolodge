import os
from flask_login import UserMixin
from apps import db
from sqlalchemy.orm import relationship
from apps.authentication.util import hash_pass
from apps.area.models import Location
from datetime import datetime
from werkzeug.utils import secure_filename

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
    profile_pic = db.Column(db.String(255))
    listings_count = db.Column(db.Integer, default=0)

    location = relationship("Location", back_populates="users")
    bookings = relationship("Booking", back_populates="user")
    listing = relationship("Listing", back_populates="user")
    reviews = relationship("Review", back_populates="reviewer")
    assets = relationship("Assets", back_populates="user")

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            if attr == "password":
                value = hash_pass(value)  # Ensure value is bytes
            setattr(self, attr, value)

    def __repr__(self):
        return f"<User {self.username}>"

    def update_password(self, new_password):
        """
        Updates the user's password.
        """
        self.password = hash_pass(new_password)

    def get_location(self):
        """
        Returns the user's location object, or None if not associated.
        """
        if self.location_id:
            return Location.query.get(self.location_id)
        return None

    def update_profile(self, **kwargs):
        """
        Updates user profile information with provided keyword arguments.

        Args:
            kwargs: Keyword arguments specifying fields to update,
                   e.g., name="New Name", phone="New Phone Number"

        Raises:
            ValueError: If invalid fields are provided.
        """
        valid_fields = [
            "name", "email", "phone", "about", "location_id", "profile_metadata_id"
        ]
        for field, value in kwargs.items():
            if field not in valid_fields:
                raise ValueError(f"Invalid field: {field}")
            setattr(self, field, value)
        db.session.commit()

    def set_profile_picture(self, picture_data):
        """
        Sets the user's profile picture from provided data.

        Args:
            picture_data: Bytes representing the image data.

        Raises:
            ValueError: If invalid picture data is provided.
        """
        # Check if picture_data is provided
        if not picture_data:
            raise ValueError("No picture data provided")

        try:
            # Create a unique filename for the profile picture
            filename = secure_filename(f"{self.username}_profile_pic.jpg")
            # Save the picture to the profile_pics directory
            file_path = os.path.join('profile_pics', filename)
            with open(file_path, 'wb') as f:
                f.write(picture_data)
            # Update the profile_pic field in the database
            self.profile_pic = filename
            db.session.commit()
            print("Profile picture set successfully")
        except Exception as e:
            print(f"Error setting profile picture: {e}")
            db.session.rollback()  # Rollback the session in case of error

    def delete_profile_picture(self):
        """
        Deletes the user's profile picture.
        """
        if self.profile_pic:
            try:
                # Assuming profile pictures are stored in a directory named 'profile_pics'
                file_path = os.path.join('profile_pics', self.profile_pic)
                os.remove(file_path)
                self.profile_pic = None
                db.session.commit()
                print("Profile picture deleted successfully")
            except Exception as e:
                print(f"Error deleting profile picture: {e}")
                db.session.rollback()
        else:
            print("User does not have a profile picture")

