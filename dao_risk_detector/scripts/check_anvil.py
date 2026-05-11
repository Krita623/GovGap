from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv

from src.utils.rpc import rpc_call


def main() -> None:
    parser = argparse.ArgumentParser(description="Check whether Anvil RPC is reachable and reset-capable.")
    parser.add_argument("--url", default=None, help="Anvil RPC URL. Defaults to ANVIL_RPC_URL or localhost:8545.")
    args = parser.parse_args()

    load_dotenv()
    import os

    url = args.url or os.getenv("ANVIL_RPC_URL") or "http://127.0.0.1:8545"
    result: dict[str, object] = {
        "anvil_rpc_url": url,
        "reachable": False,
        "client_version": None,
        "chain_id": None,
        "block_number": None,
        "looks_like_anvil": False,
        "supports_anvil_reset": None,
        "error": None,
    }

    try:
        result["chain_id"] = rpc_call(url, "eth_chainId", [])
        result["client_version"] = rpc_call(url, "web3_clientVersion", [])
        result["block_number"] = rpc_call(url, "eth_blockNumber", [])
        result["reachable"] = True
    except Exception as exc:
        result["error"] = f"RPC unavailable: {type(exc).__name__}: {exc}"
        print(json.dumps(result, indent=2, ensure_ascii=False))
        raise SystemExit(1)

    client_version = str(result["client_version"] or "").lower()
    result["looks_like_anvil"] = "anvil" in client_version
    result["supports_anvil_reset"] = result["looks_like_anvil"]
    if not result["looks_like_anvil"]:
        result["error"] = "RPC reachable but client version does not look like Anvil."
        print(json.dumps(result, indent=2, ensure_ascii=False))
        raise SystemExit(2)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
