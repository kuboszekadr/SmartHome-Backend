from flask import Blueprint, request

from model import db
from model.public.tables import Device

bp = Blueprint('heartbeat', __name__)


@bp.route("/api/v1.0/heartbeat", methods=["POST"])
def save_logs():
    """
    #TODO
    """
    if not request.is_json:
        return "Expected JSON in request", 400

    data = request.get_json()
    data['device_ip'] = request.remote_addr

    try:
        entry = Device(**data)
    except TypeError:
        return 'Wrong data schema', 400

    db.session.add(entry)
    db.session.commit()

    return 'OK', 200
