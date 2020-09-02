import json

from flask import Blueprint, request
from model import db, Reading, ProgramRuntime

bp = Blueprint("data_collector", __name__)


@bp.route("/data_collector", methods=["POST"])
def data_collector():
    
    # define class message parsers
    message_class_parser = {
        0: stage_sensor_readings,
        1: stage_program_execution
    }

    # make sure that only post requests are handled
    assert request.method == "POST"

    # Parse json request (sent as form)
    data_raw = request.form["data"]
    data = json.loads(data_raw)
    device_id = data["device_id"]

    # loop through all available messages
    for d in data["data"]:
        message_class_parser[d['c']](d, device_id)

    db.session.commit()  # commit the latest changes

    return "200"


def stage_sensor_readings(sensor_data: dict, device_id: int):
    sensor_id = sensor_data['id']
    timestamp = sensor_data['t']

    values = sensor_data['r']  # one sensor can return multiple measure (for example DHT22)
    for value in values:
        measure_id = value['m']
        value = value['v']

        # prepare new row
        reading = Reading(sensor_id=sensor_id,
                          device_id=device_id,
                          reading_value=value,
                          reading_measure=measure_id,
                          reading_timestamp=timestamp
                          )

        db.session.add(reading) # stage new program entry


def stage_program_execution(program: dict, device_id: int):
    program_id = program['id']
    execution_id = program['e']  # execution_id is hold for potencial debugging purposes
    
    is_active = program['a']
    step = program['s']
    timestamp = program['t']

    # prepare new row
    program = ProgramRuntime(program_id=program_id,
                             is_active=is_active,
                             step=step,

                             execution_timestamp=timestamp,
                             execution_id=execution_id
                             )

    db.session.add(program)  # stage new program entry

# TODO:
# def stage_event(event: dict, device_id: int)