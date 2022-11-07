from model import db


class Reading(db.Model):
    __tablename__ = 'reading'
    __table_args__ = {'schema': 'stg'}

    sensor_name = db.Column(db.String(32))
    device_name = db.Column(db.String(32))
    device_ip = db.Column(db.String(32))
    measure_name = db.Column(db.String(32))

    reading_value = db.Column(db.Numeric(), primary_key=True)
    measure_name = db.Column(db.String(32), primary_key=True)
    reading_timestamp = db.Column(db.DateTime(timezone=True), primary_key=True)


class Log(db.Model):
    __tablename__ = 'log'
    __table_args__ = {'schema': 'stg'}

    device_name = db.Column(db.String(32))
    module_name = db.Column(db.String(32))

    log_level = db.Column(db.String(32))
    msg = db.Column(db.String(255), primary_key=True)
    log_timestamp = db.Column(db.DateTime(), primary_key=True)

