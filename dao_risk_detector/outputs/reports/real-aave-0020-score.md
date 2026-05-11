# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:23 UTC
**Proposal ID**: 321
**Simulation Status**: reverted_with_trace
**Trace Source**: simulated_trace

---

## Consistency Score

**Overall Score**: 2/10
**Risk Level**: CRITICAL
**Scoring Method**: worst-case risk gating, not weighted average.

Overall score uses minimum dimension score 2 capped by highest severity CRITICAL.

Some dimensions may be acceptable, but the overall score is limited by High or Critical rule-engine findings.

---

## Conflict Detection

- Dimension score: 2/10
- Severity: CRITICAL
- Summary: An undisclosed address participates in an uncovered critical business action.

### Addresses Disclosed In Proposal Text
- `0x0568a3aeb8e78262deff75ee68fac20ae35ffa91`
- `0x0cb2535d00cddfae5ed1aff2e5a0239fc947d17d`
- `0x32f3a6134590fc2d9440663d35a2f0a6265f04c4`
- `0xf7c3350757de224bdb2b77a3943c8667acee3d37`

### Unaccounted Addresses
- `0x158a6bc04f0828318821bae797f50b0a1299d45b`
  - Risk level: CRITICAL
  - Related actions: sendMessageToChild(address,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x229047fed2591dbec1ef1118d64f7af3db9eb290`
  - Risk level: CRITICAL
  - Related actions: isFeatureEnabled(bytes32), resourceConfig()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x25ace71c97b33cc4729cf772ae268934f7ab5fa1`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x28e4f3a7f651294b9564800b2d01f35189a5bfbe`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x4dbd4fc535ac27206064b68ffcf827b0a60bab3f`
  - Risk level: CRITICAL
  - Related actions: calculateRetryableSubmissionFee(uint256,uint256), unsafeCreateRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x5e4e65926ba27467555eb562121fac00d24e9dd2`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x5f5c02875a8e9b5a26fbd09040abcfdeb2aa6711`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x7c058ad1d0ee415f7e7f30e62db1bcf568470a10`
  - Risk level: CRITICAL
  - Related actions: calculateRetryableSubmissionFee(uint256,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x97cebbf8959e2a5476fbe9b98a21806ec234609b`
  - Risk level: CRITICAL
  - Related actions: depositTransaction(address,uint256,uint64,bool,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xb686f13aff1e427a1f993f29ab0f2e7383729fe0`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xbeb5fc579115071764c7423a4f12edde41f106ed`
  - Risk level: CRITICAL
  - Related actions: depositTransaction(address,uint256,uint64,bool,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xd1b3e25fd7c8ae7caddc6f71b461b79cd4ddcfa3`
  - Risk level: CRITICAL
  - Related actions: unsafeCreateRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xd392c27b84b1ca776528f2704bc67b82a62132d2`
  - Risk level: CRITICAL
  - Related actions: isFeatureEnabled(bytes32), resourceConfig()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xde1fcfb0851916ca5101820a69b13a4e276bd81f`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xec568fffba86c094cf06b22134b23074dfe2252c`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xfe5e5d361b2ad62c541bab87c45a0b9b018389a2`
  - Risk level: CRITICAL
  - Related actions: sendMessageToChild(address,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.

### Key Findings
- Unaccounted trace addresses
  - Risk level: CRITICAL
  - Description: One or more addresses appeared in the trace without direct proposal text disclosure.
  - Evidence source: trace

---

## Depth Analysis

- Claimed complexity: simple
- Actual max depth: 6
- Depth mismatch: yes
- Delegatecall count: 6

Summary: Observed trace depth exceeds claimed complexity.

### Key Findings
- Trace complexity exceeds textual complexity disclosure
  - Risk level: HIGH
  - Description: Observed trace depth exceeds claimed complexity.
  - Evidence source: trace

---

## Function Semantic Match

- Dimension score: 2/10
- Severity: CRITICAL
- Summary: Text claims a low-risk action while the trace includes a sensitive business action.
- Claimed actions: parameter_update
- Actual actions: bridge, parameter_update, transfer

### Matched Functions
- `calculateRetryableSubmissionFee(uint256,uint256)`
- `depositTransaction(address,uint256,uint64,bool,bytes)`
- `enqueueL2GasPrepaid()`
- `execute(address)`
- `getAddress(string)`
- `isFeatureEnabled(bytes32)`
- `resourceConfig()`
- `sendMessage(address,bytes,uint32)`
- `sendMessageToChild(address,bytes)`
- `syncState(address,bytes)`
- `unsafeCreateRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes)`

### Unmatched Or Additional Actions
- `bridge`
  - Risk level: CRITICAL
  - Note: this action was not fully matched to the claimed proposal action. Review the linked evidence before relying on the proposal text.
- `transfer`
  - Risk level: CRITICAL
  - Note: this action was not fully matched to the claimed proposal action. Review the linked evidence before relying on the proposal text.

### Key Findings
- Claimed actions do not fully match trace actions
  - Risk level: CRITICAL
  - Description: Text claims a low-risk action while the trace includes a sensitive business action.
  - Evidence source: rule_engine

---

## Potential Risk Findings

### 1. CRITICAL - Unaccounted trace addresses

- **Severity**: CRITICAL
- **Description**: One or more addresses appeared in the trace without direct proposal text disclosure.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Pause or escalate manual review because an uncovered critical business action is linked to an undisclosed address.
- **Key Evidence**:
  - Unaccounted addresses: 0x158a6bc04f0828318821bae797f50b0a1299d45b, 0x229047fed2591dbec1ef1118d64f7af3db9eb290, 0x25ace71c97b33cc4729cf772ae268934f7ab5fa1, 0x28e4f3a7f651294b9564800b2d01f35189a5bfbe, 0x4dbd4fc535ac27206064b68ffcf827b0a60bab3f, 0x5e4e65926ba27467555eb562121fac00d24e9dd2, 0x5f5c02875a8e9b5a26fbd09040abcfdeb2aa6711, 0x7c058ad1d0ee415f7e7f30e62db1bcf568470a10, 0x97cebbf8959e2a5476fbe9b98a21806ec234609b, 0xb686f13aff1e427a1f993f29ab0f2e7383729fe0, 0xbeb5fc579115071764c7423a4f12edde41f106ed, 0xd1b3e25fd7c8ae7caddc6f71b461b79cd4ddcfa3, 0xd392c27b84b1ca776528f2704bc67b82a62132d2, 0xde1fcfb0851916ca5101820a69b13a4e276bd81f, 0xec568fffba86c094cf06b22134b23074dfe2252c, 0xfe5e5d361b2ad62c541bab87c45a0b9b018389a2

### 2. HIGH - Trace complexity exceeds textual complexity disclosure

- **Severity**: HIGH
- **Description**: Observed trace depth exceeds claimed complexity.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review whether the proposal text should describe the actual call depth or indirect execution paths.
- **Key Evidence**:
  - Complexity: claimed=simple, actual_max_depth=6

### 3. CRITICAL - Claimed actions do not fully match trace actions

- **Severity**: CRITICAL
- **Description**: Text claims a low-risk action while the trace includes a sensitive business action.
- **Evidence Source**: rule_engine
- **Confidence**: 0.9
- **Recommendation**: Compare proposal action wording with decoded functions and risk actions before relying on the text.
- **Key Evidence**:
  - Action comparison: claimed=parameter_update, actual=unable to confirm

---

## Security Conclusion

The proposal has a critical Semantic Gap or potential attack indicators. The textual commitment and observed on-chain behavior are severely inconsistent. Do not execute without immediate manual security review.

---

## Summary

The proposal text claims: Gauntlet recommends setting the isolated debt ceiling to 0 for MAI/MIMATIC on Arbitrum, Optimism, Avalanche, and Polygon v3 to strengthen protection against risky borrowing.
The payload actually shows: bridge, parameter_update, transfer. Decoded functions include: calculateRetryableSubmissionFee(uint256,uint256), depositTransaction(address,uint256,uint64,bool,bytes), enqueueL2GasPrepaid(), execute(address), getAddress(string), isFeatureEnabled(bytes32), resourceConfig(), sendMessage(address,bytes,uint32), sendMessageToChild(address,bytes), syncState(address,bytes), unsafeCreateRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes).
The most important scoring issue is `conflict_detection`, which scored 2/10.
High-risk findings include: Unaccounted trace addresses, Trace complexity exceeds textual complexity disclosure, Claimed actions do not fully match trace actions. Pausing or escalating to manual audit is recommended.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
