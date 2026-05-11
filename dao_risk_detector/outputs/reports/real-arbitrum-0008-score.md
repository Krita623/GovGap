# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:23 UTC
**Proposal ID**: 98446466630612736687159241204141593794174501692677162686607521796118942563659
**Simulation Status**: success
**Trace Source**: simulated_trace

---

## Consistency Score

**Overall Score**: 4/10
**Risk Level**: HIGH
**Scoring Method**: worst-case risk gating, not weighted average.

Overall score uses minimum dimension score 5 capped by highest severity HIGH.

Some dimensions may be acceptable, but the overall score is limited by High or Critical rule-engine findings.

---

## Conflict Detection

- Dimension score: 5/10
- Severity: HIGH
- Summary: An undisclosed address participates in an uncovered approval or transfer action.

### Unaccounted Addresses
- `0x912ce59144191c1204e64559fe8253a0e49e6548`
  - Risk level: HIGH
  - Related actions: transfer(address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x9f43ab02cacc8e709b05936a92dc85b76d1523c4`
  - Risk level: HIGH
  - Related actions: transfer(address,address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xbfc1feca8b09a5c5d3effe7429ebe24b9c09ef58`
  - Risk level: HIGH
  - Related actions: transfer(address,address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xc4ed0a9ea70d5bcc69f748547650d32cc219d882`
  - Risk level: HIGH
  - Related actions: transfer(address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xf3fc178157fb3c87548baa86f9d24ba38e649b58`
  - Risk level: HIGH
  - Related actions: transfer(address,address,uint256), transfer(address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.

### Key Findings
- Unaccounted trace addresses
  - Risk level: HIGH
  - Description: One or more addresses appeared in the trace without direct proposal text disclosure.
  - Evidence source: trace

---

## Depth Analysis

- Claimed complexity: unable to confirm
- Actual max depth: 3
- Depth mismatch: no
- Delegatecall count: 2

Summary: Text complexity is unknown; observed trace depth is low to moderate.

---

## Function Semantic Match

- Dimension score: 6/10
- Severity: MEDIUM
- Summary: Proposal text does not disclose canonical business actions; extracted actions need review.
- Claimed actions: unable to confirm
- Actual actions: transfer

### Matched Functions
- `transfer(address,address,uint256)`
- `transfer(address,uint256)`

### Unmatched Or Additional Actions
- `transfer`
  - Risk level: MEDIUM
  - Note: this action was not fully matched to the claimed proposal action. Review the linked evidence before relying on the proposal text.

### Key Findings
- Claimed actions do not fully match trace actions
  - Risk level: MEDIUM
  - Description: Proposal text does not disclose canonical business actions; extracted actions need review.
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
  - Unaccounted addresses: 0x912ce59144191c1204e64559fe8253a0e49e6548, 0x9f43ab02cacc8e709b05936a92dc85b76d1523c4, 0xbfc1feca8b09a5c5d3effe7429ebe24b9c09ef58, 0xc4ed0a9ea70d5bcc69f748547650d32cc219d882, 0xf3fc178157fb3c87548baa86f9d24ba38e649b58

### 2. MEDIUM - Claimed actions do not fully match trace actions

- **Severity**: MEDIUM
- **Description**: Proposal text does not disclose canonical business actions; extracted actions need review.
- **Evidence Source**: rule_engine
- **Confidence**: 0.9
- **Recommendation**: Compare proposal action wording with decoded functions and risk actions before relying on the text.
- **Key Evidence**:
  - Action comparison: claimed=unable to confirm, actual=unable to confirm

---

## Security Conclusion

The proposal has a serious Semantic Gap. Some on-chain actions are not sufficiently covered by the proposal text and may affect governance participants' judgment. Pausing or escalating to manual audit is recommended.

---

## Summary

The proposal text claims: No data provided due to rate limit error.
The payload actually shows: transfer. Decoded functions include: transfer(address,address,uint256), transfer(address,uint256).
The most important scoring issue is `conflict_detection`, which scored 5/10.
High-risk findings include: Unaccounted trace addresses. Pausing or escalating to manual audit is recommended.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
