# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:24 UTC
**Proposal ID**: 545
**Simulation Status**: reverted_with_trace
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
- `0x12875aed495cd573433f0c93d538c0ccc9e2b8fa`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x334791289a906ac8f96ac0f90e7a91bf4aae4a60`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x36a0eb84154797dadceacfd046785db31094c308`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x3d6eef6a92b15361697698695334e98c5db91d6b`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x43506849d7c04f9138d1a2050bbf3a0c054402dd`
  - Risk level: HIGH
  - Related actions: transfer(address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x6d903f6003cca6255d85cca4d3b5e5146dc33925`
  - Risk level: HIGH
  - Related actions: transfer(address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x72bf2d7b05152ef282805f3e38752c436d94e4af`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x8624f61cc6e5a86790e173712afdd480fa8b73ba`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x8fffffd4afb6115b954bd326cbe7b4ba576818f6`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x96a0029c945898de1072ea8f33aa88b7fde3b125`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48`
  - Risk level: HIGH
  - Related actions: transfer(address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xaf9cee006ae377e88f3bbd668e3d67807f546bd8`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xba3cdb9d5c2119137126989f81edaea8b50331d2`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xc00e94cb662c3520282e6f5717214004a7f26888`
  - Risk level: HIGH
  - Related actions: transfer(address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xc3d688b66703497daa19211eedff47f25384cdc3`
  - Risk level: HIGH
  - Related actions: transfer(address,uint256), withdrawTo(address,address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xc9e1a09622afdb659913fefe800feae5dbbfe9d7`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xe9c21ebc3815cdfbe07f721126d3cb46407fd79a`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xea2b6bc719cf6d2fed07865d26987d32d570dbbd`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xf088339dd8e79819a41add5ffb75d9f245afaab1`
  - Risk level: HIGH
  - Related actions: transfer(address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xfe36a00669bb4b5834a2f3e2b9a2908fee21d141`
  - Risk level: HIGH
  - Related actions: withdrawTo(address,address,uint256)
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
- Actual max depth: 4
- Depth mismatch: no
- Delegatecall count: 8

Summary: Text complexity is unknown; observed trace depth is low to moderate.

---

## Function Semantic Match

- Dimension score: 6/10
- Severity: MEDIUM
- Summary: Proposal text does not disclose canonical business actions; extracted actions need review.
- Claimed actions: unable to confirm
- Actual actions: transfer

### Matched Functions
- `balanceOf(address)`
- `execute((address,uint256,bytes))`
- `initialize()`
- `latestRoundData()`
- `sweepRemaining()`
- `terminateStream(uint256)`
- `transfer(address,uint256)`
- `withdrawTo(address,address,uint256)`

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
  - Unaccounted addresses: 0x12875aed495cd573433f0c93d538c0ccc9e2b8fa, 0x334791289a906ac8f96ac0f90e7a91bf4aae4a60, 0x36a0eb84154797dadceacfd046785db31094c308, 0x3d6eef6a92b15361697698695334e98c5db91d6b, 0x43506849d7c04f9138d1a2050bbf3a0c054402dd, 0x6d903f6003cca6255d85cca4d3b5e5146dc33925, 0x72bf2d7b05152ef282805f3e38752c436d94e4af, 0x8624f61cc6e5a86790e173712afdd480fa8b73ba, 0x8fffffd4afb6115b954bd326cbe7b4ba576818f6, 0x96a0029c945898de1072ea8f33aa88b7fde3b125, 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48, 0xaf9cee006ae377e88f3bbd668e3d67807f546bd8, 0xba3cdb9d5c2119137126989f81edaea8b50331d2, 0xc00e94cb662c3520282e6f5717214004a7f26888, 0xc3d688b66703497daa19211eedff47f25384cdc3, 0xc9e1a09622afdb659913fefe800feae5dbbfe9d7, 0xe9c21ebc3815cdfbe07f721126d3cb46407fd79a, 0xea2b6bc719cf6d2fed07865d26987d32d570dbbd, 0xf088339dd8e79819a41add5ffb75d9f245afaab1, 0xfe36a00669bb4b5834a2f3e2b9a2908fee21d141

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

The proposal text claims: Empty proposal text provided, only placeholder headings.
The payload actually shows: transfer. Decoded functions include: balanceOf(address), execute((address,uint256,bytes)), initialize(), latestRoundData(), sweepRemaining(), terminateStream(uint256), transfer(address,uint256), withdrawTo(address,address,uint256).
The most important scoring issue is `conflict_detection`, which scored 5/10.
High-risk findings include: Unaccounted trace addresses. Pausing or escalating to manual audit is recommended.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
