def test_create_contact(client):
    reg = client.post("/api/v1/auth/register", json={
        "email": "contact@test.com", "password": "contactpass", "full_name": "C"
    })
    login = client.post("/api/v1/auth/login", json={
        "email": "contact@test.com", "password": "contactpass"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    r = client.post("/api/v1/contacts", json={
        "first_name": "Alice", "last_name": "Smith", "email": "alice@test.com"
    }, headers=headers)
    assert r.status_code == 201
    data = r.json()
    assert data["first_name"] == "Alice"
    assert "id" in data


def test_list_contacts(client):
    reg = client.post("/api/v1/auth/register", json={
        "email": "list@test.com", "password": "listpass", "full_name": "L"
    })
    login = client.post("/api/v1/auth/login", json={
        "email": "list@test.com", "password": "listpass"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post("/api/v1/contacts", json={"first_name": "Bob"}, headers=headers)
    r = client.get("/api/v1/contacts", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) >= 1


def test_get_update_delete_contact(client):
    reg = client.post("/api/v1/auth/register", json={
        "email": "crud@test.com", "password": "crudpass", "full_name": "C"
    })
    login = client.post("/api/v1/auth/login", json={
        "email": "crud@test.com", "password": "crudpass"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create = client.post("/api/v1/contacts", json={
        "first_name": "Charlie", "email": "charlie@test.com"
    }, headers=headers)
    cid = create.json()["id"]

    r = client.get(f"/api/v1/contacts/{cid}", headers=headers)
    assert r.status_code == 200

    r = client.patch(f"/api/v1/contacts/{cid}", json={"first_name": "Chuck"}, headers=headers)
    assert r.status_code == 200
    assert r.json()["first_name"] == "Chuck"

    r = client.delete(f"/api/v1/contacts/{cid}", headers=headers)
    assert r.status_code == 204

    r = client.get(f"/api/v1/contacts/{cid}", headers=headers)
    assert r.status_code == 404
