from model import db


class Reading(db.Model):
    __tablename__ = 'reading'

    reading_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    sensor_name = db.Column(db.String(32))
    device_name = db.Column(db.String(32))
    device_ip = db.Column(db.String(32))
    measure_name = db.Column(db.String(32))

    reading_value = db.Column(db.Numeric())
    measure_name = db.Column(db.String(32))
    reading_timestamp = db.Column(db.DateTime(timezone=True))


class Log(db.Model):
    __tablename__ = 'log'

    log_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    
    device_name = db.Column(db.String(32))
    module_name = db.Column(db.String(32))

    log_level = db.Column(db.String(32))
    msg = db.Column(db.String(255))
    log_timestamp = db.Column(db.DateTime())

