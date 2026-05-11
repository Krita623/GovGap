# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:24 UTC
**Proposal ID**: 412
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
- `0x0fd206fc7a7dbcd5661157edcb1ffdd0d02a61ff`
  - Risk level: HIGH
  - Related actions: contract_creation
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x20bc977ffadf2b1b07b4eb9bcf214ead5edaa05d`
  - Risk level: HIGH
  - Related actions: transfer
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xb1a32fc9f9d8b2cf86c068cae13108809547ef71`
  - Risk level: HIGH
  - Related actions: deposit(), transfer, transfer(address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2`
  - Risk level: HIGH
  - Related actions: deposit(), transfer(address,uint256)
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
- Actual max depth: 1
- Depth mismatch: no
- Delegatecall count: 0

Summary: Observed trace depth is consistent with the claimed complexity.

---

## Function Semantic Match

- Dimension score: 2/10
- Severity: CRITICAL
- Summary: Text claims a low-risk action while the trace includes a sensitive business action.
- Claimed actions: treasury_operation, treasury_operation, treasury_operation
- Actual actions: contract_creation, transfer

### Matched Functions
- `createStream(address,uint256,address,uint256,uint256,uint8,address)`
- `deposit()`
- `transfer(address,uint256)`

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
  - Unaccounted addresses: 0x0fd206fc7a7dbcd5661157edcb1ffdd0d02a61ff, 0x20bc977ffadf2b1b07b4eb9bcf214ead5edaa05d, 0xb1a32fc9f9d8b2cf86c068cae13108809547ef71, 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2

### 2. CRITICAL - Claimed actions do not fully match trace actions

- **Severity**: CRITICAL
- **Description**: Text claims a low-risk action while the trace includes a sensitive business action.
- **Evidence Source**: rule_engine
- **Confidence**: 0.9
- **Recommendation**: Compare proposal action wording with decoded functions and risk actions before relying on the text.
- **Key Evidence**:
  - Action comparison: claimed=treasury_operation, treasury_operation, treasury_operation, actual=unable to confirm

---

## Security Conclusion

The proposal has a critical Semantic Gap or potential attack indicators. The textual commitment and observed on-chain behavior are severely inconsistent. Do not execute without immediate manual security review.

---

## Summary

The proposal text claims: Funding request for 3 months to develop Propdates 2.0, a tool for tracking proposal updates and successes, totaling 37 ETH.
The payload actually shows: contract_creation, transfer. Decoded functions include: createStream(address,uint256,address,uint256,uint256,uint8,address), deposit(), transfer(address,uint256).
The most important scoring issue is `function_semantic_match`, which scored 2/10.
High-risk findings include: Unaccounted trace addresses, Claimed actions do not fully match trace actions. Pausing or escalating to manual audit is recommended.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
