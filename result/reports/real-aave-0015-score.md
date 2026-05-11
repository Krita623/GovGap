# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:23 UTC
**Proposal ID**: 355
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

### Unaccounted Addresses
- `0x081d1101855bd523ba69a9794e0217f0db6323ff`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x158a6bc04f0828318821bae797f50b0a1299d45b`
  - Risk level: CRITICAL
  - Related actions: sendMessageToChild(address,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x2150bc3c64cbfddbac9815ef615d6ab8671bfe43`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x229047fed2591dbec1ef1118d64f7af3db9eb290`
  - Risk level: CRITICAL
  - Related actions: resourceConfig()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x25ace71c97b33cc4729cf772ae268934f7ab5fa1`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x28a55488fef40005309e2da0040dbe9d300a64ab`
  - Risk level: CRITICAL
  - Related actions: depositTransaction(address,uint256,uint64,bool,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x28e4f3a7f651294b9564800b2d01f35189a5bfbe`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x2fe52ef191f0be1d98459bdad2f1d3160336c08f`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x3215225538da1546fe0da88ee13019f402078942`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x49048044d57e1c92a77f79988d21fa8faf74e97e`
  - Risk level: CRITICAL
  - Related actions: depositTransaction(address,uint256,uint64,bool,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x4dbd4fc535ac27206064b68ffcf827b0a60bab3f`
  - Risk level: CRITICAL
  - Related actions: calculateRetryableSubmissionFee(uint256,uint256), unsafeCreateRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x5aed5f8a1e3607476f1f81c3d8fe126deb0afe94`
  - Risk level: CRITICAL
  - Related actions: calculateRetryableSubmissionFee(uint256,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x5e4e65926ba27467555eb562121fac00d24e9dd2`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x5efa852e92800d1c982711761e45c3fe39a2b6d8`
  - Risk level: CRITICAL
  - Related actions: resourceConfig()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x5f5c02875a8e9b5a26fbd09040abcfdeb2aa6711`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x5fb30336a8d0841cf15d452afa297cb6d10877d7`
  - Risk level: CRITICAL
  - Related actions: depositTransaction(address,uint256,uint64,bool,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x6481ff79597fe4f77e1063f615ec5bdaddeffd4b`
  - Risk level: CRITICAL
  - Related actions: resourceConfig()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x73a79fab69143498ed3712e519a88a918e1f4072`
  - Risk level: CRITICAL
  - Related actions: resourceConfig()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x7f6b0b7589febc40419a8646eff9801b87397063`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x81c4bd600793ebd1c0323604e1f455fe50a951f8`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x866e82a600a1414e583f7f13623f1ac5d58b0afa`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x8bf439ef7167023f009e24b21719ca5f768ecb36`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x8efb6b5c4767b09dc9aa6af4eaa89f749522bae2`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x918778e825747a892b17c66fe7d24c618262867d`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
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
- `0xd3cf979e676265e4f6379749dece4708b9a22476`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xde1fcfb0851916ca5101820a69b13a4e276bd81f`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xe40e84457f4b5075f1eb32352d81ecf1de77fee6`
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

- Claimed complexity: moderate
- Actual max depth: 6
- Depth mismatch: yes
- Delegatecall count: 8

Summary: Observed trace depth exceeds claimed complexity.

### Key Findings
- Trace complexity exceeds textual complexity disclosure
  - Risk level: MEDIUM
  - Description: Observed trace depth exceeds claimed complexity.
  - Evidence source: trace

---

## Function Semantic Match

- Dimension score: 2/10
- Severity: CRITICAL
- Summary: Trace includes an unclaimed critical business action.
- Claimed actions: role_change, transfer, transfer, transfer
- Actual actions: bridge, parameter_update, transfer, upgrade

### Matched Functions
- `calculateRetryableSubmissionFee(uint256,uint256)`
- `depositTransaction(address,uint256,uint64,bool,bytes)`
- `enqueueL2GasPrepaid()`
- `execute()`
- `execute(address)`
- `getAddress(string)`
- `processL2SeqGas(address,uint256)`
- `resourceConfig()`
- `sendMessage(address,bytes,uint32)`
- `sendMessageToChild(address,bytes)`
- `syncState(address,bytes)`
- `unsafeCreateRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes)`
- `upgradeAndCall(address,address,bytes)`

### Unmatched Or Additional Actions
- `bridge`
  - Risk level: CRITICAL
  - Note: this action was not fully matched to the claimed proposal action. Review the linked evidence before relying on the proposal text.
- `parameter_update`
  - Risk level: CRITICAL
  - Note: this action was not fully matched to the claimed proposal action. Review the linked evidence before relying on the proposal text.
- `upgrade`
  - Risk level: CRITICAL
  - Note: this action was not fully matched to the claimed proposal action. Review the linked evidence before relying on the proposal text.

### Key Findings
- Claimed actions do not fully match trace actions
  - Risk level: CRITICAL
  - Description: Trace includes an unclaimed critical business action.
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
  - Unaccounted addresses: 0x081d1101855bd523ba69a9794e0217f0db6323ff, 0x158a6bc04f0828318821bae797f50b0a1299d45b, 0x2150bc3c64cbfddbac9815ef615d6ab8671bfe43, 0x229047fed2591dbec1ef1118d64f7af3db9eb290, 0x25ace71c97b33cc4729cf772ae268934f7ab5fa1, 0x28a55488fef40005309e2da0040dbe9d300a64ab, 0x28e4f3a7f651294b9564800b2d01f35189a5bfbe, 0x2fe52ef191f0be1d98459bdad2f1d3160336c08f, 0x3215225538da1546fe0da88ee13019f402078942, 0x49048044d57e1c92a77f79988d21fa8faf74e97e, 0x4dbd4fc535ac27206064b68ffcf827b0a60bab3f, 0x5aed5f8a1e3607476f1f81c3d8fe126deb0afe94, 0x5e4e65926ba27467555eb562121fac00d24e9dd2, 0x5efa852e92800d1c982711761e45c3fe39a2b6d8, 0x5f5c02875a8e9b5a26fbd09040abcfdeb2aa6711, 0x5fb30336a8d0841cf15d452afa297cb6d10877d7, 0x6481ff79597fe4f77e1063f615ec5bdaddeffd4b, 0x73a79fab69143498ed3712e519a88a918e1f4072, 0x7f6b0b7589febc40419a8646eff9801b87397063, 0x81c4bd600793ebd1c0323604e1f455fe50a951f8, 0x866e82a600a1414e583f7f13623f1ac5d58b0afa, 0x8bf439ef7167023f009e24b21719ca5f768ecb36, 0x8efb6b5c4767b09dc9aa6af4eaa89f749522bae2, 0x918778e825747a892b17c66fe7d24c618262867d, 0xbeb5fc579115071764c7423a4f12edde41f106ed, 0xd1b3e25fd7c8ae7caddc6f71b461b79cd4ddcfa3, 0xd3cf979e676265e4f6379749dece4708b9a22476, 0xde1fcfb0851916ca5101820a69b13a4e276bd81f, 0xe40e84457f4b5075f1eb32352d81ecf1de77fee6, 0xec568fffba86c094cf06b22134b23074dfe2252c, 0xfe5e5d361b2ad62c541bab87c45a0b9b018389a2

### 2. MEDIUM - Trace complexity exceeds textual complexity disclosure

- **Severity**: MEDIUM
- **Description**: Observed trace depth exceeds claimed complexity.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review whether the proposal text should describe the actual call depth or indirect execution paths.
- **Key Evidence**:
  - Complexity: claimed=moderate, actual_max_depth=6

### 3. CRITICAL - Claimed actions do not fully match trace actions

- **Severity**: CRITICAL
- **Description**: Trace includes an unclaimed critical business action.
- **Evidence Source**: rule_engine
- **Confidence**: 0.9
- **Recommendation**: Compare proposal action wording with decoded functions and risk actions before relying on the text.
- **Key Evidence**:
  - Action comparison: claimed=role_change, transfer, transfer, transfer, actual=unable to confirm

---

## Security Conclusion

The proposal has a critical Semantic Gap or potential attack indicators. The textual commitment and observed on-chain behavior are severely inconsistent. Do not execute without immediate manual security review.

---

## Summary

The proposal text claims: Proposal for the partial activation of Aave Governance v3 in an interim Aave Governance v2.5 version. It migrates Level 1 (Short) permissions to v3 Executors, funds a.DI, Aave Robot, and the Aave Gelato gas tank.
The payload actually shows: bridge, parameter_update, transfer, upgrade. Decoded functions include: calculateRetryableSubmissionFee(uint256,uint256), depositTransaction(address,uint256,uint64,bool,bytes), enqueueL2GasPrepaid(), execute(), execute(address), getAddress(string), processL2SeqGas(address,uint256), resourceConfig(), sendMessage(address,bytes,uint32), sendMessageToChild(address,bytes), syncState(address,bytes), unsafeCreateRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes), upgradeAndCall(address,address,bytes).
The most important scoring issue is `conflict_detection`, which scored 2/10.
High-risk findings include: Unaccounted trace addresses, Claimed actions do not fully match trace actions. Pausing or escalating to manual audit is recommended.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
