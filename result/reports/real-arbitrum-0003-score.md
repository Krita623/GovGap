# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:23 UTC
**Proposal ID**: 4339452689891418965907083940091891085726910948106830138993485564953310970308
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
- `0x912ce59144191c1204e64559fe8253a0e49e6548`
  - Risk level: LOW
  - Related actions: transfer(address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x9f43ab02cacc8e709b05936a92dc85b76d1523c4`
  - Risk level: LOW
  - Related actions: transfer(address,address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xbfc1feca8b09a5c5d3effe7429ebe24b9c09ef58`
  - Risk level: LOW
  - Related actions: transfer(address,address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xc4ed0a9ea70d5bcc69f748547650d32cc219d882`
  - Risk level: LOW
  - Related actions: transfer(address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xf3fc178157fb3c87548baa86f9d24ba38e649b58`
  - Risk level: LOW
  - Related actions: transfer(address,address,uint256), transfer(address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.

### Key Findings
- Unaccounted trace addresses
  - Risk level: LOW
  - Description: One or more addresses appeared in the trace without direct proposal text disclosure.
  - Evidence source: trace

---

## Depth Analysis

- Claimed complexity: moderate
- Actual max depth: 3
- Depth mismatch: no
- Delegatecall count: 2

Summary: Core business actions match proposal text; observed wrapper depth is within a normal review range.

---

## Function Semantic Match

- Dimension score: 9/10
- Severity: LOW
- Summary: Claimed business actions match; extra execution wrappers are present but do not create a business-action mismatch.
- Claimed actions: transfer
- Actual actions: transfer

### Matched Functions
- `transfer(address,address,uint256)`
- `transfer(address,uint256)`

---

## Potential Risk Findings

### 1. LOW - Unaccounted trace addresses

- **Severity**: LOW
- **Description**: One or more addresses appeared in the trace without direct proposal text disclosure.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review undisclosed execution path components, but prioritize whether the core business action remains covered by proposal text.
- **Key Evidence**:
  - Unaccounted addresses: 0x912ce59144191c1204e64559fe8253a0e49e6548, 0x9f43ab02cacc8e709b05936a92dc85b76d1523c4, 0xbfc1feca8b09a5c5d3effe7429ebe24b9c09ef58, 0xc4ed0a9ea70d5bcc69f748547650d32cc219d882, 0xf3fc178157fb3c87548baa86f9d24ba38e649b58

---

## Security Conclusion

The proposal text and the observed payload effects are broadly consistent. No clear Semantic Gap was found. Reviewers should still manually review any low-risk undisclosed addresses or unknown selectors.

---

## Summary

The proposal text claims: The Rari Foundation proposes to integrate Arbitrum One with the open-source Rarible Protocol (including an indexer, orderbook, and SDK) to jumpstart NFT ecosystem growth on Arbitrum, requesting 127,351 ARB from the DAO.
The payload actually shows: transfer. Decoded functions include: transfer(address,address,uint256), transfer(address,uint256).
The most important scoring issue is `conflict_detection`, which scored 8/10.
No HIGH or CRITICAL finding was generated. Unknown or unclear fields should still be manually reviewed.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
