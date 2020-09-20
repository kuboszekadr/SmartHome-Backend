import json

from flask import Blueprint, request, Flask
from flask_cors import cross_origin

from model import db, FrondEndReading
from itertools import groupby

bp = Blueprint("api", __name__)


@bp.route("/api", methods=["GET"])
@cross_origin()
def api():
    assert request.method == "GET"

    # Get readings data
    readings = FrondEndReading.query.with_entities(
        FrondEndReading.sensor_id,
        FrondEndReading.measure_id,
        FrondEndReading.reading_value,
        FrondEndReading.reading_timestamp_label
    ).order_by(
        FrondEndReading.measure_id,
        FrondEndReading.sensor_id,
        FrondEndReading.reading_timestamp_label.desc()  # !!! sorting is curtial!!!
    ).all()

    # Convert readings into list of dict
    readings = [dict(zip(r._real_fields, r)) for r in readings]
    labels = set([r['reading_timestamp_label'] for r in readings])

    # Groupby to front-end format
    # measure - sensor
    readings_iter = groupby(readings, lambda x: x['measure_id'])

    # Add second level - sensor
    readings_data = {}  # dict of key, sensor readings (output)
    for measure, rs in readings_iter:
        sensors = groupby(list(rs), lambda x: x['sensor_id'])

        # Generate sensors data
        sensors_data = {}
        for sensor, r in sensors:
            # Generate readings data and convert decima() to float
            readings_value = map(lambda x: x['reading_value'], r)
            readings_value = map(lambda x: float(x) if x else x, list(readings_value))

            # add sensor data to the measure
            sensors_data[sensor] = list(readings_value)

        # add measure data to the result set
        readings_data[measure] = sensors_data

    labels = sorted(labels)
    labels = list(map(lambda x: x[-5:], labels))
    
    result = {'readings': readings_data, 'labels': labels}
    return json.dumps(result)
