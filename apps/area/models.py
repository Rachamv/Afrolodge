from apps import db

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
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    is_location_exact = db.Column(db.Boolean)

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

    def validate_coordinates(self):
        if self.latitude is not None and not (-90 <= self.latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")

        if self.longitude is not None and not (-180 <= self.longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")
