# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:24 UTC
**Proposal ID**: 20404686300257550242704646761273386459664655640264490428281621095220078268383
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
- `0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48`

### Unaccounted Addresses
- `0x1ba8603da702602a8657980e825a6daa03dee93a`
  - Risk level: CRITICAL
  - Related actions: getAgreementData(address,bytes32,uint256), transferFrom(address,address,uint256), upgrade(uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x2844c1bbda121e9e43105630b9c8310e5c72744b`
  - Risk level: CRITICAL
  - Related actions: getFlow(address,address,address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x43506849d7c04f9138d1a2050bbf3a0c054402dd`
  - Risk level: CRITICAL
  - Related actions: approve(address,uint256), balanceOf(address), transferFrom(address,address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xbfc8c07468aeea87a0a1d30a23804cf4fd73eff1`
  - Risk level: CRITICAL
  - Related actions: getFlow(address,address,address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xcfa132e353cb4e398080b9700609bb008eceb125`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xf0d7d1d47109ba426b9d8a3cde1941327af1eea3`
  - Risk level: CRITICAL
  - Related actions: getAgreementData(address,bytes32,uint256), upgrade(uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xfe89cc7abb2c4183683ab71653c4cdc9b02d44b7`
  - Risk level: CRITICAL
  - Related actions: approve(address,uint256)
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
- Actual max depth: 4
- Depth mismatch: no
- Delegatecall count: 7

Summary: Observed trace depth is consistent with the claimed complexity.

---

## Function Semantic Match

- Dimension score: 2/10
- Severity: CRITICAL
- Summary: Text claims a low-risk action while the trace includes a sensitive business action.
- Claimed actions: treasury_operation
- Actual actions: approval, parameter_update, transfer, upgrade

### Matched Functions
- `approve(address,uint256)`
- `balanceOf(address)`
- `getAgreementData(address,bytes32,uint256)`
- `getFlow(address,address,address)`
- `setFlowrate(address,address,int96)`
- `transferFrom(address,address,uint256)`
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
  - Unaccounted addresses: 0x1ba8603da702602a8657980e825a6daa03dee93a, 0x2844c1bbda121e9e43105630b9c8310e5c72744b, 0x43506849d7c04f9138d1a2050bbf3a0c054402dd, 0xbfc8c07468aeea87a0a1d30a23804cf4fd73eff1, 0xcfa132e353cb4e398080b9700609bb008eceb125, 0xf0d7d1d47109ba426b9d8a3cde1941327af1eea3, 0xfe89cc7abb2c4183683ab71653c4cdc9b02d44b7

### 2. CRITICAL - Claimed actions do not fully match trace actions

- **Severity**: CRITICAL
- **Description**: Text claims a low-risk action while the trace includes a sensitive business action.
- **Evidence Source**: rule_engine
- **Confidence**: 0.9
- **Recommendation**: Compare proposal action wording with decoded functions and risk actions before relying on the text.
- **Key Evidence**:
  - Action comparison: claimed=treasury_operation, actual=unable to confirm

---

## Security Conclusion

The proposal has a critical Semantic Gap or potential attack indicators. The textual commitment and observed on-chain behavior are severely inconsistent. Do not execute without immediate manual security review.

---

## Summary

The proposal text claims: This proposal implements the Service Provider Program Season 2 (SPP2), increasing the annual budget to $4.5M to support 8 providers. It adjusts the Superfluid streaming infrastructure, provides 375,000 USDC in initial funding, and configures autowrap parameters.
The payload actually shows: approval, parameter_update, transfer, upgrade. Decoded functions include: approve(address,uint256), balanceOf(address), getAgreementData(address,bytes32,uint256), getFlow(address,address,address), setFlowrate(address,address,int96), transferFrom(address,address,uint256), upgrade(uint256).
The most important scoring issue is `conflict_detection`, which scored 2/10.
High-risk findings include: Unaccounted trace addresses, Claimed actions do not fully match trace actions. Pausing or escalating to manual audit is recommended.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
