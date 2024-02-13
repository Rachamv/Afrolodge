from flask import Blueprint

blueprint = Blueprint(
    'area_blueprint',
    __name__,
    url_prefix='/area'
)