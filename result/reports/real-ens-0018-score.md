# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:24 UTC
**Proposal ID**: 69304512515872868228453463730257567312488838925636819022683533220991373699419
**Simulation Status**: reverted_with_trace
**Trace Source**: simulated_trace

---

## Consistency Score

**Overall Score**: 9/10
**Risk Level**: LOW
**Scoring Method**: worst-case risk gating, not weighted average.

Overall score uses minimum dimension score 9 capped by highest severity LOW.

---

## Conflict Detection

- Dimension score: 10/10
- Severity: LOW
- Summary: All trace addresses are disclosed or system-whitelisted.

### Addresses Disclosed In Proposal Text
- `0x00000000000c2e074ec69a0dfb2997ba6c7d2e1e`
- `0x2a9b5787207863cf2d63d20172ed1f7bb2c9487a`
- `0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85`
- `0x81c11034fe2b2f0561e9975df9a45d99172183af`
- `0x97df70ef350a5d2f606e0baf6d38de2ec26f7290`
- `0xfe89cc7abb2c4183683ab71653c4cdc9b02d44b7`

---

## Depth Analysis

- Claimed complexity: moderate
- Actual max depth: 1
- Depth mismatch: no
- Delegatecall count: 0

Summary: Core business actions match proposal text; observed wrapper depth is within a normal review range.

---

## Function Semantic Match

- Dimension score: 10/10
- Severity: LOW
- Summary: Claimed business actions match extracted business actions.
- Claimed actions: role_change, parameter_update, parameter_update, role_change
- Actual actions: parameter_update

### Matched Functions
- `addController(address)`
- `owner(bytes32)`
- `register(uint256,address,uint256)`
- `removeController(address)`
- `setResolver(bytes32,address)`

---

## Potential Risk Findings

No rule-engine risk findings were generated.

---

## Security Conclusion

The proposal text and the observed payload effects are broadly consistent. No clear Semantic Gap was found. Reviewers should still manually review any low-risk undisclosed addresses or unknown selectors.

---

## Summary

The proposal text claims: This proposal registers the `on.eth` ENS name to the ENS DAO wallet and sets the resolver to an on-chain registry-resolver contract (ChainResolver).
The payload actually shows: parameter_update. Decoded functions include: addController(address), owner(bytes32), register(uint256,address,uint256), removeController(address), setResolver(bytes32,address).
The most important scoring issue is `depth_analysis`, which scored 9/10.
No HIGH or CRITICAL finding was generated. Unknown or unclear fields should still be manually reviewed.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
