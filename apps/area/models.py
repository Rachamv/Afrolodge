from apps import db
from sqlalchemy.orm import relationship

class Location(db.Model):
    __tablename__ = "location"

    id = db.Column(db.Integer, primary_key=True)
    house_number = db.Column(db.Text)
    street = db.Column(db.Text)
    neighborhood = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.Text)
    zipcode = db.Column(db.Text)
    market = db.Column(db.Text)
    country_code = db.Column(db.Text)
    country = db.Column(db.Text)
    is_location_exact = db.Column(db.Boolean)

    users = relationship("Users", back_populates="location")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_city(cls, city):
        return cls.query.filter_by(city=city).first()

    @classmethod
    def find_by_state(cls, state):
        return cls.query.filter_by(state=state).first()

    @classmethod
    def find_by_country(cls, country):
        return cls.query.filter_by(country=country).first()

    def update(self):
        db.session.commit()
