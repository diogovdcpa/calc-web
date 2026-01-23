from endpoints import routes


def test_parse_admin_asset_payload_valid():
    payload = {
        "nome": "teste",
        "eventsize1": 1,
        "eventsize2": 2,
        "eventsize3": 3,
        "logs_por_dia": 4,
    }
    parsed, error = routes._parse_admin_asset_payload(payload)
    assert error is None
    assert parsed["nome"] == "teste"
    assert parsed["eventsize1"] == 1


def test_parse_admin_asset_payload_invalid_name():
    parsed, error = routes._parse_admin_asset_payload({"nome": " ", "eventsize1": 1, "eventsize2": 1, "eventsize3": 1, "logs_por_dia": 1})
    assert parsed is None
    assert error == "Nome do ativo obrigatorio."


def test_parse_admin_asset_payload_negative_value():
    parsed, error = routes._parse_admin_asset_payload(
        {
            "nome": "ativo",
            "eventsize1": -1,
            "eventsize2": 1,
            "eventsize3": 1,
            "logs_por_dia": 1,
        }
    )
    assert parsed is None
    assert error == "Campo eventsize1 deve ser >= 0."


def test_parse_user_asset_payload_valid():
    payload = {"nome": "ativo", "usuarios": 2}
    parsed, error = routes._parse_user_asset_payload(payload)
    assert error is None
    assert parsed["usuarios"] == 2


def test_parse_user_asset_payload_invalid_name():
    parsed, error = routes._parse_user_asset_payload({"nome": "", "usuarios": 1})
    assert parsed is None
    assert error == "Nome do ativo obrigatorio."


def test_parse_user_asset_payload_negative_value():
    parsed, error = routes._parse_user_asset_payload({"nome": "ativo", "usuarios": -1})
    assert parsed is None
    assert error == "Campo usuarios deve ser >= 0."
