import json

from flask import Blueprint, request
from model import db, StgLogs

bp = Blueprint('logs', __name__)


@bp.route("/api/logs", methods=["POST"])
def save_logs():
    """
    #TODO
    """
    if not request.is_json:
        return "Expected JSON in request", 400

    data = request.get_json()

    try:
        entry = StgLogs(**data)
    except TypeError:
        return 'Wrong data schema', 400

    db.session.add(entry)
    db.session.commit()

    return 'OK', 200
