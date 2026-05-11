# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:23 UTC
**Proposal ID**: 55434268037459750836497365958054185343730937462615166912204494229415053613423
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
- `0x912ce59144191c1204e64559fe8253a0e49e6548`

### Unaccounted Addresses
- `0x34d45e99f7d8c45ed05b5ca72d54bbd1fb3f98f0`
  - Risk level: LOW
  - Related actions: transfer(address,address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x9f43ab02cacc8e709b05936a92dc85b76d1523c4`
  - Risk level: LOW
  - Related actions: transfer(address,address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xf3fc178157fb3c87548baa86f9d24ba38e649b58`
  - Risk level: LOW
  - Related actions: transfer(address,address,uint256)
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

### Matched Functions
- `transfer(address,address,uint256)`

---

## Potential Risk Findings

### 1. LOW - Unaccounted trace addresses

- **Severity**: LOW
- **Description**: One or more addresses appeared in the trace without direct proposal text disclosure.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review undisclosed execution path components, but prioritize whether the core business action remains covered by proposal text.
- **Key Evidence**:
  - Unaccounted addresses: 0x34d45e99f7d8c45ed05b5ca72d54bbd1fb3f98f0, 0x9f43ab02cacc8e709b05936a92dc85b76d1523c4, 0xf3fc178157fb3c87548baa86f9d24ba38e649b58

---

## Security Conclusion

The proposal text and the observed payload effects are broadly consistent. No clear Semantic Gap was found. Reviewers should still manually review any low-risk undisclosed addresses or unknown selectors.

---

## Summary

The proposal text claims: This proposal establishes the Arbitrum Research & Development Collective (ARDC) for a 6-month term with a budget of 1,761,000 ARB. The ARDC will feature elected roles (DAOAdvocate, Risk, Security, Research) to review governance proposals, conduct security reviews, and provide economic risk analyses.
The payload actually shows: transfer. Decoded functions include: transfer(address,address,uint256).
The most important scoring issue is `conflict_detection`, which scored 8/10.
No HIGH or CRITICAL finding was generated. Unknown or unclear fields should still be manually reviewed.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
