import json
from urllib.parse import quote
from services.hlpr_panel_api import get_inbound_data
from configs import API_URL
from yarl import URL


def _load_json(value):
    if isinstance(value, str):
        return json.loads(value)
    return value


def _first(item, default=""):
    if isinstance(item, (list, tuple)) and item:
        return item[0]
    return default


async def build_vless_link(
    inbound_id: int | str,
    uuid: str,
    host: str | None = None
) -> str:
    """
    Получает JSON по ID inbound и строит VLESS-ссылку для клиента с нужным uuid.

    :param inbound_id: идентификатор inbound (например 3). Функция сама соберёт URL по `API_URL`.
    :param uuid: UUID клиента, по которому нужно собрать ссылку
    :param host: Хост/домен/IP для ссылки. Если не задан, берётся из сгенерированного URL.
    :return: строка вида vless://...
    """
    # Получаем объект inbound через helper в services.hlpr_panel_api
    obj = await get_inbound_data(inbound_id)

    settings = _load_json(obj.get("settings", "{}"))
    stream = _load_json(obj.get("streamSettings", "{}"))
    reality = stream.get("realitySettings", {}) or {}
    reality_settings = reality.get("settings", {}) or {}

    clients = settings.get("clients", [])
    client = next((c for c in clients if c.get("id") == uuid), None)
    if client is None:
        raise ValueError(f"Клиент с uuid={uuid} не найден в settings.clients")

    if host is None:
        host = URL(API_URL).host

    port = obj.get("port")
    remark = obj.get("remark", "")
    email = client.get("email", "")
    flow = client.get("flow", "")

    params = {
        "type": "tcp",
        "encryption": settings.get("encryption", ""),
        "path": "/",
        "headerType": "http",
        "security": "reality",
        "pbk": reality_settings.get("publicKey", ""),
        "fp": reality_settings.get("fingerprint", ""),
        "sni": _first(reality.get("serverNames", [])),
        "sid": _first(reality.get("shortIds", [])),
        "spx": reality_settings.get("spiderX", "/"),
        "pqv": reality_settings.get("mldsa65Verify", ""),
    }

    query = "&".join(
        f"{k}={quote(str(v), safe='')}"
        for k, v in params.items()
        if v not in (None, "")
    )

    fragment = f"{remark}-{email}".strip("-")
    flow_part = f"&flow={quote(flow, safe='')}" if flow else ""
    return f"vless://{uuid}@{host}:{port}?{query}{flow_part}#{quote(fragment, safe='')}"

