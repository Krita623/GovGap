# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:23 UTC
**Proposal ID**: 35
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
- `0x1b669d5034143e272b5ff548f2878735a2f3505a`
- `0x1ddcf68f4c2600cbe534212765f964342a2faf02`
- `0x956f47f50a910163d8bf957cf5846d573e7f87ca`
- `0xacf35af93a65904c50ed93dfb010baadebb4ccf0`
- `0xdee5c1662bbff8f80f7c572d8091bf251b3b0dab`
- `0xf0ba2a8c12a2354c075b363765eae825619bd490`
- `0xff865335401f12b88fa3ff5a3a51685a7f224191`

### Unaccounted Addresses
- `0x246ca67522df5895cd6cf8807ec161954ea1ba61`
  - Risk level: CRITICAL
  - Related actions: initReserve(address,address,address,uint8,address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x311bb771e4f8952e6da169b425e7e92d6ac45756`
  - Risk level: CRITICAL
  - Related actions: initReserve(address,address,address,uint8,address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xb53c1a33016b2dc2ff3653530bff1848a515c8c5`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xe775a3a0a1cdc50bd48d5f47c442a0a4f5f24473`
  - Risk level: CRITICAL
  - Related actions: execute(address,address,address,address,address,uint256,uint256,uint256,uint256,uint8,bool,bool,bool)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xec568fffba86c094cf06b22134b23074dfe2252c`
  - Risk level: CRITICAL
  - Related actions: execute(address,address,address,address,address,uint256,uint256,uint256,uint256,uint8,bool,bool,bool)
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
- Actual max depth: 3
- Depth mismatch: no
- Delegatecall count: 1

Summary: Observed trace depth is consistent with the claimed complexity.

---

## Function Semantic Match

- Dimension score: 2/10
- Severity: CRITICAL
- Summary: Text claims a low-risk action while the trace includes a sensitive business action.
- Claimed actions: parameter_update
- Actual actions: arbitrary_call

### Matched Functions
- `UNDERLYING_ASSET_ADDRESS()`
- `execute(address,address,address,address,address,uint256,uint256,uint256,uint256,uint8,bool,bool,bool)`
- `getLendingPoolConfigurator()`
- `getPoolAdmin()`
- `initReserve(address,address,address,uint8,address)`

### Unmatched Or Additional Actions
- `arbitrary_call`
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
  - Unaccounted addresses: 0x246ca67522df5895cd6cf8807ec161954ea1ba61, 0x311bb771e4f8952e6da169b425e7e92d6ac45756, 0xb53c1a33016b2dc2ff3653530bff1848a515c8c5, 0xe775a3a0a1cdc50bd48d5f47c442a0a4f5f24473, 0xec568fffba86c094cf06b22134b23074dfe2252c

### 2. CRITICAL - Claimed actions do not fully match trace actions

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

The proposal text claims: Add the FEI stablecoin as a borrowable (but not collateral) asset on Aave V2.
The payload actually shows: arbitrary_call. Decoded functions include: UNDERLYING_ASSET_ADDRESS(), execute(address,address,address,address,address,uint256,uint256,uint256,uint256,uint8,bool,bool,bool), getLendingPoolConfigurator(), getPoolAdmin(), initReserve(address,address,address,uint8,address).
The most important scoring issue is `conflict_detection`, which scored 2/10.
High-risk findings include: Unaccounted trace addresses, Claimed actions do not fully match trace actions. Pausing or escalating to manual audit is recommended.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
