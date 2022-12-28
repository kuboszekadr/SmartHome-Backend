from model import db


class Reading(db.Model):
    __tablename__ = 'reading'
    __table_args__ = {'schema': 'stg'}

    reading_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    sensor_name = db.Column(db.String(32))
    device_name = db.Column(db.String(32))
    measure_name = db.Column(db.String(32))

    reading_value = db.Column(db.Numeric())
    measure_name = db.Column(db.String(32))
    reading_timestamp = db.Column(db.DateTime(timezone=True))

