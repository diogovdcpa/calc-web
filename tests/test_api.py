def test_admin_crud(client):
    list_resp = client.get("/api/admin-assets")
    assert list_resp.status_code == 200
    data = list_resp.get_json()
    assert isinstance(data["data"], list)

    payload = {
        "nome": "novo_admin",
        "eventsize1": 10,
        "eventsize2": 20,
        "eventsize3": 30,
        "logs_por_dia": 40,
    }
    create_resp = client.post("/api/admin-assets", json=payload)
    assert create_resp.status_code == 201
    created = create_resp.get_json()["data"]
    assert isinstance(created["id"], str)
    assert "created_at" in created

    update_resp = client.put(f"/api/admin-assets/{created['id']}", json=payload)
    assert update_resp.status_code == 200
    updated = update_resp.get_json()["data"]
    assert updated["id"] == created["id"]

    delete_resp = client.delete(f"/api/admin-assets/{created['id']}")
    assert delete_resp.status_code == 200


def test_user_crud(client):
    list_resp = client.get("/api/user-assets")
    assert list_resp.status_code == 200
    data = list_resp.get_json()
    assert isinstance(data["data"], list)

    payload = {"nome": "novo_user", "usuarios": 5}
    create_resp = client.post("/api/user-assets", json=payload)
    assert create_resp.status_code == 201
    created = create_resp.get_json()["data"]
    assert isinstance(created["id"], str)
    assert "created_at" in created

    update_resp = client.put(f"/api/user-assets/{created['id']}", json=payload)
    assert update_resp.status_code == 200
    updated = update_resp.get_json()["data"]
    assert updated["id"] == created["id"]

    delete_resp = client.delete(f"/api/user-assets/{created['id']}")
    assert delete_resp.status_code == 200


def test_admin_invalid_payload(client):
    resp = client.post("/api/admin-assets", json={"nome": ""})
    assert resp.status_code == 400
    payload = resp.get_json()
    assert payload["error"] == "Nome do ativo obrigatorio."


def test_user_invalid_payload(client):
    resp = client.post("/api/user-assets", json={"nome": "ativo", "usuarios": -1})
    assert resp.status_code == 400
    payload = resp.get_json()
    assert payload["error"] == "Campo usuarios deve ser >= 0."
