from app import app


def test_health_check():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_message_endpoint():
    response = app.test_client().get("/api/message")
    assert response.status_code == 200
    assert response.json["message"]


def test_home_page():
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert b"CI/CD demo" in response.data
