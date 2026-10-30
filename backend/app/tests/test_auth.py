def test_user_registration_and_login(client):
    # Register
    reg_payload = {
        "full_name": "Advocate Priya Sharma",
        "email": "priya.sharma@example.com",
        "password": "SecurePassword999!",
    }
    reg_resp = client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_resp.status_code == 201
    reg_data = reg_resp.json()
    assert "access_token" in reg_data
    assert reg_data["user"]["email"] == "priya.sharma@example.com"

    # Duplicate registration should fail
    dup_resp = client.post("/api/v1/auth/register", json=reg_payload)
    assert dup_resp.status_code == 400

    # Successful Login
    login_resp = client.post("/api/v1/auth/login", json={
        "email": "priya.sharma@example.com",
        "password": "SecurePassword999!",
    })
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    # Invalid Password Login
    bad_login = client.post("/api/v1/auth/login", json={
        "email": "priya.sharma@example.com",
        "password": "WrongPassword",
    })
    assert bad_login.status_code == 401

    # Protected Me endpoint
    me_resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == "priya.sharma@example.com"


def test_unauthorized_access(client):
    resp = client.get("/api/v1/cases")
    assert resp.status_code == 401

