import json
import os

from datetime import datetime as dt
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

    file_name = get_file_name()
    file_path = f'./capture/data_collector/{file_name}'
    capute_request(r, file_path)

    readings = r['readings']
    for reading in readings:
        stage_reading(
            reading,
            r['device_name'],
            r.get('sensor_name'),
        )

    try:
        db.session.commit()
    except Exception as e:
        return jsonify(status='Error', msg=str(e)), 500
    else:
        return jsonify(status='OK'), 200

def stage_reading(reading: dict, device_name: str, sensor_name: str):
    """
    Creates new row to be added into readings table

    @param sensor_data: data obtained from the device sensor
    @param device_id: device sending the data
    """

    r = Reading(
        sensor_name=sensor_name,
        device_name=device_name,

        reading_value=reading['value'],
        measure_name=reading['measure_name'],
        reading_timestamp=reading['timestamp']
    )
    db.session.add(r)

def capute_request(r: dict, file_path: str):
    folder_name = os.path.dirname(file_path)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    with open(file_path, 'a+') as f:
        s = json.dumps(r) + '\n'
        f.write(s)

def get_file_name(ts = dt.now()) -> str:
    month = ts.strftime('%Y%m')
    date = ts.strftime('%Y%m%d')
    
    file_name = f"{month}/{date}.json"
    return file_name