import json

from flask import Blueprint, request
from model import db, StgReading

bp = Blueprint('api_data_collector_v2.0', __name__)


@bp.route("/api/v2.0/data_collector", methods=["POST"])
def data_collector():
    """
    Endpoint for data collection from multiple sensors

    Expected data format:
    {
        "device_id": 1,
        "sensor_id": 1,
        "readings": [
            {"measure_id":1, 
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
            r['device_id'],
            r['sensor_id']
        )

    db.session.commit()
    return '200'


def stage_sensor_reading(reading: dict, device_id: int, sensor_id: int):
    """
    Creates new row to be added into readings table

    @param sensor_data: data obtained from the device sensor
    @param device_id: device sending the data
    """

    r = StgReading(
        sensor_id=sensor_id,
        device_id=device_id,

        reading_value=reading['value'],
        measure_id=reading['measure_id'],
        reading_timestamp=reading['timestamp']
    )
    db.session.add(r)
