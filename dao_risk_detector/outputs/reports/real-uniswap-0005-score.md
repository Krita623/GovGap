# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:24 UTC
**Proposal ID**: 26
**Simulation Status**: reverted_with_trace
**Trace Source**: simulated_trace

---

## Consistency Score

**Overall Score**: 6/10
**Risk Level**: MEDIUM
**Scoring Method**: worst-case risk gating, not weighted average.

Overall score uses minimum dimension score 7 capped by highest severity MEDIUM.

---

## Conflict Detection

- Dimension score: 7/10
- Severity: MEDIUM
- Summary: Trace includes undisclosed addresses without evidence of an uncovered sensitive business action.

### Addresses Disclosed In Proposal Text
- `0x1a9c8182c09f50c8318d769245bea52c32be35bc`
- `0x1f98431c8ad98523631ae4a59f267346ea31f984`
- `0x2bad8182c09f50c8318d769245bea52c32be46cd`
- `0x41653c7d61609d856f29355e404f310ec4142cfb`

### Unaccounted Addresses
- `0x408ed6354d4973f66138c91495f2f2fcbd8724c3`
  - Risk level: MEDIUM
  - Related actions: delegatecall
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x53a328f4086d7c0f1fa19e594c9b842125263026`
  - Risk level: MEDIUM
  - Related actions: delegatecall
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.

### Key Findings
- Unaccounted trace addresses
  - Risk level: MEDIUM
  - Description: One or more addresses appeared in the trace without direct proposal text disclosure.
  - Evidence source: trace

---

## Depth Analysis

- Claimed complexity: moderate
- Actual max depth: 1
- Depth mismatch: no
- Delegatecall count: 1

Summary: Core business actions match proposal text; observed wrapper depth is within a normal review range.

---

## Function Semantic Match

- Dimension score: 9/10
- Severity: LOW
- Summary: Claimed business actions match; extra execution wrappers are present but do not create a business-action mismatch.
- Claimed actions: bridge, role_change, bridge
- Actual actions: unable to confirm

---

## Potential Risk Findings

### 1. MEDIUM - Unaccounted trace addresses

- **Severity**: MEDIUM
- **Description**: One or more addresses appeared in the trace without direct proposal text disclosure.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review undisclosed execution path components, but prioritize whether the core business action remains covered by proposal text.
- **Key Evidence**:
  - Unaccounted addresses: 0x408ed6354d4973f66138c91495f2f2fcbd8724c3, 0x53a328f4086d7c0f1fa19e594c9b842125263026

---

## Security Conclusion

The proposal has some disclosure gaps or incomplete semantic coverage. Reviewers should verify the relevant addresses, functions, and call paths before voting or execution.

---

## Summary

The proposal text claims: This proposal aims to fix the cross-chain governance bridge for Uniswap on Arbitrum. It involves temporarily disabling address-aliasing for the L1 Timelock, calling setOwner on the L2 Uniswap Factory to set the owner to the properly aliased L1 Timelock address, and then re-enabling aliasing.
The payload actually shows: unable to confirm. Decoded functions include: unable to confirm.
The most important scoring issue is `conflict_detection`, which scored 7/10.
No HIGH or CRITICAL finding was generated. Unknown or unclear fields should still be manually reviewed.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
