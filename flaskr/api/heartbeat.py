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

    device = get_device(data['device_name'])
    if device is None:
        db.session.add(entry)
    else:
        setattr(entry, 'device_ip', data['device_ip'])

    db.session.commit()
    return 'OK', 200


def get_device(device_name: str):
    result = (db
              .session
              .query(Device)
              .filter(Device.device_name == device_name)
              .first()
              )
    return result
