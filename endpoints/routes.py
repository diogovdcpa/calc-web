from datetime import datetime
from uuid import uuid4

from flask import Blueprint, jsonify, request


api_bp = Blueprint("api", __name__)


_DEFAULT_ADMIN_ASSETS = [
    {
        "id": "6f3df0b4-9e19-4f4e-808f-7b3a4c5bb0f6",
        "nome": "skyhigh_webgateway",
        "eventsize1": 446,
        "eventsize2": 637,
        "eventsize3": 3189,
        "logs_por_dia": 5071546,
        "created_at": "2024-01-05T10:00:00Z",
    },
    {
        "id": "7c2f4e8f-6786-4b1c-bd36-6d5cbd7c24d1",
        "nome": "mcafee_epo",
        "eventsize1": 1389,
        "eventsize2": 1446,
        "eventsize3": 1452,
        "logs_por_dia": 27476,
        "created_at": "2024-01-05T10:00:00Z",
    },
]
_DEFAULT_USER_ASSETS = [
    {
        "id": "0f15d2f2-7318-4e44-9c53-829f3a0d2c07",
        "nome": "skyhigh_webgateway",
        "usuarios": 3.4,
        "created_at": "2024-01-05T10:00:00Z",
    }
]
_ADMIN_ASSETS = []
_USER_ASSETS = []


def _timestamp():
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def _new_id():
    return str(uuid4())


def reset_storage():
    _ADMIN_ASSETS.clear()
    _USER_ASSETS.clear()
    _ADMIN_ASSETS.extend([asset.copy() for asset in _DEFAULT_ADMIN_ASSETS])
    _USER_ASSETS.extend([asset.copy() for asset in _DEFAULT_USER_ASSETS])


reset_storage()


def _parse_admin_asset_payload(payload):
    if not isinstance(payload, dict):
        return None, "Payload invalido."

    required_fields = [
        "nome",
        "eventsize1",
        "eventsize2",
        "eventsize3",
        "logs_por_dia",
    ]
    parsed = {}

    for field in required_fields:
        if field not in payload:
            return None, f"Campo obrigatorio: {field}."

        value = payload[field]
        if field == "nome":
            if not isinstance(value, str) or not value.strip():
                return None, "Nome do ativo obrigatorio."
            parsed[field] = value.strip()
            continue

        try:
            number = float(value)
        except (TypeError, ValueError):
            return None, f"Campo {field} deve ser numerico."
        if number < 0:
            return None, f"Campo {field} deve ser >= 0."
        parsed[field] = number

    return parsed, None


def _parse_user_asset_payload(payload):
    if not isinstance(payload, dict):
        return None, "Payload invalido."

    required_fields = ["nome", "usuarios"]
    parsed = {}

    for field in required_fields:
        if field not in payload:
            return None, f"Campo obrigatorio: {field}."

        value = payload[field]
        if field == "nome":
            if not isinstance(value, str) or not value.strip():
                return None, "Nome do ativo obrigatorio."
            parsed[field] = value.strip()
            continue

        try:
            number = float(value)
        except (TypeError, ValueError):
            return None, f"Campo {field} deve ser numerico."
        if number < 0:
            return None, f"Campo {field} deve ser >= 0."
        parsed[field] = number

    return parsed, None


@api_bp.get("/api/admin-assets")
def list_admin_assets():
    return jsonify(
        {
            "timestamp": _timestamp(),
            "data": _ADMIN_ASSETS,
            "total": len(_ADMIN_ASSETS),
        }
    )


@api_bp.post("/api/admin-assets")
def create_admin_asset():
    payload, error = _parse_admin_asset_payload(request.get_json(silent=True))
    if error:
        return jsonify({"error": error, "timestamp": _timestamp()}), 400

    asset = {"id": _new_id(), **payload, "created_at": _timestamp()}
    _ADMIN_ASSETS.append(asset)

    return jsonify({"data": asset, "timestamp": _timestamp()}), 201


@api_bp.put("/api/admin-assets/<string:asset_id>")
def update_admin_asset(asset_id: str):
    payload, error = _parse_admin_asset_payload(request.get_json(silent=True))
    if error:
        return jsonify({"error": error, "timestamp": _timestamp()}), 400

    for idx, asset in enumerate(_ADMIN_ASSETS):
        if asset["id"] == asset_id:
            _ADMIN_ASSETS[idx] = {
                "id": asset_id,
                **payload,
                "created_at": asset.get("created_at", _timestamp()),
            }
            return jsonify({"data": _ADMIN_ASSETS[idx], "timestamp": _timestamp()})

    return jsonify({"error": "Ativo nao encontrado.", "timestamp": _timestamp()}), 404


@api_bp.delete("/api/admin-assets/<string:asset_id>")
def delete_admin_asset(asset_id: str):
    for idx, asset in enumerate(_ADMIN_ASSETS):
        if asset["id"] == asset_id:
            removed = _ADMIN_ASSETS.pop(idx)
            return jsonify({"data": removed, "timestamp": _timestamp()})

    return jsonify({"error": "Ativo nao encontrado.", "timestamp": _timestamp()}), 404


@api_bp.get("/api/user-assets")
def list_user_assets():
    return jsonify(
        {
            "timestamp": _timestamp(),
            "data": _USER_ASSETS,
            "total": len(_USER_ASSETS),
        }
    )


@api_bp.post("/api/user-assets")
def create_user_asset():
    payload, error = _parse_user_asset_payload(request.get_json(silent=True))
    if error:
        return jsonify({"error": error, "timestamp": _timestamp()}), 400

    asset = {"id": _new_id(), **payload, "created_at": _timestamp()}
    _USER_ASSETS.append(asset)

    return jsonify({"data": asset, "timestamp": _timestamp()}), 201


@api_bp.put("/api/user-assets/<string:asset_id>")
def update_user_asset(asset_id: str):
    payload, error = _parse_user_asset_payload(request.get_json(silent=True))
    if error:
        return jsonify({"error": error, "timestamp": _timestamp()}), 400

    for idx, asset in enumerate(_USER_ASSETS):
        if asset["id"] == asset_id:
            _USER_ASSETS[idx] = {
                "id": asset_id,
                **payload,
                "created_at": asset.get("created_at", _timestamp()),
            }
            return jsonify({"data": _USER_ASSETS[idx], "timestamp": _timestamp()})

    return jsonify({"error": "Ativo nao encontrado.", "timestamp": _timestamp()}), 404


@api_bp.delete("/api/user-assets/<string:asset_id>")
def delete_user_asset(asset_id: str):
    for idx, asset in enumerate(_USER_ASSETS):
        if asset["id"] == asset_id:
            removed = _USER_ASSETS.pop(idx)
            return jsonify({"data": removed, "timestamp": _timestamp()})

    return jsonify({"error": "Ativo nao encontrado.", "timestamp": _timestamp()}), 404
