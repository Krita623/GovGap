# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:24 UTC
**Proposal ID**: 173
**Simulation Status**: success
**Trace Source**: simulated_trace

---

## Consistency Score

**Overall Score**: 8/10
**Risk Level**: LOW
**Scoring Method**: worst-case risk gating, not weighted average.

Overall score uses minimum dimension score 8 capped by highest severity LOW.

---

## Conflict Detection

- Dimension score: 8/10
- Severity: LOW
- Summary: Execution includes undisclosed path components, but core business actions match proposal text.

### Addresses Disclosed In Proposal Text
- `0x5d802e2fe48392c104ce0401c7eca8a4456f1f16`
- `0x80826180a2629206e3499b5167aac8440e3f87f6`
- `0xac2671baaa44b79ca1fb006750c684e5349d721b`
- `0xdf6e59c6df1e9500fd35a76ff4c62f9901e90019`
- `0xe6232ed3436c4065d38d8bfdc8ea90858ecdfa69`
- `0xe7304ba0f157f2ade94015934284b6704bc72911`
- `0xf8a065f287d91d77cd626af38ffa220d9b552a2b`

### Unaccounted Addresses
- `0x0bc3807ec262cb779b38d65b38158acc3bfede10`
  - Risk level: LOW
  - Related actions: transfer
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xd9db270c1b5e3bd161e8c8503c55ceabee709552`
  - Risk level: LOW
  - Related actions: delegatecall
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.

### Key Findings
- Unaccounted trace addresses
  - Risk level: LOW
  - Description: One or more addresses appeared in the trace without direct proposal text disclosure.
  - Evidence source: trace

---

## Depth Analysis

- Claimed complexity: simple
- Actual max depth: 1
- Depth mismatch: no
- Delegatecall count: 1

Summary: Core business actions match proposal text; observed wrapper depth is within a normal review range.

---

## Function Semantic Match

- Dimension score: 9/10
- Severity: LOW
- Summary: Claimed business actions match; extra execution wrappers are present but do not create a business-action mismatch.
- Claimed actions: transfer
- Actual actions: transfer

---

## Potential Risk Findings

### 1. LOW - Unaccounted trace addresses

- **Severity**: LOW
- **Description**: One or more addresses appeared in the trace without direct proposal text disclosure.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review undisclosed execution path components, but prioritize whether the core business action remains covered by proposal text.
- **Key Evidence**:
  - Unaccounted addresses: 0x0bc3807ec262cb779b38d65b38158acc3bfede10, 0xd9db270c1b5e3bd161e8c8503c55ceabee709552

---

## Security Conclusion

The proposal text and the observed payload effects are broadly consistent. No clear Semantic Gap was found. Reviewers should still manually review any low-risk undisclosed addresses or unknown selectors.

---

## Summary

The proposal text claims: Fund a Nouns-branded sailing event during NFT.NYC 2023, featuring a fleet of J/24 sailboats in New York Harbor, interactive community building, and post-event meetups.
The payload actually shows: transfer. Decoded functions include: unable to confirm.
The most important scoring issue is `conflict_detection`, which scored 8/10.
No HIGH or CRITICAL finding was generated. Unknown or unclear fields should still be manually reviewed.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
