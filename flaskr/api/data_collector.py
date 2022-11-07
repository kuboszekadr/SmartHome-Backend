import json

from flask import Blueprint, request
from model import db
from model.stg.tables import Reading

bp = Blueprint('api_data_collector', __name__)


@bp.route("/api/v2.0/data_collector", methods=["POST"])
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
    r = json.loads(request)

    readings = r['reading']
    for reading in readings:
        stage_sensor_reading(
            reading,
            r['device_name'],
            r['sensor_name']
        )

    db.session.commit()
    return '200'


def stage_sensor_reading(reading: dict, device_name: str, sensor_name: str):
    """
    Creates new row to be added into readings table

    @param sensor_data: data obtained from the device sensor
    @param device_id: device sending the data
    """

    r = Reading(
        sensor_name=sensor_name,
        device_name=device_name,

        reading_value=reading['value'],
        measure_id=reading['measure_id'],
        reading_timestamp=reading['timestamp']
    )
    db.session.add(r)
