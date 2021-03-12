import json

from flask import Blueprint, request
from model import db, Reading

bp = Blueprint('api_data_collector', __name__)


@bp.route("/api/data_collector", methods=["POST"])
def data_collector():
    """
    Endpoint for data collection from multiple sensors

    Expected data format:
    {"device_id": 1,
     "data": {
         {"sensor_id":1,
         "readings":[{"measure_id":1, "value":22.22}],
         "timestamp":"20200513 063312"
         }
     }
    }
    """
    # make sure that only post requests are handled
    assert request.method == 'POST'

    # Parse json request (sent as form)
    data_raw = request.form['data']
    data = json.loads(data_raw)
    device_id = data['device_id']

    # loop through all available messages
    for d in data['data']:
        stage_sensor_readings(d, device_id)

    db.session.commit()  # commit the latest changes

    return '200'


def stage_sensor_readings(sensor_data: dict, device_id: int):
    """
    Creates new row to be added into readings table

    @param sensor_data: data obtained from the device sensor
    @param device_id: device sending the data
    """
    sensor_id = sensor_data['sensor_id']
    timestamp = sensor_data['timestamp']

    # one sensor can return multiple measure (for example DHT22)
    for reading in sensor_data['readings']:
        measure_id = reading['measure_id']
        value = reading['value']

        # prepare new row
        r = Reading(sensor_id=sensor_id,
                    device_id=device_id,
                    reading_value=value,
                    measure_id=measure_id,
                    reading_timestamp=timestamp
                    )
        db.session.add(r)  # stage new program entry
