import time

from flask import Blueprint, request, Flask, jsonify
from flask_cors import cross_origin

bp = Blueprint("date", __name__)


@bp.route("/api/date", methods=["GET"])
@cross_origin()
def date():
    format = request.args.get("format")
    
    if format:
        results = time.strftime(format)
    else:
        results = int(time.time())

    return jsonify(date=results)