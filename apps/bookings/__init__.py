from flask import Blueprint

blueprint = Blueprint(
    'booking_blueprint',
    __name__,
    url_prefix='/booking'
)