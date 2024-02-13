from flask import Blueprint

blueprint = Blueprint(
    'assets_blueprint',
    __name__,
    url_prefix='/assets'
)