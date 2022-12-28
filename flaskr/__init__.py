import os
from flask import Flask
from model import db    


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    from .api import date, data_collector, logs, solar_panel_value, heartbeat
    from .notifier import notifier

    app.register_blueprint(data_collector.bp)
    app.register_blueprint(date.bp)
    
    app.register_blueprint(logs.bp)
    app.register_blueprint(notifier.bp)
    app.register_blueprint(solar_panel_value.bp)
    app.register_blueprint(heartbeat.bp)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{pwd}@{ip}:{port}/{db}'.format(
        user=os.environ['DBUSER'],
        pwd=os.environ['DBPWD'],
        ip=os.environ['DBIP'],
        port=os.environ['DBPORT'],
        db=os.environ['DB']
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    return app
