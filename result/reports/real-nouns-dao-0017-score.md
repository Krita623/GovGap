# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:24 UTC
**Proposal ID**: 743
**Simulation Status**: success
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

### Unaccounted Addresses
- `0x43506849d7c04f9138d1a2050bbf3a0c054402dd`
  - Risk level: MEDIUM
  - Related actions: balanceOf(address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48`
  - Risk level: MEDIUM
  - Related actions: balanceOf(address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xb1a32fc9f9d8b2cf86c068cae13108809547ef71`
  - Risk level: MEDIUM
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xd97bcd9f47cee35c0a9ec1dc40c1269afc9e8e1d`
  - Risk level: MEDIUM
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.

### Key Findings
- Unaccounted trace addresses
  - Risk level: MEDIUM
  - Description: One or more addresses appeared in the trace without direct proposal text disclosure.
  - Evidence source: trace

---

## Depth Analysis

- Claimed complexity: simple
- Actual max depth: 2
- Depth mismatch: no
- Delegatecall count: 1

Summary: Core business actions match proposal text; observed wrapper depth is within a normal review range.

---

## Function Semantic Match

- Dimension score: 9/10
- Severity: LOW
- Summary: Claimed business actions match; extra execution wrappers are present but do not create a business-action mismatch.
- Claimed actions: transfer
- Actual actions: unable to confirm

### Matched Functions
- `balanceOf(address)`
- `sendOrRegisterDebt(address,uint256)`

---

## Potential Risk Findings

### 1. MEDIUM - Unaccounted trace addresses

- **Severity**: MEDIUM
- **Description**: One or more addresses appeared in the trace without direct proposal text disclosure.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review undisclosed execution path components, but prioritize whether the core business action remains covered by proposal text.
- **Key Evidence**:
  - Unaccounted addresses: 0x43506849d7c04f9138d1a2050bbf3a0c054402dd, 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48, 0xb1a32fc9f9d8b2cf86c068cae13108809547ef71, 0xd97bcd9f47cee35c0a9ec1dc40c1269afc9e8e1d

---

## Security Conclusion

The proposal has some disclosure gaps or incomplete semantic coverage. Reviewers should verify the relevant addresses, functions, and call paths before voting or execution.

---

## Summary

The proposal text claims: Fund the submission of the documentary 'Benbodhi: Decoded' to 48 film festivals with a requested budget of 2,854 USDC.
The payload actually shows: unable to confirm. Decoded functions include: balanceOf(address), sendOrRegisterDebt(address,uint256).
The most important scoring issue is `conflict_detection`, which scored 7/10.
No HIGH or CRITICAL finding was generated. Unknown or unclear fields should still be manually reviewed.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
