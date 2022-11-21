import json

from flask import Blueprint, request

from model import db
from model.stg.tables import Log

bp = Blueprint('logs', __name__)


@bp.route("/api/v2.0/logs", methods=["POST"])
def save_logs():
    """
    #TODO
    """
    if not request.is_json:
        return "Expected JSON in request", 400

    data = request.get_json()

    try:
        entry = Log(**data)
    except TypeError:
        return 'Wrong data schema', 400

    db.session.add(entry)
    db.session.commit()

    return 'OK', 200
