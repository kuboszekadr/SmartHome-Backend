import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    from . import get_date
    from . import data_collector as dc
    from .api import date, chart_data, data_collector
    from model import db

    app.register_blueprint(get_date.bp)
    app.register_blueprint(data_collector.bp)
    app.register_blueprint(dc.bp)
    app.register_blueprint(date.bp)
    app.register_blueprint(chart_data.bp)
    
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
