from flask import Blueprint, jsonify, request
from model import db
from model.public.tables import Reading

from sqlalchemy import select, and_
from sqlalchemy.orm import aliased

from datetime import datetime, timedelta

bp = Blueprint('get_readings', __name__)

r = aliased(Reading)

@bp.route('/api/v1.0/readings', methods=['GET'])
def get_readings():
    request_json = request.get_json()
    device_name = request_json['device_name']
    
    cutoff = datetime.now() - timedelta(hours=24)
    query = select([
        r.sensor_name,
        r.device_name,
        r.measure_name,

        r.reading_value,
        r.reading_timestamp
    ]).where(
        and_(
            r.device_name == device_name,
            r.reading_timestamp >= cutoff
            )
    )

    data = db.session.execute(query).fetchall()
    results = [
            {
                'sensor_name': row[0],
                'device_name': row[1],
                'measure_name': row[2],
                'reading_value': float(row[3]),
                'reading_timestamp': row[4].isoformat()
            }
            for row in data
        ]
    
    return jsonify(results)