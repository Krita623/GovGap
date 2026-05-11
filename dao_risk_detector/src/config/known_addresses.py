"""Known address labels used for deterministic address disclosure checks."""

SYSTEM_ADDRESS_WHITELIST: dict[str, str] = {
    "0x0000000000000000000000000000000000000001": "ECRecover precompile",
    "0x0000000000000000000000000000000000000002": "SHA256 precompile",
    "0x0000000000000000000000000000000000000003": "RIPEMD160 precompile",
    "0x0000000000000000000000000000000000000004": "Identity precompile",
}

KNOWN_ADDRESSES: dict[str, str] = SYSTEM_ADDRESS_WHITELIST.copy()

# Optional deterministic address sets populated by resolver or project config.
# Empty by default so the engine does not rely on DAO-specific address special cases.
KNOWN_PROTOCOL_ADDRESSES: set[str] = set()
KNOWN_SAFE_OR_PROXY_OR_GOVERNANCE_ADDRESSES: set[str] = set()
