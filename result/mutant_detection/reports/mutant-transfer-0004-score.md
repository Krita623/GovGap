# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-11 05:58:42 UTC
**Proposal ID**: mutant-transfer-0004
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

### Addresses Disclosed In Proposal Text
- `0x1000000000000000000000000000000000000001`

### Unaccounted Addresses
- `0x3000000000000000000000000000000000000004`
  - Risk level: HIGH
  - Related actions: transfer(address,uint256)
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
- Claimed actions: maintenance
- Actual actions: transfer

### Matched Functions
- `transfer(address,uint256)`

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
  - Unaccounted addresses: 0x3000000000000000000000000000000000000004

### 2. HIGH - Claimed actions do not fully match trace actions

- **Severity**: HIGH
- **Description**: Claimed business action categories differ from extracted business actions.
- **Evidence Source**: rule_engine
- **Confidence**: 0.9
- **Recommendation**: Compare proposal action wording with decoded functions and risk actions before relying on the text.
- **Key Evidence**:
  - Action comparison: claimed=maintenance, actual=unable to confirm

---

## Security Conclusion

The proposal has a serious Semantic Gap. Some on-chain actions are not sufficiently covered by the proposal text and may affect governance participants' judgment. Pausing or escalating to manual audit is recommended.

---

## Summary

The proposal text claims: This proposal refreshes accounting records and does not mention token movement.
The payload actually shows: transfer. Decoded functions include: transfer(address,uint256).
The most important scoring issue is `function_semantic_match`, which scored 4/10.
High-risk findings include: Unaccounted trace addresses, Claimed actions do not fully match trace actions. Pausing or escalating to manual audit is recommended.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
