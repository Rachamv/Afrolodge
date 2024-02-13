from flask import Blueprint

blueprint = Blueprint(
    'leases_blueprint',
    __name__,
    url_prefix='/listing'
)