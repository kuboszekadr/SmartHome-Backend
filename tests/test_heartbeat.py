import pytest
import json

from dotenv import load_dotenv
from flaskr import create_app, db

from model.public.tables import Device


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


def test_hearbeat(client):
    data = {'device_name': 'Test'}

    r = client.post("/api/v1.0/heartbeat",
                    data=json.dumps(data),
                    content_type='application/json')

    assert r.status_code == 200

    session = db.session.execute("select * from device")
    state: tuple = session.fetchone()

    assert state[1] == 'Test'
    assert state[3] is not None

    assert db.session.query(Device.device_id).count() == 1

    r = client.post("/api/v1.0/heartbeat",
                    data=json.dumps(data),
                    content_type='application/json')

    assert r.status_code == 200