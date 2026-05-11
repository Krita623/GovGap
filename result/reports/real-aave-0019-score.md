# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:23 UTC
**Proposal ID**: 390
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
- `0x945fd405773973d286de54e44649cc0d9e264f78`
- `0xc1cba3fcea344f92d9239c08c0568f6f2f0ee452`

### Unaccounted Addresses
- `0x5300a1a15135ea4dc7ad5a167152c01efc9b192a`
  - Risk level: MEDIUM
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x58bcb647c4beff253b4b6996c62f737b783f2cdd`
  - Risk level: MEDIUM
  - Related actions: forwardPayloadForExecution((uint256,uint8,address,uint40))
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x9aee0b04504cef83a65ac3f0e838d0593bcb2bc7`
  - Risk level: MEDIUM
  - Related actions: forwardPayloadForExecution((uint256,uint8,address,uint40))
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
- Actual max depth: 1
- Depth mismatch: no
- Delegatecall count: 1

Summary: Core business actions match proposal text; observed wrapper depth is within a normal review range.

---

## Function Semantic Match

- Dimension score: 9/10
- Severity: LOW
- Summary: Claimed business actions match; extra execution wrappers are present but do not create a business-action mismatch.
- Claimed actions: parameter_update
- Actual actions: unable to confirm

### Matched Functions
- `forwardPayloadForExecution((uint256,uint8,address,uint40))`

---

## Potential Risk Findings

### 1. MEDIUM - Unaccounted trace addresses

- **Severity**: MEDIUM
- **Description**: One or more addresses appeared in the trace without direct proposal text disclosure.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review undisclosed execution path components, but prioritize whether the core business action remains covered by proposal text.
- **Key Evidence**:
  - Unaccounted addresses: 0x5300a1a15135ea4dc7ad5a167152c01efc9b192a, 0x58bcb647c4beff253b4b6996c62f737b783f2cdd, 0x9aee0b04504cef83a65ac3f0e838d0593bcb2bc7

---

## Security Conclusion

The proposal has some disclosure gaps or incomplete semantic coverage. Reviewers should verify the relevant addresses, functions, and call paths before voting or execution.

---

## Summary

The proposal text claims: This proposal aims to onboard wstETH (wrapped staked ETH) from Lido to the Aave V3 Base Network, enriching the liquid staking assets options and configuring specific risk parameters.
The payload actually shows: unable to confirm. Decoded functions include: forwardPayloadForExecution((uint256,uint8,address,uint40)).
The most important scoring issue is `conflict_detection`, which scored 7/10.
No HIGH or CRITICAL finding was generated. Unknown or unclear fields should still be manually reviewed.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
