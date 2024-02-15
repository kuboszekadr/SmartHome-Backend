from model import db
from sqlalchemy.sql import func


class Reading(db.Model):
    __tablename__ = 'reading'

    reading_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    sensor_name = db.Column(db.String(32))
    device_name = db.Column(db.String(32))
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
    insert_timestamp = db.Column(db.DateTime(), default=func.now())


class Device(db.Model):
    __tablename__ = 'device'

    device_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    device_name = db.Column(db.String(32))
    device_ip = db.Column(db.String(32))

    last_update = db.Column(
        db.DateTime(),
        onupdate=func.now(),
        default=func.now()
    )

    def to_dict(self):
            return {
                'device_id': self.device_id,
                'device_name': self.device_name,
                'device_ip': self.device_ip,
                'last_update': self.last_update.strftime('%Y-%m-%d %H:%M:%S') if self.last_update else None
            }