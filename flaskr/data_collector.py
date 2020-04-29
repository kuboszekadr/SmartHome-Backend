import json

from flask import Blueprint, request
from model import db, Reading

bp = Blueprint('data_collector', __name__)

@bp.route('/data_collector', methods=['POST'])
def data_collector():
    # make sure that only post requests are handled
    assert request.method == 'POST'

    data = request.form['data']
    buf = json.loads(data) # serialize json

    #insert data into db
    for b in buf:
        reading = Reading(sensor_id=b['id'],
            reading_value=b['value'],
            reading_measure=1, # TODO
            reading_timestamp=b['ts'])
        db.session.add(reading)
    db.session.commit()

    return "200"
