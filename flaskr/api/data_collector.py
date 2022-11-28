import json

from flask import Blueprint, request
from model import db
from flask import jsonify
from model.stg.tables import Reading

bp = Blueprint('api_data_collector', __name__)


@bp.route("/api/data_collector", methods=["POST"])
def data_collector():
    """
    Endpoint for data collection from multiple sensors

    Expected data format:
    {
        "device_name": "device_name",
        "sensor_name": "sensor_name",
        "readings": [
            {"measure_name":"measure_name", 
             "value":22.22,
             "timestamp":"20200513 063312"
            }
        ]
    }
    """
    r: dict = request.get_json()

    readings = r['readings']
    for reading in readings:
        stage_sensor_reading(
            reading,
            r['device_name'],
            r.get('sensor_name'),
            request.remote_addr
        )

    try:
        db.session.commit()
    except Exception as e:
        return jsonify(status='Error', msg=str(e)), 500
    else:
        return jsonify(status='OK'), 200

def stage_sensor_reading(reading: dict, device_name: str, sensor_name: str, device_ip: str):
    """
    Creates new row to be added into readings table

    @param sensor_data: data obtained from the device sensor
    @param device_id: device sending the data
    """

    r = Reading(
        sensor_name=sensor_name,
        device_name=device_name,
        device_ip=device_ip,

        reading_value=reading['value'],
        measure_name=reading['measure_name'],
        reading_timestamp=reading['timestamp']
    )
    db.session.add(r)
