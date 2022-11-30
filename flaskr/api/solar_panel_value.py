from model import db
from flask import Blueprint, request
from model.public.queries.queries import get_solarpanel_value_stmt

bp = Blueprint('solar_panel', __name__)

@bp.route("/api/v2.0/solar_panel_value", methods=["GET"])
def get_solar_panel_value():
    """
    TODO
    """

    r: dict = request.get_json()
    window = 60

    stmt = get_solarpanel_value_stmt(window)[0]
    result = db.session.execute(stmt)

    return result