def test_register_and_login(client):
    register_payload = {
        "full_name": "Restaurant User",
        "email": "restaurant@example.com",
        "password": "supersecure123",
        "role": "restaurant",
    }
    response = client.post("/api/v1/auth/register", json=register_payload)
    assert response.status_code == 201
    assert response.json()["email"] == "restaurant@example.com"

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "restaurant@example.com", "password": "supersecure123"},
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()