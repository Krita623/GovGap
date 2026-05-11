# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:23 UTC
**Proposal ID**: 234
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
- `0x4c0633bf70fb2bb984a9eec5d9052bdea451c70a`
- `0x5e76e98e0963ecdc6a065d1435f84065b7523f39`
- `0x5f4d15d761528c57a5c30c43c1dab26fc5452731`
- `0x7e1f23bdfc7287af276f77b5a867e85cf0377a31`
- `0x82dccf206ae2ab46e2099e663f70dee77cae7778`
- `0x90127a46207e97e4205db5ccc1ec9d6d43633fd4`
- `0xa3e44d830440df5098520f62ebec285b1198c51e`
- `0xadf86b537ef08591c2777e144322e8b0ca7e82a7`
- `0xc5de989e0d1bf605d19478fdd32aa827a10b464f`
- `0xd2c92b5a793e196ab11dbefbe3af6bdded6c3dd5`
- `0xd91d1331db4f436daf47ec9dd86decb8eef946b4`
- `0xe79ca44408dae5a57ea2a9594532f1e84d2edaa4`

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
- `0x2fe52ef191f0be1d98459bdad2f1d3160336c08f`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
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
- `0x5f5c02875a8e9b5a26fbd09040abcfdeb2aa6711`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x7f6b0b7589febc40419a8646eff9801b87397063`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x8bf439ef7167023f009e24b21719ca5f768ecb36`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x918778e825747a892b17c66fe7d24c618262867d`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xc2aacf6553d20d1e9d78e365aaba8032af9c85b0`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xd1b3e25fd7c8ae7caddc6f71b461b79cd4ddcfa3`
  - Risk level: CRITICAL
  - Related actions: unsafeCreateRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xd9166833ff12a5f900ccfbf2c8b62a90f1ca1fd5`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
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
- Actual max depth: 3
- Depth mismatch: yes
- Delegatecall count: 3

Summary: Observed trace depth exceeds claimed complexity.

### Key Findings
- Trace complexity exceeds textual complexity disclosure
  - Risk level: MEDIUM
  - Description: Observed trace depth exceeds claimed complexity.
  - Evidence source: trace

---

## Function Semantic Match

- Dimension score: 3/10
- Severity: HIGH
- Summary: Trace includes an unclaimed high-risk business action.
- Claimed actions: role_change, role_change
- Actual actions: bridge, transfer

### Matched Functions
- `addRiskAdmin(address)`
- `calculateRetryableSubmissionFee(uint256,uint256)`
- `enqueue(address,uint256,bytes)`
- `enqueueL2GasPrepaid()`
- `execute()`
- `execute(address)`
- `getAddress(string)`
- `getQueueLength()`
- `processL2SeqGas(address,uint256)`
- `sendMessage(address,bytes,uint32)`
- `sendMessageToChild(address,bytes)`
- `syncState(address,bytes)`
- `unsafeCreateRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes)`

### Unmatched Or Additional Actions
- `bridge`
  - Risk level: HIGH
  - Note: this action was not fully matched to the claimed proposal action. Review the linked evidence before relying on the proposal text.
- `transfer`
  - Risk level: HIGH
  - Note: this action was not fully matched to the claimed proposal action. Review the linked evidence before relying on the proposal text.

### Key Findings
- Claimed actions do not fully match trace actions
  - Risk level: HIGH
  - Description: Trace includes an unclaimed high-risk business action.
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
  - Unaccounted addresses: 0x081d1101855bd523ba69a9794e0217f0db6323ff, 0x158a6bc04f0828318821bae797f50b0a1299d45b, 0x25ace71c97b33cc4729cf772ae268934f7ab5fa1, 0x28e4f3a7f651294b9564800b2d01f35189a5bfbe, 0x2fe52ef191f0be1d98459bdad2f1d3160336c08f, 0x4dbd4fc535ac27206064b68ffcf827b0a60bab3f, 0x5aed5f8a1e3607476f1f81c3d8fe126deb0afe94, 0x5e4e65926ba27467555eb562121fac00d24e9dd2, 0x5f5c02875a8e9b5a26fbd09040abcfdeb2aa6711, 0x7f6b0b7589febc40419a8646eff9801b87397063, 0x8bf439ef7167023f009e24b21719ca5f768ecb36, 0x918778e825747a892b17c66fe7d24c618262867d, 0xc2aacf6553d20d1e9d78e365aaba8032af9c85b0, 0xd1b3e25fd7c8ae7caddc6f71b461b79cd4ddcfa3, 0xd9166833ff12a5f900ccfbf2c8b62a90f1ca1fd5, 0xde1fcfb0851916ca5101820a69b13a4e276bd81f, 0xec568fffba86c094cf06b22134b23074dfe2252c, 0xfe5e5d361b2ad62c541bab87c45a0b9b018389a2

### 2. MEDIUM - Trace complexity exceeds textual complexity disclosure

- **Severity**: MEDIUM
- **Description**: Observed trace depth exceeds claimed complexity.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review whether the proposal text should describe the actual call depth or indirect execution paths.
- **Key Evidence**:
  - Complexity: claimed=simple, actual_max_depth=3

### 3. HIGH - Claimed actions do not fully match trace actions

- **Severity**: HIGH
- **Description**: Trace includes an unclaimed high-risk business action.
- **Evidence Source**: rule_engine
- **Confidence**: 0.9
- **Recommendation**: Compare proposal action wording with decoded functions and risk actions before relying on the text.
- **Key Evidence**:
  - Action comparison: claimed=role_change, role_change, actual=unable to confirm

---

## Security Conclusion

The proposal has a critical Semantic Gap or potential attack indicators. The textual commitment and observed on-chain behavior are severely inconsistent. Do not execute without immediate manual security review.

---

## Summary

The proposal text claims: Grants the RISK_ADMIN role to a CapsPlusRiskStewards smart contract on each network with an active Aave v3 instance, enabling the RISK_COUNCIL to adjust asset caps upwards without voting overhead.
The payload actually shows: bridge, transfer. Decoded functions include: addRiskAdmin(address), calculateRetryableSubmissionFee(uint256,uint256), enqueue(address,uint256,bytes), enqueueL2GasPrepaid(), execute(), execute(address), getAddress(string), getQueueLength(), processL2SeqGas(address,uint256), sendMessage(address,bytes,uint32), sendMessageToChild(address,bytes), syncState(address,bytes), unsafeCreateRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes).
The most important scoring issue is `conflict_detection`, which scored 2/10.
High-risk findings include: Unaccounted trace addresses, Claimed actions do not fully match trace actions. Pausing or escalating to manual audit is recommended.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
