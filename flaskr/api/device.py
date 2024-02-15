from flask import Blueprint, jsonify
from model import db
from model.public.tables import Device

bp = Blueprint('device', __name__)

@bp.route('/api/v1.0/devices', methods=['GET'])
def get_devices():
    devices = (
        Device
        .query
        .order_by(Device.last_update.desc())
        .all()
    )
    records = jsonify([device.to_dict() for device in devices])
    return records
