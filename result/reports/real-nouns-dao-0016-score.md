# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:24 UTC
**Proposal ID**: 795
**Simulation Status**: success
**Trace Source**: simulated_trace

---

## Consistency Score

**Overall Score**: 3/10
**Risk Level**: HIGH
**Scoring Method**: worst-case risk gating, not weighted average.

Overall score uses minimum dimension score 3 capped by highest severity HIGH.

Some dimensions may be acceptable, but the overall score is limited by High or Critical rule-engine findings.

---

## Conflict Detection

- Dimension score: 4/10
- Severity: HIGH
- Summary: An undisclosed address participates in an uncovered high-risk business action.

### Addresses Disclosed In Proposal Text
- `0x0b276e727b3c09545593c484966138a11b1a32e7`

### Unaccounted Addresses
- `0x0b9dff1aba32a9fa95011c7f097ec672f689038f`
  - Risk level: HIGH
  - Related actions: initialize()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x0fd206fc7a7dbcd5661157edcb1ffdd0d02a61ff`
  - Risk level: HIGH
  - Related actions: contract_creation
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x43506849d7c04f9138d1a2050bbf3a0c054402dd`
  - Risk level: HIGH
  - Related actions: balanceOf(address), transfer(address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x948da71e0d4322ef249de7a6a08de9f486d12612`
  - Risk level: HIGH
  - Related actions: contract_creation, initialize()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x9c8ff314c9bc7f6e59a9d9225fb22946427edc03`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48`
  - Risk level: HIGH
  - Related actions: balanceOf(address), transfer(address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xb1a32fc9f9d8b2cf86c068cae13108809547ef71`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xd97bcd9f47cee35c0a9ec1dc40c1269afc9e8e1d`
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
- Actual max depth: 2
- Depth mismatch: no
- Delegatecall count: 5

Summary: Observed trace depth is consistent with the claimed complexity.

---

## Function Semantic Match

- Dimension score: 3/10
- Severity: HIGH
- Summary: Trace includes an unclaimed high-risk business action.
- Claimed actions: transfer, transfer, transfer
- Actual actions: contract_creation, transfer

### Matched Functions
- `balanceOf(address)`
- `createStream(address,uint256,address,uint256,uint256,uint8,address)`
- `initialize()`
- `safeTransferFrom(address,address,uint256)`
- `sendOrRegisterDebt(address,uint256)`
- `transfer(address,uint256)`

### Unmatched Or Additional Actions
- `contract_creation`
  - Risk level: HIGH
  - Note: this action was not fully matched to the claimed proposal action. Review the linked evidence before relying on the proposal text.

### Key Findings
- Claimed actions do not fully match trace actions
  - Risk level: HIGH
  - Description: Trace includes an unclaimed high-risk business action.
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
  - Unaccounted addresses: 0x0b9dff1aba32a9fa95011c7f097ec672f689038f, 0x0fd206fc7a7dbcd5661157edcb1ffdd0d02a61ff, 0x43506849d7c04f9138d1a2050bbf3a0c054402dd, 0x948da71e0d4322ef249de7a6a08de9f486d12612, 0x9c8ff314c9bc7f6e59a9d9225fb22946427edc03, 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48, 0xb1a32fc9f9d8b2cf86c068cae13108809547ef71, 0xd97bcd9f47cee35c0a9ec1dc40c1269afc9e8e1d

### 2. HIGH - Claimed actions do not fully match trace actions

- **Severity**: HIGH
- **Description**: Trace includes an unclaimed high-risk business action.
- **Evidence Source**: rule_engine
- **Confidence**: 0.9
- **Recommendation**: Compare proposal action wording with decoded functions and risk actions before relying on the text.
- **Key Evidence**:
  - Action comparison: claimed=transfer, transfer, transfer, actual=unable to confirm

---

## Security Conclusion

The proposal has a serious Semantic Gap. Some on-chain actions are not sufficiently covered by the proposal text and may affect governance participants' judgment. Pausing or escalating to manual audit is recommended.

---

## Summary

The proposal text claims: A proposal to fund volky.eth $18k streamed over 3 months to revamp nouns.wtf and dev tooling, retroactive compensation of 1 Noun for past work, and $2k to seed a bounty program managed by a 2/3 multisig.
The payload actually shows: contract_creation, transfer. Decoded functions include: balanceOf(address), createStream(address,uint256,address,uint256,uint256,uint8,address), initialize(), safeTransferFrom(address,address,uint256), sendOrRegisterDebt(address,uint256), transfer(address,uint256).
The most important scoring issue is `function_semantic_match`, which scored 3/10.
High-risk findings include: Unaccounted trace addresses, Claimed actions do not fully match trace actions. Pausing or escalating to manual audit is recommended.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
