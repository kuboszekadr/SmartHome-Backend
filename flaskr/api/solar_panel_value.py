from model import db
from flask import Blueprint, request, jsonify
from model.public.queries.queries import get_solarpanel_value_stmt

bp = Blueprint('solar_panel', __name__)
DEFAULT_WINDOW = 60

@bp.route("/api/v2.0/solar_panel_value", methods=["GET"])
def get_solar_panel_value():
    """
    TODO
    """

    r: dict = request.get_json()
    window = r.get('window', DEFAULT_WINDOW) if r else DEFAULT_WINDOW

    stmt = get_solarpanel_value_stmt(window)[0]
    query_result = db.session.execute(stmt)
    
    value = query_result.fetchone()[0]
    
    value = float(value if value else 0)
    value = round(value, 0)

    result = {
        'value': value,
        'window': window,
    }

    return jsonify(result), 200