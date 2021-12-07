import pytest
import json

from dotenv import load_dotenv
from flaskr import create_app, db

from model import StgReading


@pytest.fixture
def client():
    load_dotenv()

    app = create_app({'TESTING': True})

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            db.session.commit()

        yield client


def test_data_collector(client):
    tests = load_test_sets()
    for test in tests:
        data, expected_status_code, expected_db_count = test.values()

        r = client.post("/api/data_collector",
                        data=json.dumps(data),
                        content_type='application/json')
        assert r.status_code == expected_status_code


def load_test_sets():
    with open("./tests/test_sets/readings.json") as f:
        data = json.load(f)

    return data
