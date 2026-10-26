
from fastapi.testclient import TestClient

from src.api_contract_sentinel.api import app


client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_compare_endpoint_detects_removed_response_field():
    old_spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Test API",
            "version": "1.0.0",
        },
        "paths": {
            "/users": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Success",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "integer"},
                                            "email": {"type": "string"},
                                        },
                                    }
                                }
                            },
                        }
                    }
                }
            }
        },
    }

    new_spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Test API",
            "version": "2.0.0",
        },
        "paths": {
            "/users": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Success",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "integer"},
                                        },
                                    }
                                }
                            },
                        }
                    }
                }
            }
        },
    }

    response = client.post(
        "/compare",
        json={
            "old_spec": old_spec,
            "new_spec": new_spec,
        },
    )

    assert response.status_code == 200

    report = response.json()

    assert report["old_version"] == "1.0.0"
    assert report["new_version"] == "2.0.0"
    assert report["total_changes"] == 1
    assert report["changes"][0]["field"] == "email"
    assert report["changes"][0]["severity"] == "Breaking"


def test_compare_endpoint_rejects_invalid_request():
    response = client.post(
        "/compare",
        json={
            "old_spec": "not-a-valid-specification",
            "new_spec": {},
        },
    )

    assert response.status_code == 422

