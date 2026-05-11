# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:23 UTC
**Proposal ID**: 134
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
- Summary: Execution includes undisclosed path components, but core business actions match proposal text.

### Addresses Disclosed In Proposal Text
- `0xbfda7f4ab1e146505a78e4659aec7acab39adbb0`

### Unaccounted Addresses
- `0x6d903f6003cca6255d85cca4d3b5e5146dc33925`
  - Risk level: LOW
  - Related actions: transfer(address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xc00e94cb662c3520282e6f5717214004a7f26888`
  - Risk level: LOW
  - Related actions: transfer(address,uint256)
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
- Actual max depth: 0
- Depth mismatch: no
- Delegatecall count: 0

Summary: Core business actions match proposal text; observed wrapper depth is within a normal review range.

---

## Function Semantic Match

- Dimension score: 10/10
- Severity: LOW
- Summary: Claimed business actions match extracted business actions.
- Claimed actions: transfer
- Actual actions: transfer

### Matched Functions
- `transfer(address,uint256)`

---

## Potential Risk Findings

### 1. LOW - Unaccounted trace addresses

- **Severity**: LOW
- **Description**: One or more addresses appeared in the trace without direct proposal text disclosure.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review undisclosed execution path components, but prioritize whether the core business action remains covered by proposal text.
- **Key Evidence**:
  - Unaccounted addresses: 0x6d903f6003cca6255d85cca4d3b5e5146dc33925, 0xc00e94cb662c3520282e6f5717214004a7f26888

---

## Security Conclusion

The proposal text and the observed payload effects are broadly consistent. No clear Semantic Gap was found. Reviewers should still manually review any low-risk undisclosed addresses or unknown selectors.

---

## Summary

The proposal text claims: Proposal to launch Compound Grants Program (CGP) 2.0 by Questbook, utilizing delegated domain allocation. It requests a transfer of 24,467.82 COMP to a multi-sig to fund 4 domain allocators, community grants, and operational costs over 2 quarters.
The payload actually shows: transfer. Decoded functions include: transfer(address,uint256).
The most important scoring issue is `conflict_detection`, which scored 8/10.
No HIGH or CRITICAL finding was generated. Unknown or unclear fields should still be manually reviewed.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
