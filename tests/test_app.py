import math

import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


@pytest.mark.parametrize("number", [0, 1, 2, 5, 10, 20, 200])
def test_factorial(client, number):
    response = client.get(f"/factorial?number={number}")
    assert response.status_code == 200
    assert response.get_json() == {
        "number": number,
        "factorial": math.factorial(number),
    }


@pytest.mark.parametrize(
    ("query", "message"),
    [
        ("", "Query parameter 'number' is required"),
        ("?number=abc", "'number' must be an integer"),
        ("?number=3.5", "'number' must be an integer"),
        ("?number=-1", "'number' must be between 0 and 200"),
        ("?number=201", "'number' must be between 0 and 200"),
    ],
)
def test_invalid_number(client, query, message):
    response = client.get(f"/factorial{query}")
    assert response.status_code == 400
    assert response.get_json() == {"error": message}


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
