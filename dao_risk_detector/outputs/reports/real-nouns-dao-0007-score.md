# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:24 UTC
**Proposal ID**: 435
**Simulation Status**: success
**Trace Source**: simulated_trace

---

## Consistency Score

**Overall Score**: 8/10
**Risk Level**: LOW
**Scoring Method**: worst-case risk gating, not weighted average.

Overall score uses minimum dimension score 8 capped by highest severity LOW.

---

## Conflict Detection

- Dimension score: 8/10
- Severity: LOW
- Summary: Execution includes undisclosed path components, but core business actions match proposal text.

### Unaccounted Addresses
- `0x34761eb1bda821ed7b30b51d7fbabbe18fd7574b`
  - Risk level: LOW
  - Related actions: delegatecall
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x44d97d22b3d37d837ce4b22773aad9d1566055d9`
  - Risk level: LOW
  - Related actions: transferFrom(address,address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x6f3e6272a167e8accb32072d08e0957f9c79223d`
  - Risk level: LOW
  - Related actions: delegatecall, withdrawDAONounsFromEscrowToTreasury(uint256[])
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x9c8ff314c9bc7f6e59a9d9225fb22946427edc03`
  - Risk level: LOW
  - Related actions: transferFrom(address,address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xb1a32fc9f9d8b2cf86c068cae13108809547ef71`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xdd1492570beb290a2f309541e1fddcaaa3f00b61`
  - Risk level: LOW
  - Related actions: withdrawDAONounsFromEscrowToTreasury(uint256[])
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.

### Key Findings
- Unaccounted trace addresses
  - Risk level: LOW
  - Description: One or more addresses appeared in the trace without direct proposal text disclosure.
  - Evidence source: trace

---

## Depth Analysis

- Claimed complexity: simple
- Actual max depth: 4
- Depth mismatch: yes
- Delegatecall count: 2

Summary: Core business actions match proposal text; observed wrapper depth is within a normal review range.

---

## Function Semantic Match

- Dimension score: 9/10
- Severity: LOW
- Summary: Claimed business actions match; extra execution wrappers are present but do not create a business-action mismatch.
- Claimed actions: treasury_operation
- Actual actions: transfer

### Matched Functions
- `transferFrom(address,address,uint256)`
- `withdrawDAONounsFromEscrowToTreasury(uint256[])`
- `withdrawTokens(uint256[],address)`

---

## Potential Risk Findings

### 1. LOW - Unaccounted trace addresses

- **Severity**: LOW
- **Description**: One or more addresses appeared in the trace without direct proposal text disclosure.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review undisclosed execution path components, but prioritize whether the core business action remains covered by proposal text.
- **Key Evidence**:
  - Unaccounted addresses: 0x34761eb1bda821ed7b30b51d7fbabbe18fd7574b, 0x44d97d22b3d37d837ce4b22773aad9d1566055d9, 0x6f3e6272a167e8accb32072d08e0957f9c79223d, 0x9c8ff314c9bc7f6e59a9d9225fb22946427edc03, 0xb1a32fc9f9d8b2cf86c068cae13108809547ef71, 0xdd1492570beb290a2f309541e1fddcaaa3f00b61

---

## Security Conclusion

The proposal text and the observed payload effects are broadly consistent. No clear Semantic Gap was found. Reviewers should still manually review any low-risk undisclosed addresses or unknown selectors.

---

## Summary

The proposal text claims: Proposal to withdraw Noun 181 (Sasquatch) from the escrow contract back to the DAO treasury so that Proposal 428 can be successfully executed.
The payload actually shows: transfer. Decoded functions include: transferFrom(address,address,uint256), withdrawDAONounsFromEscrowToTreasury(uint256[]), withdrawTokens(uint256[],address).
The most important scoring issue is `conflict_detection`, which scored 8/10.
No HIGH or CRITICAL finding was generated. Unknown or unclear fields should still be manually reviewed.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
