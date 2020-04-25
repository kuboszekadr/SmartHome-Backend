import json

from flask import Blueprint, request
bp = Blueprint('data_collector', __name__)

@bp.route('/data_collector', methods=['POST'])
def data_collector():
    # make sure that only post requests are handled
    assert request.method == 'POST'

    data = request.args.get('data')
    buf = json.loads(data) # serialize json

    for b in buf:
        print(b['id'])
        print(b['value'])
        print(b['ts'])

    return "200"