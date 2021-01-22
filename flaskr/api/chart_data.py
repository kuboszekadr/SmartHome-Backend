import json

from flask import Blueprint, request, Flask
from flask_cors import cross_origin

from model import db, FrondEndReading, DeviceSensor, Measure
from itertools import groupby

bp = Blueprint("chart_data", __name__)


@bp.route("/api/chart_data", methods=["GET"])
@cross_origin()
def chart_data():
    assert request.method == "GET"

    result = get_readings()
    result["measures"] = get_measures()
    result["sensors"] = get_sensors()

    return result


def get_readings():

    # Get readings data
    readings = FrondEndReading.query.with_entities(
        FrondEndReading.sensor_id,
        FrondEndReading.measure_id,
        FrondEndReading.reading_value,
        FrondEndReading.reading_timestamp_label
    ).order_by(
        FrondEndReading.measure_id,
        FrondEndReading.sensor_id,
        FrondEndReading.reading_timestamp_label.asc()  # !!! sorting is curtial!!!
    ).all()

    # Convert readings into list of dict with column names
    readings = [dict(zip(r._real_fields, r)) for r in readings]

    # Groupby to front-end format
    # measure - sensor
    readings_iter = groupby(readings, lambda x: x["measure_id"])

    # Add second level - sensor
    readings_data = {}  # dict of key, sensor readings (output)
    for measure, rs in readings_iter:
        sensors = groupby(list(rs), lambda x: x["sensor_id"])

        # Generate sensors data
        sensors_data = {}
        for sensor, r in sensors:
            # Generate readings data and convert decima() to float
            readings_value = map(lambda x: x["reading_value"], r)
            readings_value = map(lambda x:
                                 float(x) if x else x, list(readings_value))

            # add sensor data to the measure
            sensors_data[sensor] = list(readings_value)

        # add measure data to the result set
        readings_data[measure] = sensors_data

    # Prepare chart labels
    labels = set([r["reading_timestamp_label"] for r in readings])
    labels = sorted(labels)
    labels = list(map(lambda x: x[-5:], labels))

    result = {
        "readings": readings_data,
        "labels": labels
    }
    return result


def get_measures():
    measures = Measure.query.with_entities(
        Measure.measure_id,
        Measure.measure_name
    ).all()
    
    # Convert measures into list of dict with column names
    measures = [dict(zip(m._real_fields, m)) for m in measures]
    result = [
        (m["measure_id"], m["measure_name"]) for m in measures
    ]

    return dict(result)


def get_sensors():
    sensors = DeviceSensor.query.with_entities(
        DeviceSensor.sensor_id,
        DeviceSensor.sensor_label,
        DeviceSensor.measure_id
    ).all()

    # Convert measures into list of dict with column names
    sensors = [dict(zip(s._real_fields, s)) for s in sensors]
    result = [
        (s["sensor_id"], {"label": s["sensor_label"],
                          "measures": s["measure_id"]})
        for s in sensors
    ]

    return dict(result)
