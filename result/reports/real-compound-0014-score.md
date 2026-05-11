# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:24 UTC
**Proposal ID**: 426
**Simulation Status**: success
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
- `0x18084fba666a33d37592fa2633fd49a74dd93a88`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x1923dfee706a8e78157416c29cbccfde7cdf4102`
  - Risk level: CRITICAL
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x192e29ffd0bcfb2326a18d88d77521a89b90fccd`
  - Risk level: CRITICAL
  - Related actions: contract_creation
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x1ec63b5883c3481134fd50d5daebc83ecd2e8779`
  - Risk level: CRITICAL
  - Related actions: upgradeTo(address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x1fa408992e74a42d1787e28b880c451452e8c958`
  - Risk level: CRITICAL
  - Related actions: contract_creation
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
- `0x2665701293fcbeb223d11a08d826563edcce423a`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x28e4f3a7f651294b9564800b2d01f35189a5bfbe`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x2d7e764a0d9919e16983a46595cfa81fc34fa7cd`
  - Risk level: CRITICAL
  - Related actions: depositTransaction(address,uint256,uint64,bool,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x316f9708bb98af7da9c68c1c3b5e79039cd336e3`
  - Risk level: CRITICAL
  - Related actions: deploy(address), updateAssetBorrowCollateralFactor(address,address,uint64)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x31b844dbc7cdbaa27d22fd6d54986836d023bf3f`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x3ea6084748ed1b2a9b5d4426181f1ad8c93f6231`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x3ff744cf6078714bb9d3c4fe5ab37fa6d05dec4e`
  - Risk level: CRITICAL
  - Related actions: contract_creation
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x4c9edd5852cd905f086c759e8383e09bff1e68b3`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x4dbd4fc535ac27206064b68ffcf827b0a60bab3f`
  - Risk level: CRITICAL
  - Related actions: createRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes), transfer
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x4e7991e5c547ce825bdeb665ee14a3274f9f61e0`
  - Risk level: CRITICAL
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x592700e4fcdd674dc54d2681ded3b63f54f63f9a`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x5d409e56d886231adaf00c8775665ad0f9897b56`
  - Risk level: CRITICAL
  - Related actions: upgradeTo(address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x5e2420cace3650622f62b2713b2b3727fc8bcdd1`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x5f4ec3df9cbd43714fe2740f5e3616155c5b8419`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x6d903f6003cca6255d85cca4d3b5e5146dc33925`
  - Risk level: CRITICAL
  - Related actions: createRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes), sendMessage(address,bytes,uint32), sendMessageToChild(address,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x7458bfdc30034eb860b265e6068121d18fa5aa72`
  - Risk level: CRITICAL
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x760c48c62a85045a6b69f07f4a9f22868659cbcc`
  - Risk level: CRITICAL
  - Related actions: resourceConfig()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x7c058ad1d0ee415f7e7f30e62db1bcf568470a10`
  - Risk level: CRITICAL
  - Related actions: createRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x7d4e742018fb52e48b08be73d041c18b21de6fb5`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x7de363b6bf0a892b94a1cd0c9df76826bfc14228`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x8315177ab297ba92a06054ce80a67ed4dbd7ed3a`
  - Risk level: CRITICAL
  - Related actions: delegatecall, transfer
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x8350b7de6a6a2c1368e7d4bd968190e13e354297`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x93e8f92327bfa8096f5f6ee5f2a49183d3b3b898`
  - Risk level: CRITICAL
  - Related actions: delegatecall
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xa3931d71877c0e7a3148cb7eb4463524fec27fbd`
  - Risk level: CRITICAL
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xa569d910839ae8865da8f8e70fffb0cba869f961`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xb7dabef05ab656123d0274c4c39e4ce4eb894b89`
  - Risk level: CRITICAL
  - Related actions: contract_creation
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xbeb5fc579115071764c7423a4f12edde41f106ed`
  - Risk level: CRITICAL
  - Related actions: depositTransaction(address,uint256,uint64,bool,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf`
  - Risk level: CRITICAL
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xcc16f670129f965b396f2e81312f6e339ffdb18e`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xcfc1fa6b7ca982176529899d99af6473ad80df4f`
  - Risk level: CRITICAL
  - Related actions: deploy(address), updateAssetBorrowCollateralFactor(address,address,uint64)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xd4ec911b8fd79139736950235a93d3ea9c3f68ed`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xdae05e337c56cd1b988fd7a6b74e8bbd3028c4c6`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xdc035d45d973e3ec169d2276ddab16f1e407384f`
  - Risk level: CRITICAL
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xde1fcfb0851916ca5101820a69b13a4e276bd81f`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xfe5e5d361b2ad62c541bab87c45a0b9b018389a2`
  - Risk level: CRITICAL
  - Related actions: sendMessageToChild(address,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xff30586cd0f29ed462364c7e81375fc0c71219b1`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
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
- Actual max depth: 8
- Depth mismatch: yes
- Delegatecall count: 10

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
- Actual actions: bridge, contract_creation, parameter_update, transfer, upgrade

### Matched Functions
- `assetListFactory()`
- `clone((address,address,address,address,address,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint104,uint104,uint104,(address,address,uint8,uint64,uint64,uint64,uint128)[]))`
- `createAssetList((address,address,uint8,uint64,uint64,uint64,uint128)[])`
- `createRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes)`
- `decimals()`
- `deploy(address)`
- `deployAndUpgradeTo(address,address)`
- `depositTransaction(address,uint256,uint64,bool,bytes)`
- `getAddress(string)`
- `resourceConfig()`
- `sendMessage(address,bytes,uint32)`
- `sendMessageToChild(address,bytes)`
- `syncState(address,bytes)`
- `updateAssetBorrowCollateralFactor(address,address,uint64)`
- `upgradeTo(address)`

### Unmatched Or Additional Actions
- `bridge`
  - Risk level: CRITICAL
  - Note: this action was not fully matched to the claimed proposal action. Review the linked evidence before relying on the proposal text.
- `contract_creation`
  - Risk level: CRITICAL
  - Note: this action was not fully matched to the claimed proposal action. Review the linked evidence before relying on the proposal text.
- `transfer`
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
  - Unaccounted addresses: 0x18084fba666a33d37592fa2633fd49a74dd93a88, 0x1923dfee706a8e78157416c29cbccfde7cdf4102, 0x192e29ffd0bcfb2326a18d88d77521a89b90fccd, 0x1ec63b5883c3481134fd50d5daebc83ecd2e8779, 0x1fa408992e74a42d1787e28b880c451452e8c958, 0x229047fed2591dbec1ef1118d64f7af3db9eb290, 0x25ace71c97b33cc4729cf772ae268934f7ab5fa1, 0x2665701293fcbeb223d11a08d826563edcce423a, 0x28e4f3a7f651294b9564800b2d01f35189a5bfbe, 0x2d7e764a0d9919e16983a46595cfa81fc34fa7cd, 0x316f9708bb98af7da9c68c1c3b5e79039cd336e3, 0x31b844dbc7cdbaa27d22fd6d54986836d023bf3f, 0x3ea6084748ed1b2a9b5d4426181f1ad8c93f6231, 0x3ff744cf6078714bb9d3c4fe5ab37fa6d05dec4e, 0x4c9edd5852cd905f086c759e8383e09bff1e68b3, 0x4dbd4fc535ac27206064b68ffcf827b0a60bab3f, 0x4e7991e5c547ce825bdeb665ee14a3274f9f61e0, 0x592700e4fcdd674dc54d2681ded3b63f54f63f9a, 0x5d409e56d886231adaf00c8775665ad0f9897b56, 0x5e2420cace3650622f62b2713b2b3727fc8bcdd1, 0x5f4ec3df9cbd43714fe2740f5e3616155c5b8419, 0x6d903f6003cca6255d85cca4d3b5e5146dc33925, 0x7458bfdc30034eb860b265e6068121d18fa5aa72, 0x760c48c62a85045a6b69f07f4a9f22868659cbcc, 0x7c058ad1d0ee415f7e7f30e62db1bcf568470a10, 0x7d4e742018fb52e48b08be73d041c18b21de6fb5, 0x7de363b6bf0a892b94a1cd0c9df76826bfc14228, 0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0, 0x8315177ab297ba92a06054ce80a67ed4dbd7ed3a, 0x8350b7de6a6a2c1368e7d4bd968190e13e354297, 0x93e8f92327bfa8096f5f6ee5f2a49183d3b3b898, 0xa3931d71877c0e7a3148cb7eb4463524fec27fbd, 0xa569d910839ae8865da8f8e70fffb0cba869f961, 0xb7dabef05ab656123d0274c4c39e4ce4eb894b89, 0xbeb5fc579115071764c7423a4f12edde41f106ed, 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2, 0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf, 0xcc16f670129f965b396f2e81312f6e339ffdb18e, 0xcfc1fa6b7ca982176529899d99af6473ad80df4f, 0xd4ec911b8fd79139736950235a93d3ea9c3f68ed, 0xdae05e337c56cd1b988fd7a6b74e8bbd3028c4c6, 0xdc035d45d973e3ec169d2276ddab16f1e407384f, 0xde1fcfb0851916ca5101820a69b13a4e276bd81f, 0xfe5e5d361b2ad62c541bab87c45a0b9b018389a2, 0xff30586cd0f29ed462364c7e81375fc0c71219b1

### 2. HIGH - Trace complexity exceeds textual complexity disclosure

- **Severity**: HIGH
- **Description**: Observed trace depth exceeds claimed complexity.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review whether the proposal text should describe the actual call depth or indirect execution paths.
- **Key Evidence**:
  - Complexity: claimed=simple, actual_max_depth=8

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

The proposal text claims: Gauntlet recommends updating risk parameters including Liquidation Penalty, Liquidation Factor, and Collateral Factor for WETH and wstETH collateral assets across multiple Compound V3 deployments on Ethereum, Arbitrum, Optimism, and Polygon.
The payload actually shows: bridge, contract_creation, parameter_update, transfer, upgrade. Decoded functions include: assetListFactory(), clone((address,address,address,address,address,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint104,uint104,uint104,(address,address,uint8,uint64,uint64,uint64,uint128)[])), createAssetList((address,address,uint8,uint64,uint64,uint64,uint128)[]), createRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes), decimals(), deploy(address), deployAndUpgradeTo(address,address), depositTransaction(address,uint256,uint64,bool,bytes), getAddress(string), resourceConfig(), sendMessage(address,bytes,uint32), sendMessageToChild(address,bytes), syncState(address,bytes), updateAssetBorrowCollateralFactor(address,address,uint64), upgradeTo(address).
The most important scoring issue is `conflict_detection`, which scored 2/10.
High-risk findings include: Unaccounted trace addresses, Trace complexity exceeds textual complexity disclosure, Claimed actions do not fully match trace actions. Pausing or escalating to manual audit is recommended.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
