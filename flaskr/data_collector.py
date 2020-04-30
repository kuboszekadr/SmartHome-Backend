import json

from flask import Blueprint, request
from model import db, Reading

bp = Blueprint('data_collector', __name__)


@bp.route('/data_collector', methods=['POST'])
def data_collector():
    # make sure that only post requests are handled
    assert request.method == 'POST'

    data = request.form['data']
    sensors_data = json.loads(data)  # serialize json

    # stage sensor data
    for sensor_data in sensors_data:
        add_sensor_data_to_session(sensor_data)
    db.session.commit()

    return "200"


def add_sensor_data_to_session(sensor_data):
    sensor_id = sensor_data['sensor_id']
    timestamp = sensor_data['ts']
    values = sensor_data['reading']

    for value in values:
        measure_id = value['measure_id']
        value = value['value']

        reading = Reading(sensor_id=sensor_id,
                          reading_value=value,
                          reading_measure=measure_id,
                          reading_timestamp=timestamp
                          )
        db.session.add(reading)
