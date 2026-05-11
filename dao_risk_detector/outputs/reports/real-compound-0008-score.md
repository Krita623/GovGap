# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:24 UTC
**Proposal ID**: 238
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
- `0xbd3fa81b58ba92a82136038b25adec7066af3155`

### Unaccounted Addresses
- `0x00000000000c2e074ec69a0dfb2997ba6c7d2e1e`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x0a992d191deec32afe36203ad87d7d289a738f81`
  - Risk level: HIGH
  - Related actions: addressToBytes32(address), sendMessage(uint32,bytes32,bytes)
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
- `0x2d778797049fe9259d947d1ed8e5442226dfb589`
  - Risk level: HIGH
  - Related actions: depositTransaction(address,uint256,uint64,bool,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x43506849d7c04f9138d1a2050bbf3a0c054402dd`
  - Risk level: HIGH
  - Related actions: approve(address,uint256), burn(uint256), transferFrom(address,address,uint256)
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
- `0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48`
  - Risk level: HIGH
  - Related actions: approve(address,uint256), burn(uint256), transferFrom(address,address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xb2f38107a18f8599331677c14374fd3a952fb2c8`
  - Risk level: HIGH
  - Related actions: addressToBytes32(address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xba2492e52f45651b60b8b38d4ea5e2390c64ffb1`
  - Risk level: HIGH
  - Related actions: resourceConfig()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xbeb5fc579115071764c7423a4f12edde41f106ed`
  - Risk level: HIGH
  - Related actions: depositTransaction(address,uint256,uint64,bool,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xc00e94cb662c3520282e6f5717214004a7f26888`
  - Risk level: HIGH
  - Related actions: approve(address,uint256), transferFrom(address,address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xc4922d64a24675e16e1586e3e3aa56c06fabe907`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xd3494713a5cfad3f5359379dfa074e2ac8c6fd65`
  - Risk level: HIGH
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xde1fcfb0851916ca5101820a69b13a4e276bd81f`
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

- Claimed complexity: moderate
- Actual max depth: 7
- Depth mismatch: yes
- Delegatecall count: 13

Summary: Observed trace depth is moderately deeper than claimed.

### Key Findings
- Trace complexity exceeds textual complexity disclosure
  - Risk level: MEDIUM
  - Description: Observed trace depth is moderately deeper than claimed.
  - Evidence source: trace

---

## Function Semantic Match

- Dimension score: 7/10
- Severity: MEDIUM
- Summary: Claimed business actions partially match; extra non-critical business actions need review.
- Claimed actions: bridge, bridge, approval, bridge, bridge, bridge, parameter_update
- Actual actions: approval, bridge, parameter_update, transfer

### Matched Functions
- `addressToBytes32(address)`
- `approve(address,uint256)`
- `burn(address,uint256)`
- `burn(uint256)`
- `depositERC20To(address,address,address,uint256,uint32,bytes)`
- `depositForBurn(uint256,uint32,bytes32,address)`
- `depositTransaction(address,uint256,uint64,bool,bytes)`
- `getAddress(string)`
- `isUpgrading()`
- `owner(bytes32)`
- `resourceConfig()`
- `sendMessage(address,bytes,uint32)`
- `sendMessage(uint32,bytes32,bytes)`
- `setText(bytes32,string,string)`
- `supportsInterface(bytes4)`
- `transferFrom(address,address,uint256)`

### Unmatched Or Additional Actions
- `transfer`
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
  - Unaccounted addresses: 0x00000000000c2e074ec69a0dfb2997ba6c7d2e1e, 0x0a992d191deec32afe36203ad87d7d289a738f81, 0x229047fed2591dbec1ef1118d64f7af3db9eb290, 0x25ace71c97b33cc4729cf772ae268934f7ab5fa1, 0x2d778797049fe9259d947d1ed8e5442226dfb589, 0x43506849d7c04f9138d1a2050bbf3a0c054402dd, 0x4976fb03c32e5b8cfe2b6ccb31c09ba78ebaba41, 0x543ba4aadbab8f9025686bd03993043599c6fb04, 0x64b5a5ed26dcb17370ff4d33a8d503f0fbd06cff, 0x6d903f6003cca6255d85cca4d3b5e5146dc33925, 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48, 0xb2f38107a18f8599331677c14374fd3a952fb2c8, 0xba2492e52f45651b60b8b38d4ea5e2390c64ffb1, 0xbeb5fc579115071764c7423a4f12edde41f106ed, 0xc00e94cb662c3520282e6f5717214004a7f26888, 0xc4922d64a24675e16e1586e3e3aa56c06fabe907, 0xd3494713a5cfad3f5359379dfa074e2ac8c6fd65, 0xde1fcfb0851916ca5101820a69b13a4e276bd81f

### 2. MEDIUM - Trace complexity exceeds textual complexity disclosure

- **Severity**: MEDIUM
- **Description**: Observed trace depth is moderately deeper than claimed.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review whether the proposal text should describe the actual call depth or indirect execution paths.
- **Key Evidence**:
  - Complexity: claimed=moderate, actual_max_depth=7

### 3. MEDIUM - Claimed actions do not fully match trace actions

- **Severity**: MEDIUM
- **Description**: Claimed business actions partially match; extra non-critical business actions need review.
- **Evidence Source**: rule_engine
- **Confidence**: 0.9
- **Recommendation**: Compare proposal action wording with decoded functions and risk actions before relying on the text.
- **Key Evidence**:
  - Action comparison: claimed=bridge, bridge, approval, bridge, bridge, bridge, parameter_update, actual=unable to confirm

---

## Security Conclusion

The proposal has a serious Semantic Gap. Some on-chain actions are not sufficiently covered by the proposal text and may affect governance participants' judgment. Pausing or escalating to manual audit is recommended.

---

## Summary

The proposal text claims: This proposal initializes a Compound III USDC market (cUSDCv3) on Optimism. It deploys the Comet implementation, sets risk parameters, configures COMP rewards, bridges 10K USDC via CCTP to seed reserves, bridges 3.6K COMP via L1StandardBridge to seed rewards, and updates the official ENS TXT records.
The payload actually shows: approval, bridge, parameter_update, transfer. Decoded functions include: addressToBytes32(address), approve(address,uint256), burn(address,uint256), burn(uint256), depositERC20To(address,address,address,uint256,uint32,bytes), depositForBurn(uint256,uint32,bytes32,address), depositTransaction(address,uint256,uint64,bool,bytes), getAddress(string), isUpgrading(), owner(bytes32), resourceConfig(), sendMessage(address,bytes,uint32), sendMessage(uint32,bytes32,bytes), setText(bytes32,string,string), supportsInterface(bytes4), transferFrom(address,address,uint256).
The most important scoring issue is `conflict_detection`, which scored 5/10.
High-risk findings include: Unaccounted trace addresses. Pausing or escalating to manual audit is recommended.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
