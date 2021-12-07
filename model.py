from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql

db = SQLAlchemy()


class StgReading(db.Model):
    __tablename__ = 'reading'
    __table_args__ = {'schema': 'stg'}

    # dummy primary key here, artificial one
    sensor_id = db.Column(db.Integer(), primary_key=True)
    device_id = db.Column(db.Integer())

    reading_value = db.Column(db.Numeric())
    measure_id = db.Column(db.Integer())
    reading_timestamp = db.Column(db.DateTime())

class StgLogs(db.Model):
    __tablename__ = 'logs'
    __table_args__ = {'schema': 'stg'}

    device_id = db.Column(db.Integer(), primary_key=True)
    module_name = db.Column(db.String())
    log_level = db.Column(db.String())
    msg = db.Column(db.String())

    reading_timestamp = db.Column(db.DateTime())


class FrondEndReading(db.Model):
    __tablename__ = 'reading'
    db.Model.metadata.schema = 'front_end'

    device_id = db.Column(db.Integer(), primary_key=True)

    sensor_id = db.Column(db.Integer(), primary_key=True)
    sensor_label = db.Column(db.Integer(), primary_key=True)

    measure_id = db.Column(db.Integer(), primary_key=True)
    measure_name = db.Column(db.String())

    reading_value = db.Column(db.Numeric())
    reading_count = db.Column(db.Integer())
    reading_timestamp_label = db.Column(db.String(), primary_key=True)
