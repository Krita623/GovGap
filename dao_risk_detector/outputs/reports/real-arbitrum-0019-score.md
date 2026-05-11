# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:23 UTC
**Proposal ID**: 16288348195459185256236376597446433097934740027053618232242382845767010422421
**Simulation Status**: reverted_with_trace
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

### Addresses Disclosed In Proposal Text
- `0x13f7f24ca959359a4d710d32c715d4bce273c793`
- `0x6491c05a82219b8d1479057361ff1654749b876b`
- `0x72ce9c846789fdb6fc1f34ac4ad25dd9ef7031ef`
- `0x84b9700e28b23f873b82c1beb23d86c091b6079e`
- `0xa3931d71877c0e7a3148cb7eb4463524fec27fbd`
- `0xdc035d45d973e3ec169d2276ddab16f1e407384f`
- `0xddb46999f8891663a8f2828d25298f70416d7610`

### Unaccounted Addresses
- `0x0000000000000000000000000000000000000064`
  - Risk level: HIGH
  - Related actions: sendTxToL1(address,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x34d45e99f7d8c45ed05b5ca72d54bbd1fb3f98f0`
  - Risk level: HIGH
  - Related actions: sendTxToL1(address,bytes)
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
- Actual max depth: 0
- Depth mismatch: no
- Delegatecall count: 0

Summary: Observed trace depth is consistent with the claimed complexity.

---

## Function Semantic Match

- Dimension score: 4/10
- Severity: HIGH
- Summary: Claimed business action categories differ from extracted business actions.
- Claimed actions: parameter_update
- Actual actions: transfer

### Matched Functions
- `sendTxToL1(address,bytes)`

### Unmatched Or Additional Actions
- `transfer`
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
  - Unaccounted addresses: 0x0000000000000000000000000000000000000064, 0x34d45e99f7d8c45ed05b5ca72d54bbd1fb3f98f0

### 2. HIGH - Claimed actions do not fully match trace actions

- **Severity**: HIGH
- **Description**: Claimed business action categories differ from extracted business actions.
- **Evidence Source**: rule_engine
- **Confidence**: 0.9
- **Recommendation**: Compare proposal action wording with decoded functions and risk actions before relying on the text.
- **Key Evidence**:
  - Action comparison: claimed=parameter_update, actual=unable to confirm

---

## Security Conclusion

The proposal has a serious Semantic Gap. Some on-chain actions are not sufficiently covered by the proposal text and may affect governance participants' judgment. Pausing or escalating to manual audit is recommended.

---

## Summary

The proposal text claims: Register the Sky Custom Gateway contracts in the Arbitrum Router to allow bridging USDS and sUSDS through the official Arbitrum Bridge UI.
The payload actually shows: transfer. Decoded functions include: sendTxToL1(address,bytes).
The most important scoring issue is `function_semantic_match`, which scored 4/10.
High-risk findings include: Unaccounted trace addresses, Claimed actions do not fully match trace actions. Pausing or escalating to manual audit is recommended.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
