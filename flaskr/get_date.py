import datetime

from flask import Blueprint
bp = Blueprint('get_date', __name__)

@bp.route('/get_date')
def get_date():
    dt = datetime.datetime.now()
    return  dt.strftime("%Y%m%d %H%M%S")