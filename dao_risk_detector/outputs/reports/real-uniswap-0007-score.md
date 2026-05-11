# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:24 UTC
**Proposal ID**: 50
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

### Addresses Disclosed In Proposal Text
- `0x1f8a4d195b647647c7dd45650cbd553fd33ccaa6`
- `0x22850a17032f40778c0c0a3fdd96905950a39f89`
- `0x409af45457d4779828bfbcbe7aa653c38edb9ed9`
- `0x4cd986dd509fbb6a695ae971d5c56c8795f640ee`
- `0x76c001ad9e527fefa8fa822a987ad44ce720baed`
- `0x915362b5450acbbc9f8044191ae7e35c86f2fe51`
- `0xb4c47ed546fc31e26470a186ec2c5f19ef09ba41`
- `0xcab04058e60020d65d18d4b3dff2ca1445d7099f`
- `0xe45c06922228a33fff1ed54638a0db78f69f9780`
- `0xe909b0cae57ee7eff56a5ca7fc4b66cf4f7c2d38`
- `0xe9901ae78efb4386b1132009e310d08bcb445bf5`
- `0xf0198aaa4a8792e2a4a6e6fb3039e4b1c71f15bb`
- `0xff3b2da1379cc67cc2755194604713f10b820b0e`
- `0xffd927d6f17495b28635dd49d24638e97bd8c8b8`

### Unaccounted Addresses
- `0x00000000000c2e074ec69a0dfb2997ba6c7d2e1e`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x1a9c8182c09f50c8318d769245bea52c32be35bc`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x4976fb03c32e5b8cfe2b6ccb31c09ba78ebaba41`
  - Risk level: LOW
  - Related actions: unable to confirm
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
- Actual max depth: 1
- Depth mismatch: no
- Delegatecall count: 0

Summary: Core business actions match proposal text; observed wrapper depth is within a normal review range.

---

## Function Semantic Match

- Dimension score: 10/10
- Severity: LOW
- Summary: Claimed business actions match extracted business actions.
- Claimed actions: parameter_update
- Actual actions: parameter_update

### Matched Functions
- `owner(bytes32)`
- `setText(bytes32,string,string)`

---

## Potential Risk Findings

### 1. LOW - Unaccounted trace addresses

- **Severity**: LOW
- **Description**: One or more addresses appeared in the trace without direct proposal text disclosure.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review undisclosed execution path components, but prioritize whether the core business action remains covered by proposal text.
- **Key Evidence**:
  - Unaccounted addresses: 0x00000000000c2e074ec69a0dfb2997ba6c7d2e1e, 0x1a9c8182c09f50c8318d769245bea52c32be35bc, 0x4976fb03c32e5b8cfe2b6ccb31c09ba78ebaba41

---

## Security Conclusion

The proposal text and the observed payload effects are broadly consistent. No clear Semantic Gap was found. Reviewers should still manually review any low-risk undisclosed addresses or unknown selectors.

---

## Summary

The proposal text claims: Proposal by Michigan Blockchain to deploy and officially recognize Uniswap v3 on the Filecoin Virtual Machine (FVM) and utilize Axelar as the interchain governance executor.
The payload actually shows: parameter_update. Decoded functions include: owner(bytes32), setText(bytes32,string,string).
The most important scoring issue is `conflict_detection`, which scored 8/10.
No HIGH or CRITICAL finding was generated. Unknown or unclear fields should still be manually reviewed.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
