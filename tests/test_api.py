from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_health_endpoint_returns_status_and_accuracy():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["model_accuracy"] >= 0.85


def test_predict_endpoint_returns_valid_species():
    response = client.post(
        "/predict",
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
        },
    )

    assert response.status_code == 200
    assert response.json()["species"] in {"setosa", "versicolor", "virginica"}


def test_predict_endpoint_rejects_impossible_values():
    response = client.post(
        "/predict",
        json={
            "sepal_length": -1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
        },
    )

    assert response.status_code == 422
