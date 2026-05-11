# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:24 UTC
**Proposal ID**: 13214174724111749338017943143826453367599509196993220699255450633508989705578
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
- `0x1ba8603da702602a8657980e825a6daa03dee93a`
- `0x1bb64af7fe05fc69c740609267d2abe3e119ef82`
- `0x1d65c6d3ad39d454ea8f682c49ae7744706ea96d`
- `0x3466eb008edd8d5052446293d1a7d212cb65c646`
- `0x64ca550f78d6cc711b247319cc71a04a166707ab`
- `0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48`
- `0xc18360217d8f7ab5e7c516566761ea12ce7f9d72`
- `0xcfa132e353cb4e398080b9700609bb008eceb125`
- `0xfe89cc7abb2c4183683ab71653c4cdc9b02d44b7`

### Unaccounted Addresses
- `0x0fb7694c990cf19001127391dbe53924dd7a61c7`
  - Risk level: CRITICAL
  - Related actions: decodeCtx(bytes), forwardBatchCall((uint32,address,bytes)[]), getGovernance(), isAgreementClassListed(address), isApp(address), isCtxValid(bytes), mapAgreementClasses(uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x1820a4b7618bde71dce8cdc73aab6c95905fad24`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x2844c1bbda121e9e43105630b9c8310e5c72744b`
  - Risk level: CRITICAL
  - Related actions: agreementType(), createFlow(address,address,int96,bytes), getFlow(address,address,address), realtimeBalanceOf(address,address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x3acf197e729fb2816dca7d61f3622ed77ecabbf7`
  - Risk level: CRITICAL
  - Related actions: delegatecall
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x43506849d7c04f9138d1a2050bbf3a0c054402dd`
  - Risk level: CRITICAL
  - Related actions: approve(address,uint256), balanceOf(address), increaseAllowance(address,uint256), transferFrom(address,address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x4e583d9390082b65bef884b629dfa426114ced6d`
  - Risk level: CRITICAL
  - Related actions: decodeCtx(bytes), forwardBatchCall((uint32,address,bytes)[]), getGovernance(), isAgreementClassListed(address), isApp(address), isCtxValid(bytes), mapAgreementClasses(uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x87e00dced5670e01bee33a9a724b1dac790937ef`
  - Risk level: CRITICAL
  - Related actions: getConfigAsUint256(address,address,bytes32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xa794c9ee519fd31bbce643e8d8138f735e97d1db`
  - Risk level: CRITICAL
  - Related actions: realtimeBalanceOf(address,address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xbcf9cfa8da20b591790df27de65c1254bf91563d`
  - Risk level: CRITICAL
  - Related actions: delegatecall, realtimeBalanceOf(address,address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xd0de1486f69495d49c02d8f541b7dadf9cf5cd91`
  - Risk level: CRITICAL
  - Related actions: agreementType(), createFlow(address,address,int96,bytes), getFlow(address,address,address), realtimeBalanceOf(address,address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xe2e14e2c4518cb06c32cd0818b4c01f53e1ba653`
  - Risk level: CRITICAL
  - Related actions: getConfigAsUint256(address,address,bytes32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xeb69ed9143d33d5fbad67f394456f212c65c1544`
  - Risk level: CRITICAL
  - Related actions: CONSTANT_OUTFLOW_NFT(), getAgreementData(address,bytes32,uint256), getAgreementStateSlot(address,address,uint256,uint256), getHost(), realtimeBalanceOf(address,uint256), settleBalance(address,int256), updateAgreementData(bytes32,bytes32[]), updateAgreementStateSlot(address,uint256,bytes32[]), upgrade(uint256)
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
- Actual max depth: 11
- Depth mismatch: yes
- Delegatecall count: 41

The actual call chain is deep and may increase review difficulty.

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
- Claimed actions: approval, transfer, transfer, approval, approval, transfer
- Actual actions: approval, parameter_update, transfer, upgrade

### Matched Functions
- `CONSTANT_OUTFLOW_NFT()`
- `agreementType()`
- `approve(address,uint256)`
- `balanceOf(address)`
- `batchVestingPlans(address,address,uint256,(address,uint256,uint256,uint256,uint256)[],uint256,address,bool,uint8)`
- `createFlow(address,address,int96,bytes)`
- `decodeCtx(bytes)`
- `forwardBatchCall((uint32,address,bytes)[])`
- `getAgreementData(address,bytes32,uint256)`
- `getAgreementStateSlot(address,address,uint256,uint256)`
- `getConfigAsUint256(address,address,bytes32)`
- `getFlow(address,address,address)`
- `getGovernance()`
- `getHost()`
- `getInterfaceImplementer(address,bytes32)`
- `increaseAllowance(address,uint256)`
- `isAgreementClassListed(address)`
- `isApp(address)`
- `isCtxValid(bytes)`
- `mapAgreementClasses(uint256)`
- `realtimeBalanceOf(address,address,uint256)`
- `realtimeBalanceOf(address,uint256)`
- `setFlowrate(address,address,int96)`
- `settleBalance(address,int256)`
- `transferFrom(address,address,uint256)`
- `updateAgreementData(bytes32,bytes32[])`
- `updateAgreementStateSlot(address,uint256,bytes32[])`
- `upgrade(uint256)`

### Unmatched Or Additional Actions
- `parameter_update`
  - Risk level: CRITICAL
  - Note: this action was not fully matched to the claimed proposal action. Review the linked evidence before relying on the proposal text.
- `upgrade`
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
  - Unaccounted addresses: 0x0fb7694c990cf19001127391dbe53924dd7a61c7, 0x1820a4b7618bde71dce8cdc73aab6c95905fad24, 0x2844c1bbda121e9e43105630b9c8310e5c72744b, 0x3acf197e729fb2816dca7d61f3622ed77ecabbf7, 0x43506849d7c04f9138d1a2050bbf3a0c054402dd, 0x4e583d9390082b65bef884b629dfa426114ced6d, 0x87e00dced5670e01bee33a9a724b1dac790937ef, 0xa794c9ee519fd31bbce643e8d8138f735e97d1db, 0xbcf9cfa8da20b591790df27de65c1254bf91563d, 0xd0de1486f69495d49c02d8f541b7dadf9cf5cd91, 0xe2e14e2c4518cb06c32cd0818b4c01f53e1ba653, 0xeb69ed9143d33d5fbad67f394456f212c65c1544

### 2. HIGH - Trace complexity exceeds textual complexity disclosure

- **Severity**: HIGH
- **Description**: Observed trace depth exceeds claimed complexity.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review whether the proposal text should describe the actual call depth or indirect execution paths.
- **Key Evidence**:
  - Complexity: claimed=moderate, actual_max_depth=11

### 3. CRITICAL - Claimed actions do not fully match trace actions

- **Severity**: CRITICAL
- **Description**: Text claims a low-risk action while the trace includes a sensitive business action.
- **Evidence Source**: rule_engine
- **Confidence**: 0.9
- **Recommendation**: Compare proposal action wording with decoded functions and risk actions before relying on the text.
- **Key Evidence**:
  - Action comparison: claimed=approval, transfer, transfer, approval, approval, transfer, actual=unable to confirm

---

## Security Conclusion

The proposal has a critical Semantic Gap or potential attack indicators. The textual commitment and observed on-chain behavior are severely inconsistent. Do not execute without immediate manual security review.

---

## Summary

The proposal text claims: Funding request for Unruggable to build and operate a network of gateways supporting EVM-chain Reverse Resolution (ENSIP-19). Requests $1,200,000 USDC streamed over 1 year and 24,000 ENS tokens vested over 2 years.
The payload actually shows: approval, parameter_update, transfer, upgrade. Decoded functions include: CONSTANT_OUTFLOW_NFT(), agreementType(), approve(address,uint256), balanceOf(address), batchVestingPlans(address,address,uint256,(address,uint256,uint256,uint256,uint256)[],uint256,address,bool,uint8), createFlow(address,address,int96,bytes), decodeCtx(bytes), forwardBatchCall((uint32,address,bytes)[]), getAgreementData(address,bytes32,uint256), getAgreementStateSlot(address,address,uint256,uint256), getConfigAsUint256(address,address,bytes32), getFlow(address,address,address), getGovernance(), getHost(), getInterfaceImplementer(address,bytes32), increaseAllowance(address,uint256), isAgreementClassListed(address), isApp(address), isCtxValid(bytes), mapAgreementClasses(uint256), realtimeBalanceOf(address,address,uint256), realtimeBalanceOf(address,uint256), setFlowrate(address,address,int96), settleBalance(address,int256), transferFrom(address,address,uint256), updateAgreementData(bytes32,bytes32[]), updateAgreementStateSlot(address,uint256,bytes32[]), upgrade(uint256).
The most important scoring issue is `conflict_detection`, which scored 2/10.
High-risk findings include: Unaccounted trace addresses, Trace complexity exceeds textual complexity disclosure, Claimed actions do not fully match trace actions. Pausing or escalating to manual audit is recommended.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
