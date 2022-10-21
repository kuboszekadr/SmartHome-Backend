import json
import pytest
import time

from flaskr import create_app


@pytest.fixture
def client():
    app = create_app({'TESTING': True})

    with app.test_client() as client:
        yield client


def test_date_epoch(client):
    r = client.get("/api/date")
    data = json.loads(r.data)

    ts = int(time.time())
    assert ts - data["date"] <= 10


def test_date_format(client):
    format = "%m/%d/%Y, %H:%M:%S"
    r = client.get(
        "/api/date",
        query_string={'format': format}
    )
    data = json.loads(r.data)

    ts = time.strftime(format)
    assert ts == data["date"]
