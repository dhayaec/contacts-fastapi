def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


def test_register(client):
    r = client.post("/api/v1/auth/register", json={
        "email": "new@user.com", "password": "newpass123", "full_name": "New"
    })
    assert r.status_code == 201
    data = r.json()
    assert data["email"] == "new@user.com"
    assert "id" in data


def test_login_success(client):
    client.post("/api/v1/auth/register", json={
        "email": "login@test.com", "password": "loginpass", "full_name": "L"
    })
    r = client.post("/api/v1/auth/login", json={
        "email": "login@test.com", "password": "loginpass", "full_name": "L"
    })
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_bad_password(client):
    client.post("/api/v1/auth/register", json={
        "email": "bad@test.com", "password": "goodpass", "full_name": "B"
    })
    r = client.post("/api/v1/auth/login", json={
        "email": "bad@test.com", "password": "badpasswor", "full_name": "B"
    })
    assert r.status_code == 401


def test_refresh_token(client):
    reg = client.post("/api/v1/auth/register", json={
        "email": "refresh@test.com", "password": "refreshpass", "full_name": "R"
    })
    login = client.post("/api/v1/auth/login", json={
        "email": "refresh@test.com", "password": "refreshpass", "full_name": "R"
    })
    refresh_token = login.json()["refresh_token"]
    r = client.post("/api/v1/auth/refresh", params={"refresh_token": refresh_token})
    assert r.status_code == 200
    assert "access_token" in r.json()
