# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:23 UTC
**Proposal ID**: 176
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
- `0x1ec63b5883c3481134fd50d5daebc83ecd2e8779`
  - Risk level: CRITICAL
  - Related actions: upgradeTo(address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x23a982b74a3236a5f2297856d4391b2edbbb5549`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x316f9708bb98af7da9c68c1c3b5e79039cd336e3`
  - Risk level: CRITICAL
  - Related actions: deploy(address), setBaseTrackingSupplySpeed(address,uint64), setBorrowPerYearInterestRateSlopeLow(address,uint64), setStoreFrontPriceFactor(address,uint64), updateAssetLiquidationFactor(address,address,uint64)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x31724ca0c982a31fbb5c57f4217ab585271fc9a5`
  - Risk level: CRITICAL
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x4f67e4d9bd67efa28236013288737d39aef48e79`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x6d903f6003cca6255d85cca4d3b5e5146dc33925`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x7a1316220a46dce22fd5c6d55a39513367e6c967`
  - Risk level: CRITICAL
  - Related actions: contract_creation
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xa17581a9e3356d9a858b789d68b4d866e593ae94`
  - Risk level: CRITICAL
  - Related actions: upgradeTo(address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xa7f7de6ccad4d83d81676717053883337ac2c1b4`
  - Risk level: CRITICAL
  - Related actions: contract_creation
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xbe9895146f7af43049ca1c1ae358b0541ea49704`
  - Risk level: CRITICAL
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xcfc1fa6b7ca982176529899d99af6473ad80df4f`
  - Risk level: CRITICAL
  - Related actions: deploy(address), setBaseTrackingSupplySpeed(address,uint64), setBorrowPerYearInterestRateSlopeLow(address,uint64), setStoreFrontPriceFactor(address,uint64), updateAssetLiquidationFactor(address,address,uint64)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xd72ac1bce9177cfe7aeb5d0516a38c88a64ce0ab`
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
- Actual max depth: 6
- Depth mismatch: yes
- Delegatecall count: 7

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
- Claimed actions: parameter_update, parameter_update, parameter_update, parameter_update, parameter_update
- Actual actions: contract_creation, parameter_update, upgrade

### Matched Functions
- `clone((address,address,address,address,address,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint104,uint104,uint104,(address,address,uint8,uint64,uint64,uint64,uint128)[]))`
- `decimals()`
- `deploy(address)`
- `deployAndUpgradeTo(address,address)`
- `setBaseTrackingSupplySpeed(address,uint64)`
- `setBorrowPerYearInterestRateSlopeLow(address,uint64)`
- `setStoreFrontPriceFactor(address,uint64)`
- `updateAssetLiquidationFactor(address,address,uint64)`
- `upgradeTo(address)`

### Unmatched Or Additional Actions
- `contract_creation`
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
  - Unaccounted addresses: 0x1ec63b5883c3481134fd50d5daebc83ecd2e8779, 0x23a982b74a3236a5f2297856d4391b2edbbb5549, 0x316f9708bb98af7da9c68c1c3b5e79039cd336e3, 0x31724ca0c982a31fbb5c57f4217ab585271fc9a5, 0x4f67e4d9bd67efa28236013288737d39aef48e79, 0x6d903f6003cca6255d85cca4d3b5e5146dc33925, 0x7a1316220a46dce22fd5c6d55a39513367e6c967, 0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0, 0xa17581a9e3356d9a858b789d68b4d866e593ae94, 0xa7f7de6ccad4d83d81676717053883337ac2c1b4, 0xbe9895146f7af43049ca1c1ae358b0541ea49704, 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2, 0xcfc1fa6b7ca982176529899d99af6473ad80df4f, 0xd72ac1bce9177cfe7aeb5d0516a38c88a64ce0ab

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
  - Action comparison: claimed=parameter_update, parameter_update, parameter_update, parameter_update, parameter_update, actual=unable to confirm

---

## Security Conclusion

The proposal has a critical Semantic Gap or potential attack indicators. The textual commitment and observed on-chain behavior are severely inconsistent. Do not execute without immediate manual security review.

---

## Summary

The proposal text claims: A proposal by Gauntlet to adjust risk parameters, an interest rate curve parameter, and an incentive parameter for Ethereum Compound v3 WETH to stimulate growth.
The payload actually shows: contract_creation, parameter_update, upgrade. Decoded functions include: clone((address,address,address,address,address,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint104,uint104,uint104,(address,address,uint8,uint64,uint64,uint64,uint128)[])), decimals(), deploy(address), deployAndUpgradeTo(address,address), setBaseTrackingSupplySpeed(address,uint64), setBorrowPerYearInterestRateSlopeLow(address,uint64), setStoreFrontPriceFactor(address,uint64), updateAssetLiquidationFactor(address,address,uint64), upgradeTo(address).
The most important scoring issue is `conflict_detection`, which scored 2/10.
High-risk findings include: Unaccounted trace addresses, Trace complexity exceeds textual complexity disclosure, Claimed actions do not fully match trace actions. Pausing or escalating to manual audit is recommended.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
