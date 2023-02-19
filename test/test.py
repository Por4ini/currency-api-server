from app import app
import json
import pytest


def test_get_route():
    response = app.test_client().get('/items/UAH')
    res = json.loads(response.data.decode('utf-8')).get("items")

    assert type(res[0]) is dict
    assert response.status_code == 200


def test_push():
    pass


