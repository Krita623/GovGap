# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:24 UTC
**Proposal ID**: 332
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

### Unaccounted Addresses
- `0x0bc3807ec262cb779b38d65b38158acc3bfede10`
  - Risk level: LOW
  - Related actions: submit(address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x17144556fd3424edc8fc8a4c940b2d04936d17eb`
  - Risk level: LOW
  - Related actions: submit(address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x2b33cf282f867a7ff693a66e11b0fcc5552e4425`
  - Risk level: LOW
  - Related actions: getApp(bytes32,bytes32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xae7ab96520de3a18e5e111b5eaab095312d7fe84`
  - Risk level: LOW
  - Related actions: submit(address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xb8ffc3cd6e7cf5a098a1c92f48009765b24088dc`
  - Risk level: LOW
  - Related actions: getApp(bytes32,bytes32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.

### Key Findings
- Unaccounted trace addresses
  - Risk level: LOW
  - Description: One or more addresses appeared in the trace without direct proposal text disclosure.
  - Evidence source: trace

---

## Depth Analysis

- Claimed complexity: unable to confirm
- Actual max depth: 2
- Depth mismatch: no
- Delegatecall count: 2

Summary: Core business actions match proposal text; observed wrapper depth is within a normal review range.

---

## Function Semantic Match

- Dimension score: 9/10
- Severity: LOW
- Summary: Claimed business actions match; extra execution wrappers are present but do not create a business-action mismatch.
- Claimed actions: treasury_operation
- Actual actions: transfer

### Matched Functions
- `getApp(bytes32,bytes32)`
- `submit(address)`

---

## Potential Risk Findings

### 1. LOW - Unaccounted trace addresses

- **Severity**: LOW
- **Description**: One or more addresses appeared in the trace without direct proposal text disclosure.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review undisclosed execution path components, but prioritize whether the core business action remains covered by proposal text.
- **Key Evidence**:
  - Unaccounted addresses: 0x0bc3807ec262cb779b38d65b38158acc3bfede10, 0x17144556fd3424edc8fc8a4c940b2d04936d17eb, 0x2b33cf282f867a7ff693a66e11b0fcc5552e4425, 0xae7ab96520de3a18e5e111b5eaab095312d7fe84, 0xb8ffc3cd6e7cf5a098a1c92f48009765b24088dc

---

## Security Conclusion

The proposal text and the observed payload effects are broadly consistent. No clear Semantic Gap was found. Reviewers should still manually review any low-risk undisclosed addresses or unknown selectors.

---

## Summary

The proposal text claims: Proposal to stake an additional 10000 ETH to Lido.
The payload actually shows: transfer. Decoded functions include: getApp(bytes32,bytes32), submit(address).
The most important scoring issue is `conflict_detection`, which scored 8/10.
No HIGH or CRITICAL finding was generated. Unknown or unclear fields should still be manually reviewed.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
