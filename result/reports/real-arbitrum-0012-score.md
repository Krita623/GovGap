# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:23 UTC
**Proposal ID**: 112325874093084064493910714319140234408317576120604499542718372361020687891105
**Simulation Status**: reverted_with_trace
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
- Summary: Trace includes undisclosed execution path components without extracted risk actions.

### Addresses Disclosed In Proposal Text
- `0x4fd1216c8b5e72b22785169ae5c1e8f3b30c19e4`
- `0x7796f378b3c56ced57350b938561d8c52256456b`

### Unaccounted Addresses
- `0x0000000000000000000000000000000000000064`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x34d45e99f7d8c45ed05b5ca72d54bbd1fb3f98f0`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.

### Key Findings
- Unaccounted trace addresses
  - Risk level: LOW
  - Description: One or more addresses appeared in the trace without direct proposal text disclosure.
  - Evidence source: trace

---

## Depth Analysis

- Claimed complexity: moderate
- Actual max depth: 0
- Depth mismatch: no
- Delegatecall count: 0

Summary: Core business actions match proposal text; observed wrapper depth is within a normal review range.

---

## Function Semantic Match

- Dimension score: 10/10
- Severity: LOW
- Summary: No deterministic business action was extracted from the trace.
- Claimed actions: treasury_operation, treasury_operation
- Actual actions: unable to confirm

### Matched Functions
- `sendTxToL1(address,bytes)`

---

## Potential Risk Findings

### 1. LOW - Unaccounted trace addresses

- **Severity**: LOW
- **Description**: One or more addresses appeared in the trace without direct proposal text disclosure.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review undisclosed execution path components, but prioritize whether the core business action remains covered by proposal text.
- **Key Evidence**:
  - Unaccounted addresses: 0x0000000000000000000000000000000000000064, 0x34d45e99f7d8c45ed05b5ca72d54bbd1fb3f98f0

---

## Security Conclusion

The proposal text and the observed payload effects are broadly consistent. No clear Semantic Gap was found. Reviewers should still manually review any low-risk undisclosed addresses or unknown selectors.

---

## Summary

The proposal text claims: This proposal transfers the proposer and canceller roles from the current Arbitrum Core Governor and Arbitrum Treasury Governor to newly deployed Governor contracts to upgrade the governance infrastructure.
The payload actually shows: unable to confirm. Decoded functions include: sendTxToL1(address,bytes).
The most important scoring issue is `conflict_detection`, which scored 8/10.
No HIGH or CRITICAL finding was generated. Unknown or unclear fields should still be manually reviewed.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
