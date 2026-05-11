# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:23 UTC
**Proposal ID**: 255
**Simulation Status**: success
**Trace Source**: simulated_trace

---

## Consistency Score

**Overall Score**: 4/10
**Risk Level**: HIGH
**Scoring Method**: worst-case risk gating, not weighted average.

Overall score uses minimum dimension score 4 capped by highest severity HIGH.

Some dimensions may be acceptable, but the overall score is limited by High or Critical rule-engine findings.

---

## Conflict Detection

- Dimension score: 5/10
- Severity: HIGH
- Summary: An undisclosed address participates in an uncovered approval or transfer action.

### Unaccounted Addresses
- `0x0475cbcaebd9ce8afa5025828d5b98dfb67e059e`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x1066cecc8880948fe55e427e94f1ff221d626591`
  - Risk level: HIGH
  - Related actions: delegatecall
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x3154cf16ccdb4c6d922629664174b904d80f2c35`
  - Risk level: HIGH
  - Related actions: depositERC20To(address,address,address,uint256,uint32,bytes), sendMessage(address,bytes,uint32), transferFrom(address,address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b`
  - Risk level: HIGH
  - Related actions: _grantComp(address,uint256), transfer(address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x3f3c0f6bc115e698e35038e1759e9c31032e590c`
  - Risk level: HIGH
  - Related actions: depositERC20To(address,address,address,uint256,uint32,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x49048044d57e1c92a77f79988d21fa8faf74e97e`
  - Risk level: HIGH
  - Related actions: depositTransaction(address,uint256,uint64,bool,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x4dbd4fc535ac27206064b68ffcf827b0a60bab3f`
  - Risk level: HIGH
  - Related actions: createRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes), transfer
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x52595021fa01b3e14ec6c88953afc8e35dff423c`
  - Risk level: HIGH
  - Related actions: outboundTransferCustomRefund(address,address,address,uint256,uint256,uint256,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x5aed5f8a1e3607476f1f81c3d8fe126deb0afe94`
  - Risk level: HIGH
  - Related actions: createRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x5fb30336a8d0841cf15d452afa297cb6d10877d7`
  - Risk level: HIGH
  - Related actions: depositTransaction(address,uint256,uint64,bool,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x6481ff79597fe4f77e1063f615ec5bdaddeffd4b`
  - Risk level: HIGH
  - Related actions: resourceConfig()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x6d903f6003cca6255d85cca4d3b5e5146dc33925`
  - Risk level: HIGH
  - Related actions: approve(address,uint256), outboundTransferCustomRefund(address,address,address,uint256,uint256,uint256,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x72ce9c846789fdb6fc1f34ac4ad25dd9ef7031ef`
  - Risk level: HIGH
  - Related actions: outboundTransferCustomRefund(address,address,address,uint256,uint256,uint256,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x73a79fab69143498ed3712e519a88a918e1f4072`
  - Risk level: HIGH
  - Related actions: resourceConfig()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x81c4bd600793ebd1c0323604e1f455fe50a951f8`
  - Risk level: HIGH
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x8315177ab297ba92a06054ce80a67ed4dbd7ed3a`
  - Risk level: HIGH
  - Related actions: delegatecall, transfer
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x866e82a600a1414e583f7f13623f1ac5d58b0afa`
  - Risk level: HIGH
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x8efb6b5c4767b09dc9aa6af4eaa89f749522bae2`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xa3a7b6f88361f48403514059f1f16c8e78d60eec`
  - Risk level: HIGH
  - Related actions: createRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes), outboundTransferCustomRefund(address,address,address,uint256,uint256,uint256,bytes), transferFrom(address,address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xb4299a1f5f26ff6a98b7ba35572290c359fde900`
  - Risk level: HIGH
  - Related actions: outboundTransferCustomRefund(address,address,address,uint256,uint256,uint256,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xbafe01ff935c7305907c33bf824352ee5979b526`
  - Risk level: HIGH
  - Related actions: _grantComp(address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xc00e94cb662c3520282e6f5717214004a7f26888`
  - Risk level: HIGH
  - Related actions: approve(address,uint256), transfer(address,uint256), transferFrom(address,address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.

### Key Findings
- Unaccounted trace addresses
  - Risk level: HIGH
  - Description: One or more addresses appeared in the trace without direct proposal text disclosure.
  - Evidence source: trace

---

## Depth Analysis

- Claimed complexity: simple
- Actual max depth: 7
- Depth mismatch: yes
- Delegatecall count: 11

Summary: Observed trace depth exceeds claimed complexity.

### Key Findings
- Trace complexity exceeds textual complexity disclosure
  - Risk level: HIGH
  - Description: Observed trace depth exceeds claimed complexity.
  - Evidence source: trace

---

## Function Semantic Match

- Dimension score: 4/10
- Severity: HIGH
- Summary: Claimed business action categories differ from extracted business actions.
- Claimed actions: transfer, bridge, bridge
- Actual actions: approval, bridge, parameter_update, transfer

### Matched Functions
- `_grantComp(address,uint256)`
- `approve(address,uint256)`
- `balanceOf(address)`
- `createRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes)`
- `decimals()`
- `depositERC20To(address,address,address,uint256,uint32,bytes)`
- `depositTransaction(address,uint256,uint64,bool,bytes)`
- `getAddress(string)`
- `isUpgrading()`
- `name()`
- `outboundTransferCustomRefund(address,address,address,uint256,uint256,uint256,bytes)`
- `resourceConfig()`
- `sendMessage(address,bytes,uint32)`
- `supportsInterface(bytes4)`
- `symbol()`
- `transfer(address,uint256)`
- `transferFrom(address,address,uint256)`

### Unmatched Or Additional Actions
- `approval`
  - Risk level: HIGH
  - Note: this action was not fully matched to the claimed proposal action. Review the linked evidence before relying on the proposal text.
- `parameter_update`
  - Risk level: HIGH
  - Note: this action was not fully matched to the claimed proposal action. Review the linked evidence before relying on the proposal text.

### Key Findings
- Claimed actions do not fully match trace actions
  - Risk level: HIGH
  - Description: Claimed business action categories differ from extracted business actions.
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
  - Unaccounted addresses: 0x0475cbcaebd9ce8afa5025828d5b98dfb67e059e, 0x1066cecc8880948fe55e427e94f1ff221d626591, 0x3154cf16ccdb4c6d922629664174b904d80f2c35, 0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b, 0x3f3c0f6bc115e698e35038e1759e9c31032e590c, 0x49048044d57e1c92a77f79988d21fa8faf74e97e, 0x4dbd4fc535ac27206064b68ffcf827b0a60bab3f, 0x52595021fa01b3e14ec6c88953afc8e35dff423c, 0x5aed5f8a1e3607476f1f81c3d8fe126deb0afe94, 0x5fb30336a8d0841cf15d452afa297cb6d10877d7, 0x6481ff79597fe4f77e1063f615ec5bdaddeffd4b, 0x6d903f6003cca6255d85cca4d3b5e5146dc33925, 0x72ce9c846789fdb6fc1f34ac4ad25dd9ef7031ef, 0x73a79fab69143498ed3712e519a88a918e1f4072, 0x81c4bd600793ebd1c0323604e1f455fe50a951f8, 0x8315177ab297ba92a06054ce80a67ed4dbd7ed3a, 0x866e82a600a1414e583f7f13623f1ac5d58b0afa, 0x8efb6b5c4767b09dc9aa6af4eaa89f749522bae2, 0xa3a7b6f88361f48403514059f1f16c8e78d60eec, 0xb4299a1f5f26ff6a98b7ba35572290c359fde900, 0xbafe01ff935c7305907c33bf824352ee5979b526, 0xc00e94cb662c3520282e6f5717214004a7f26888

### 2. HIGH - Trace complexity exceeds textual complexity disclosure

- **Severity**: HIGH
- **Description**: Observed trace depth exceeds claimed complexity.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review whether the proposal text should describe the actual call depth or indirect execution paths.
- **Key Evidence**:
  - Complexity: claimed=simple, actual_max_depth=7

### 3. HIGH - Claimed actions do not fully match trace actions

- **Severity**: HIGH
- **Description**: Claimed business action categories differ from extracted business actions.
- **Evidence Source**: rule_engine
- **Confidence**: 0.9
- **Recommendation**: Compare proposal action wording with decoded functions and risk actions before relying on the text.
- **Key Evidence**:
  - Action comparison: claimed=transfer, bridge, bridge, actual=unable to confirm

---

## Security Conclusion

The proposal has a serious Semantic Gap. Some on-chain actions are not sufficiently covered by the proposal text and may affect governance participants' judgment. Pausing or escalating to manual audit is recommended.

---

## Summary

The proposal text claims: Gauntlet recommends adding COMP to the reward contracts for Ethereum (28,000 COMP), Base (3,600 COMP), and Arbitrum (2,250 COMP).
The payload actually shows: approval, bridge, parameter_update, transfer. Decoded functions include: _grantComp(address,uint256), approve(address,uint256), balanceOf(address), createRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes), decimals(), depositERC20To(address,address,address,uint256,uint32,bytes), depositTransaction(address,uint256,uint64,bool,bytes), getAddress(string), isUpgrading(), name(), outboundTransferCustomRefund(address,address,address,uint256,uint256,uint256,bytes), resourceConfig(), sendMessage(address,bytes,uint32), supportsInterface(bytes4), symbol(), transfer(address,uint256), transferFrom(address,address,uint256).
The most important scoring issue is `function_semantic_match`, which scored 4/10.
High-risk findings include: Unaccounted trace addresses, Trace complexity exceeds textual complexity disclosure, Claimed actions do not fully match trace actions. Pausing or escalating to manual audit is recommended.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
