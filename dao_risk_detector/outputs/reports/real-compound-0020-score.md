# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:24 UTC
**Proposal ID**: 506
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
- `0x0507aaa21c678976fcdc7e804836acd6ebc17a44`
  - Risk level: LOW
  - Related actions: isFeatureEnabled(bytes32), resourceConfig()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x49048044d57e1c92a77f79988d21fa8faf74e97e`
  - Risk level: LOW
  - Related actions: depositTransaction(address,uint256,uint64,bool,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x6d903f6003cca6255d85cca4d3b5e5146dc33925`
  - Risk level: LOW
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x73a79fab69143498ed3712e519a88a918e1f4072`
  - Risk level: LOW
  - Related actions: isFeatureEnabled(bytes32), resourceConfig()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x866e82a600a1414e583f7f13623f1ac5d58b0afa`
  - Risk level: LOW
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x8efb6b5c4767b09dc9aa6af4eaa89f749522bae2`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x97cebbf8959e2a5476fbe9b98a21806ec234609b`
  - Risk level: LOW
  - Related actions: depositTransaction(address,uint256,uint64,bool,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xb686f13aff1e427a1f993f29ab0f2e7383729fe0`
  - Risk level: LOW
  - Related actions: sendMessage(address,bytes,uint32)
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
- Actual max depth: 5
- Depth mismatch: no
- Delegatecall count: 5

Summary: Observed trace depth is consistent with the claimed complexity.

---

## Function Semantic Match

- Dimension score: 9/10
- Severity: LOW
- Summary: Claimed business actions match; extra execution wrappers are present but do not create a business-action mismatch.
- Claimed actions: parameter_update, bridge
- Actual actions: bridge, parameter_update

### Matched Functions
- `depositTransaction(address,uint256,uint64,bool,bytes)`
- `getAddress(string)`
- `isFeatureEnabled(bytes32)`
- `resourceConfig()`
- `sendMessage(address,bytes,uint32)`

---

## Potential Risk Findings

### 1. LOW - Unaccounted trace addresses

- **Severity**: LOW
- **Description**: One or more addresses appeared in the trace without direct proposal text disclosure.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review undisclosed execution path components, but prioritize whether the core business action remains covered by proposal text.
- **Key Evidence**:
  - Unaccounted addresses: 0x0507aaa21c678976fcdc7e804836acd6ebc17a44, 0x49048044d57e1c92a77f79988d21fa8faf74e97e, 0x6d903f6003cca6255d85cca4d3b5e5146dc33925, 0x73a79fab69143498ed3712e519a88a918e1f4072, 0x866e82a600a1414e583f7f13623f1ac5d58b0afa, 0x8efb6b5c4767b09dc9aa6af4eaa89f749522bae2, 0x97cebbf8959e2a5476fbe9b98a21806ec234609b, 0xb686f13aff1e427a1f993f29ab0f2e7383729fe0

---

## Security Conclusion

The proposal text and the observed payload effects are broadly consistent. No clear Semantic Gap was found. Reviewers should still manually review any low-risk undisclosed addresses or unknown selectors.

---

## Summary

The proposal text claims: Add wsuperOETHb as collateral into the cUSDCv3 market on Base.
The payload actually shows: bridge, parameter_update. Decoded functions include: depositTransaction(address,uint256,uint64,bool,bytes), getAddress(string), isFeatureEnabled(bytes32), resourceConfig(), sendMessage(address,bytes,uint32).
The most important scoring issue is `conflict_detection`, which scored 8/10.
No HIGH or CRITICAL finding was generated. Unknown or unclear fields should still be manually reviewed.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
