# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:23 UTC
**Proposal ID**: 51
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

- Dimension score: 7/10
- Severity: MEDIUM
- Summary: Trace includes undisclosed addresses without evidence of an uncovered sensitive business action.

### Unaccounted Addresses
- `0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b`
  - Risk level: MEDIUM
  - Related actions: _setContributorCompSpeed(address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x6d903f6003cca6255d85cca4d3b5e5146dc33925`
  - Risk level: MEDIUM
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x75442ac771a7243433e033f3f8eab2631e22938f`
  - Risk level: MEDIUM
  - Related actions: _setContributorCompSpeed(address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.

### Key Findings
- Unaccounted trace addresses
  - Risk level: MEDIUM
  - Description: One or more addresses appeared in the trace without direct proposal text disclosure.
  - Evidence source: trace

---

## Depth Analysis

- Claimed complexity: simple
- Actual max depth: 1
- Depth mismatch: no
- Delegatecall count: 1

Summary: Observed trace depth is consistent with the claimed complexity.

---

## Function Semantic Match

- Dimension score: 4/10
- Severity: HIGH
- Summary: Claimed business action categories differ from extracted business actions.
- Claimed actions: treasury_operation
- Actual actions: parameter_update

### Matched Functions
- `_setContributorCompSpeed(address,uint256)`

### Unmatched Or Additional Actions
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

### 1. MEDIUM - Unaccounted trace addresses

- **Severity**: MEDIUM
- **Description**: One or more addresses appeared in the trace without direct proposal text disclosure.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review undisclosed execution path components, but prioritize whether the core business action remains covered by proposal text.
- **Key Evidence**:
  - Unaccounted addresses: 0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b, 0x6d903f6003cca6255d85cca4d3b5e5146dc33925, 0x75442ac771a7243433e033f3f8eab2631e22938f

### 2. HIGH - Claimed actions do not fully match trace actions

- **Severity**: HIGH
- **Description**: Claimed business action categories differ from extracted business actions.
- **Evidence Source**: rule_engine
- **Confidence**: 0.9
- **Recommendation**: Compare proposal action wording with decoded functions and risk actions before relying on the text.
- **Key Evidence**:
  - Action comparison: claimed=treasury_operation, actual=unable to confirm

---

## Security Conclusion

The proposal has a serious Semantic Gap. Some on-chain actions are not sufficiently covered by the proposal text and may affect governance participants' judgment. Pausing or escalating to manual audit is recommended.

---

## Summary

The proposal text claims: A proposal to create a streaming COMP grant (0.000214 Contributor Comp Speed) for Getty Hill to compensate for past and future work on coordinating and improving Compound's oracle system.
The payload actually shows: parameter_update. Decoded functions include: _setContributorCompSpeed(address,uint256).
The most important scoring issue is `function_semantic_match`, which scored 4/10.
High-risk findings include: Claimed actions do not fully match trace actions. Pausing or escalating to manual audit is recommended.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
