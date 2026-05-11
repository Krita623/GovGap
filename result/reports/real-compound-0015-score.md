# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:24 UTC
**Proposal ID**: 418
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

- Dimension score: 4/10
- Severity: HIGH
- Summary: An undisclosed address participates in an uncovered high-risk business action.

### Unaccounted Addresses
- `0x16f3532e6af45a2c51b6c77b1267cef34a9cf3b3`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x18084fba666a33d37592fa2633fd49a74dd93a88`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x1933f7e5f8b0423fbab28ce9c8c39c2cc414027b`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x1ad4ceba9f8135a557bbe317db62aa125c330f26`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x1ec63b5883c3481134fd50d5daebc83ecd2e8779`
  - Risk level: HIGH
  - Related actions: upgradeTo(address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x2260fac5e5542a773aa44fbcfedf7c193bc2c599`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x23a982b74a3236a5f2297856d4391b2edbbb5549`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x316f9708bb98af7da9c68c1c3b5e79039cd336e3`
  - Risk level: HIGH
  - Related actions: addAsset(address,(address,address,uint8,uint64,uint64,uint64,uint128)), deploy(address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x31724ca0c982a31fbb5c57f4217ab585271fc9a5`
  - Risk level: HIGH
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x4796d939b22027c2876d5ce9fde52da9ec4e2362`
  - Risk level: HIGH
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x4c22ffd479637ea0ed61d451cbe6355627283358`
  - Risk level: HIGH
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x4e295eac3bf76a1537039a1461bdea4b13272a62`
  - Risk level: HIGH
  - Related actions: contract_creation
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x4f67e4d9bd67efa28236013288737d39aef48e79`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x57a71a9c632b2e6d8b0eb9a157888a3fc87400d1`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x5ecf850c770f78dc7b9f9760672484b2ccaea818`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x60ff20bacd9a647e4025ed8b17ce30e40095a1d2`
  - Risk level: HIGH
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x66f5afdad14b30816b47b707240d1e8e3344d04d`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x680a7937c59b19e2d38b86ef47e9c2e415043ded`
  - Risk level: HIGH
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x6d903f6003cca6255d85cca4d3b5e5146dc33925`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x7458bfdc30034eb860b265e6068121d18fa5aa72`
  - Risk level: HIGH
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x9f2f60f38bbc275af8f88a21c0e2bfe751e97c1f`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xa1290d69c65a6fe4df752f95823fae25cb99e5a7`
  - Risk level: HIGH
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xa17581a9e3356d9a858b789d68b4d866e593ae94`
  - Risk level: HIGH
  - Related actions: upgradeTo(address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xa35b1b31ce002fbf2058d22f30f95d405200a15b`
  - Risk level: HIGH
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xa3a7fb5963d1d69b95eec4957f77678ef073ba08`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xae78736cd615f374d3085123a210448e74fc6393`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xba8f83fffc7097cbcd89fe323d31753cfac33867`
  - Risk level: HIGH
  - Related actions: contract_creation
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xbe9895146f7af43049ca1c1ae358b0541ea49704`
  - Risk level: HIGH
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xbf5495efe5db9ce00f80364c8b423567e58d2110`
  - Risk level: HIGH
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf`
  - Risk level: HIGH
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xcd5fe23c85820f7b72d0926fc9b05b43e359b7ee`
  - Risk level: HIGH
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xcfc1fa6b7ca982176529899d99af6473ad80df4f`
  - Risk level: HIGH
  - Related actions: addAsset(address,(address,address,uint8,uint64,uint64,uint64,uint128)), deploy(address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xd11c452fc99cf405034ee446803b6f6c1f6d5ed8`
  - Risk level: HIGH
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xd1a622566f277aa76c3c47a30469432aaec95e38`
  - Risk level: HIGH
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xd72ac1bce9177cfe7aeb5d0516a38c88a64ce0ab`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xd98be00b5d27fc98112bde293e487f8d4ca57d07`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xdd18688bb75af704f3fb1183e459c4d4d41132d9`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xde43600de5016b50752cc2615332d8ccbed6ec1b`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xe02156874041af6cdf4151e4d8072ac8648477ee`
  - Risk level: HIGH
  - Related actions: contract_creation
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xe629ee84c1bd9ea9c677d2d5391919fcf5e7d5d9`
  - Risk level: HIGH
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xea2a6e7b41505d62d404f927f991edc9e45883c2`
  - Risk level: HIGH
  - Related actions: contract_creation
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xf1c9acdc66974dfb6decb12aa385b9cd01190e38`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xfa454de61b317b6535a0c462267208e8fdb89f45`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xfae103dc9cf190ed75350761e95403b7b8afa6c0`
  - Risk level: HIGH
  - Related actions: decimals()
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
- Actual max depth: 8
- Depth mismatch: yes
- Delegatecall count: 10

Summary: Observed trace depth is moderately deeper than claimed.

### Key Findings
- Trace complexity exceeds textual complexity disclosure
  - Risk level: MEDIUM
  - Description: Observed trace depth is moderately deeper than claimed.
  - Evidence source: trace

---

## Function Semantic Match

- Dimension score: 2/10
- Severity: CRITICAL
- Summary: Text claims a low-risk action while the trace includes a sensitive business action.
- Claimed actions: parameter_update, upgrade
- Actual actions: contract_creation, upgrade

### Matched Functions
- `addAsset(address,(address,address,uint8,uint64,uint64,uint64,uint128))`
- `assetListFactory()`
- `clone((address,address,address,address,address,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint104,uint104,uint104,(address,address,uint8,uint64,uint64,uint64,uint128)[]))`
- `createAssetList((address,address,uint8,uint64,uint64,uint64,uint128)[])`
- `decimals()`
- `deploy(address)`
- `deployAndUpgradeTo(address,address)`
- `upgradeTo(address)`

### Unmatched Or Additional Actions
- `contract_creation`
  - Risk level: CRITICAL
  - Note: this action was not fully matched to the claimed proposal action. Review the linked evidence before relying on the proposal text.

### Key Findings
- Claimed actions do not fully match trace actions
  - Risk level: CRITICAL
  - Description: Text claims a low-risk action while the trace includes a sensitive business action.
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
  - Unaccounted addresses: 0x16f3532e6af45a2c51b6c77b1267cef34a9cf3b3, 0x18084fba666a33d37592fa2633fd49a74dd93a88, 0x1933f7e5f8b0423fbab28ce9c8c39c2cc414027b, 0x1ad4ceba9f8135a557bbe317db62aa125c330f26, 0x1ec63b5883c3481134fd50d5daebc83ecd2e8779, 0x2260fac5e5542a773aa44fbcfedf7c193bc2c599, 0x23a982b74a3236a5f2297856d4391b2edbbb5549, 0x316f9708bb98af7da9c68c1c3b5e79039cd336e3, 0x31724ca0c982a31fbb5c57f4217ab585271fc9a5, 0x4796d939b22027c2876d5ce9fde52da9ec4e2362, 0x4c22ffd479637ea0ed61d451cbe6355627283358, 0x4e295eac3bf76a1537039a1461bdea4b13272a62, 0x4f67e4d9bd67efa28236013288737d39aef48e79, 0x57a71a9c632b2e6d8b0eb9a157888a3fc87400d1, 0x5ecf850c770f78dc7b9f9760672484b2ccaea818, 0x60ff20bacd9a647e4025ed8b17ce30e40095a1d2, 0x66f5afdad14b30816b47b707240d1e8e3344d04d, 0x680a7937c59b19e2d38b86ef47e9c2e415043ded, 0x6d903f6003cca6255d85cca4d3b5e5146dc33925, 0x7458bfdc30034eb860b265e6068121d18fa5aa72, 0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0, 0x9f2f60f38bbc275af8f88a21c0e2bfe751e97c1f, 0xa1290d69c65a6fe4df752f95823fae25cb99e5a7, 0xa17581a9e3356d9a858b789d68b4d866e593ae94, 0xa35b1b31ce002fbf2058d22f30f95d405200a15b, 0xa3a7fb5963d1d69b95eec4957f77678ef073ba08, 0xae78736cd615f374d3085123a210448e74fc6393, 0xba8f83fffc7097cbcd89fe323d31753cfac33867, 0xbe9895146f7af43049ca1c1ae358b0541ea49704, 0xbf5495efe5db9ce00f80364c8b423567e58d2110, 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2, 0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf, 0xcd5fe23c85820f7b72d0926fc9b05b43e359b7ee, 0xcfc1fa6b7ca982176529899d99af6473ad80df4f, 0xd11c452fc99cf405034ee446803b6f6c1f6d5ed8, 0xd1a622566f277aa76c3c47a30469432aaec95e38, 0xd72ac1bce9177cfe7aeb5d0516a38c88a64ce0ab, 0xd98be00b5d27fc98112bde293e487f8d4ca57d07, 0xdd18688bb75af704f3fb1183e459c4d4d41132d9, 0xde43600de5016b50752cc2615332d8ccbed6ec1b, 0xe02156874041af6cdf4151e4d8072ac8648477ee, 0xe629ee84c1bd9ea9c677d2d5391919fcf5e7d5d9, 0xea2a6e7b41505d62d404f927f991edc9e45883c2, 0xf1c9acdc66974dfb6decb12aa385b9cd01190e38, 0xfa454de61b317b6535a0c462267208e8fdb89f45, 0xfae103dc9cf190ed75350761e95403b7b8afa6c0

### 2. MEDIUM - Trace complexity exceeds textual complexity disclosure

- **Severity**: MEDIUM
- **Description**: Observed trace depth is moderately deeper than claimed.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review whether the proposal text should describe the actual call depth or indirect execution paths.
- **Key Evidence**:
  - Complexity: claimed=moderate, actual_max_depth=8

### 3. CRITICAL - Claimed actions do not fully match trace actions

- **Severity**: CRITICAL
- **Description**: Text claims a low-risk action while the trace includes a sensitive business action.
- **Evidence Source**: rule_engine
- **Confidence**: 0.9
- **Recommendation**: Compare proposal action wording with decoded functions and risk actions before relying on the text.
- **Key Evidence**:
  - Action comparison: claimed=parameter_update, upgrade, actual=unable to confirm

---

## Security Conclusion

The proposal has a critical Semantic Gap or potential attack indicators. The textual commitment and observed on-chain behavior are severely inconsistent. Do not execute without immediate manual security review.

---

## Summary

The proposal text claims: Compound Growth Program (AlphaGrowth) proposes to add tETH as collateral into the cWETHv3 market on the Ethereum network, alongside upgrading Comet to a new version.
The payload actually shows: contract_creation, upgrade. Decoded functions include: addAsset(address,(address,address,uint8,uint64,uint64,uint64,uint128)), assetListFactory(), clone((address,address,address,address,address,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint104,uint104,uint104,(address,address,uint8,uint64,uint64,uint64,uint128)[])), createAssetList((address,address,uint8,uint64,uint64,uint64,uint128)[]), decimals(), deploy(address), deployAndUpgradeTo(address,address), upgradeTo(address).
The most important scoring issue is `function_semantic_match`, which scored 2/10.
High-risk findings include: Unaccounted trace addresses, Claimed actions do not fully match trace actions. Pausing or escalating to manual audit is recommended.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
