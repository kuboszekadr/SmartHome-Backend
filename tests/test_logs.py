import pytest
import json

from datetime import datetime
from dotenv import load_dotenv
from flaskr import create_app, db

from model import StgLog


@pytest.fixture
def client():
    load_dotenv('.env-tests')

    app = create_app({'TESTING': True})

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            db.session.commit()

        yield client


def test_logs(client):
    tests = load_test_sets()
    for test in tests:
        data, expected_status_code, expected_db_count = test.values()

        r = client.post("/api/logs",
                        data=json.dumps(data),
                        content_type='application/json')
        assert r.status_code == expected_status_code
        assert db.session.query(StgLog.device_id).count() == expected_db_count


def load_test_sets():
    with open("./tests/test_sets/logs.json") as f:
        data = json.load(f)

    return data
