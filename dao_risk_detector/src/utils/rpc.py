from __future__ import annotations

import os
from collections.abc import Sequence
from urllib.parse import urlparse

import requests


def rpc_call(rpc_url: str, method: str, params: Sequence[object]) -> object:
    request = requests.Session()
    if should_bypass_proxy(rpc_url):
        request.trust_env = False
    response = request.post(
        rpc_url,
        json={"jsonrpc": "2.0", "id": 1, "method": method, "params": list(params)},
        timeout=_rpc_timeout_seconds(),
    )
    if not response.ok:
        raise RuntimeError(f"{response.status_code} {response.text[:500]}")
    body = response.json()
    if "error" in body:
        raise RuntimeError(body["error"])
    return body.get("result")


def _rpc_timeout_seconds() -> int:
    try:
        return int(os.getenv("RPC_TIMEOUT_SECONDS", "120"))
    except ValueError:
        return 120


def should_bypass_proxy(rpc_url: str) -> bool:
    host = urlparse(rpc_url).hostname
    if host in {"localhost", "127.0.0.1", "::1"}:
        return True
    if host is None:
        return False
    parts = host.split(".")
    if len(parts) != 4 or not all(part.isdigit() for part in parts):
        return False
    first, second = int(parts[0]), int(parts[1])
    return (
        first == 10
        or (first == 172 and 16 <= second <= 31)
        or (first == 192 and second == 168)
    )
