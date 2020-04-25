import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    from . import get_date
    from . import data_collector

    app.register_blueprint(get_date.bp)
    app.register_blueprint(data_collector.bp)

    return app


