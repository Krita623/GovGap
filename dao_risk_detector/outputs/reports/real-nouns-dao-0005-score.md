# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:24 UTC
**Proposal ID**: 189
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
- `0x0658f4ed17289144717713adffc2539ef7c2ef8e`
- `0x8c5effc5fb5d3805212713115427f4efe82a40be`
- `0xdd930e878bdf23a78573998a451464c5bf56eeca`

### Unaccounted Addresses
- `0xb1a32fc9f9d8b2cf86c068cae13108809547ef71`
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
- Claimed actions: treasury_operation
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
  - Unaccounted addresses: 0xb1a32fc9f9d8b2cf86c068cae13108809547ef71, 0xd9db270c1b5e3bd161e8c8503c55ceabee709552

---

## Security Conclusion

The proposal text and the observed payload effects are broadly consistent. No clear Semantic Gap was found. Reviewers should still manually review any low-risk undisclosed addresses or unknown selectors.

---

## Summary

The proposal text claims: Requesting 694.20 ETH for Gnars to scale the provision of extremely nounish public goods through action sports activations, onboarding initiatives via Prop House and That's Gnarly, and funding the Gnars treasury.
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
