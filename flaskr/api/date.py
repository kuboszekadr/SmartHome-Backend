import datetime

from flask import Blueprint, request, Flask
from flask_cors import cross_origin

bp = Blueprint("date", __name__)


@bp.route("/api/date", methods=["GET"])
@cross_origin()
def date():
    dt = datetime.datetime.now()
    return dt.strftime("%Y%m%d %H%M%S")
