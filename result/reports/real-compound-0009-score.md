# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:24 UTC
**Proposal ID**: 258
**Simulation Status**: success
**Trace Source**: simulated_trace

---

## Consistency Score

**Overall Score**: 4/10
**Risk Level**: HIGH
**Scoring Method**: worst-case risk gating, not weighted average.

Overall score uses minimum dimension score 5 capped by highest severity HIGH.

Some dimensions may be acceptable, but the overall score is limited by High or Critical rule-engine findings.

---

## Conflict Detection

- Dimension score: 5/10
- Severity: HIGH
- Summary: An undisclosed address participates in an uncovered approval or transfer action.

### Addresses Disclosed In Proposal Text
- `0x99c9fc46f92e8a1c0dec1b1747d010903e884be1`
- `0xf650c3d88d12db855b8bf7d11be6c55a4e07dcc9`

### Unaccounted Addresses
- `0x00000000000c2e074ec69a0dfb2997ba6c7d2e1e`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x229047fed2591dbec1ef1118d64f7af3db9eb290`
  - Risk level: HIGH
  - Related actions: resourceConfig()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x25ace71c97b33cc4729cf772ae268934f7ab5fa1`
  - Risk level: HIGH
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x3363bae2fc44da742df13cd3ee94b6bb868ea376`
  - Risk level: HIGH
  - Related actions: _reduceReserves(uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x4976fb03c32e5b8cfe2b6ccb31c09ba78ebaba41`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x543ba4aadbab8f9025686bd03993043599c6fb04`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x64b5a5ed26dcb17370ff4d33a8d503f0fbd06cff`
  - Risk level: HIGH
  - Related actions: depositERC20To(address,address,address,uint256,uint32,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x6d903f6003cca6255d85cca4d3b5e5146dc33925`
  - Risk level: HIGH
  - Related actions: approve(address,uint256), sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xbeb5fc579115071764c7423a4f12edde41f106ed`
  - Risk level: HIGH
  - Related actions: depositTransaction(address,uint256,uint64,bool,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xd3494713a5cfad3f5359379dfa074e2ac8c6fd65`
  - Risk level: HIGH
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xdac17f958d2ee523a2206206994597c13d831ec7`
  - Risk level: HIGH
  - Related actions: approve(address,uint256), transfer(address,uint256), transferFrom(address,address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xde1fcfb0851916ca5101820a69b13a4e276bd81f`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xe2f826324b2faf99e513d16d266c3f80ae87832b`
  - Risk level: HIGH
  - Related actions: depositTransaction(address,uint256,uint64,bool,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xf56d96b2535b932656d3c04ebf51babff241d886`
  - Risk level: HIGH
  - Related actions: resourceConfig()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xfb564da37b41b2f6b6edcc3e56fbf523bd9f2012`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.

### Key Findings
- Unaccounted trace addresses
  - Risk level: HIGH
  - Description: One or more addresses appeared in the trace without direct proposal text disclosure.
  - Evidence source: trace

---

## Depth Analysis

- Claimed complexity: complex
- Actual max depth: 7
- Depth mismatch: no
- Delegatecall count: 8

Summary: Observed trace depth is consistent with the claimed complexity.

---

## Function Semantic Match

- Dimension score: 7/10
- Severity: MEDIUM
- Summary: Claimed business actions partially match; extra non-critical business actions need review.
- Claimed actions: bridge, bridge, transfer, bridge, bridge, parameter_update
- Actual actions: approval, bridge, parameter_update, transfer

### Matched Functions
- `_reduceReserves(uint256)`
- `approve(address,uint256)`
- `balanceOf(address)`
- `depositERC20To(address,address,address,uint256,uint32,bytes)`
- `depositTransaction(address,uint256,uint64,bool,bytes)`
- `getAddress(string)`
- `getBorrowRate(uint256,uint256,uint256)`
- `isUpgrading()`
- `owner(bytes32)`
- `resourceConfig()`
- `sendMessage(address,bytes,uint32)`
- `setText(bytes32,string,string)`
- `supportsInterface(bytes4)`
- `transfer(address,uint256)`
- `transferFrom(address,address,uint256)`

### Unmatched Or Additional Actions
- `approval`
  - Risk level: MEDIUM
  - Note: this action was not fully matched to the claimed proposal action. Review the linked evidence before relying on the proposal text.

### Key Findings
- Claimed actions do not fully match trace actions
  - Risk level: MEDIUM
  - Description: Claimed business actions partially match; extra non-critical business actions need review.
  - Evidence source: rule_engine

---

## Potential Risk Findings

### 1. HIGH - Unaccounted trace addresses

- **Severity**: HIGH
- **Description**: One or more addresses appeared in the trace without direct proposal text disclosure.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review whether the proposal text sufficiently discloses the business action and its counterparty.
- **Key Evidence**:
  - Unaccounted addresses: 0x00000000000c2e074ec69a0dfb2997ba6c7d2e1e, 0x229047fed2591dbec1ef1118d64f7af3db9eb290, 0x25ace71c97b33cc4729cf772ae268934f7ab5fa1, 0x3363bae2fc44da742df13cd3ee94b6bb868ea376, 0x4976fb03c32e5b8cfe2b6ccb31c09ba78ebaba41, 0x543ba4aadbab8f9025686bd03993043599c6fb04, 0x64b5a5ed26dcb17370ff4d33a8d503f0fbd06cff, 0x6d903f6003cca6255d85cca4d3b5e5146dc33925, 0xbeb5fc579115071764c7423a4f12edde41f106ed, 0xd3494713a5cfad3f5359379dfa074e2ac8c6fd65, 0xdac17f958d2ee523a2206206994597c13d831ec7, 0xde1fcfb0851916ca5101820a69b13a4e276bd81f, 0xe2f826324b2faf99e513d16d266c3f80ae87832b, 0xf56d96b2535b932656d3c04ebf51babff241d886, 0xfb564da37b41b2f6b6edcc3e56fbf523bd9f2012

### 2. MEDIUM - Claimed actions do not fully match trace actions

- **Severity**: MEDIUM
- **Description**: Claimed business actions partially match; extra non-critical business actions need review.
- **Evidence Source**: rule_engine
- **Confidence**: 0.9
- **Recommendation**: Compare proposal action wording with decoded functions and risk actions before relying on the text.
- **Key Evidence**:
  - Action comparison: claimed=bridge, bridge, transfer, bridge, bridge, parameter_update, actual=unable to confirm

---

## Security Conclusion

The proposal has a serious Semantic Gap. Some on-chain actions are not sufficiently covered by the proposal text and may affect governance participants' judgment. Pausing or escalating to manual audit is recommended.

---

## Summary

The proposal text claims: Initialize a Compound III USDT market (cUSDTv3) on the Optimism network, including deployment, seeding reserves via a bridge, setting reward configurations, and updating the official markets ENS record.
The payload actually shows: approval, bridge, parameter_update, transfer. Decoded functions include: _reduceReserves(uint256), approve(address,uint256), balanceOf(address), depositERC20To(address,address,address,uint256,uint32,bytes), depositTransaction(address,uint256,uint64,bool,bytes), getAddress(string), getBorrowRate(uint256,uint256,uint256), isUpgrading(), owner(bytes32), resourceConfig(), sendMessage(address,bytes,uint32), setText(bytes32,string,string), supportsInterface(bytes4), transfer(address,uint256), transferFrom(address,address,uint256).
The most important scoring issue is `conflict_detection`, which scored 5/10.
High-risk findings include: Unaccounted trace addresses. Pausing or escalating to manual audit is recommended.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
