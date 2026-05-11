# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:24 UTC
**Proposal ID**: 42
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

### Addresses Disclosed In Proposal Text
- `0x03a520b32c04bf3beef7beb72e919cf822ed34f1`
- `0x091e99cb1c49331a94dd62755d168e941abd0693`
- `0x0cdee061c75d43c82520ed998c23ac2991c9ac6d`
- `0x31fafd4889fa1269f7a13a66ee0fb458f27d72a9`
- `0x3334d83e224af5ef9c2e7dda7c7c98efd9621fa9`
- `0x3d4e44eb1374240ce5f1b871ab261cd16335b76a`
- `0x42be4d6527829fefa1493e1fb9f3676d2425c3c1`
- `0x4615c383f85d0a2bbed973d83ccecf5cb7121463`
- `0x4f225937edc33efd6109c4cef7b560b2d6401009`
- `0x68ed6c1d24a1aa74ef684e958dd6b6e1f1a90c57`
- `0x93e253d101519578a8df0bce2a43d8292bfb3a1f`
- `0xa6e8772af29b29b9202a073f8e36f447689beef6`
- `0xf9d1077fd35670d4acbd27af82652a8d84577d9f`

### Unaccounted Addresses
- `0x00000000000c2e074ec69a0dfb2997ba6c7d2e1e`
  - Risk level: MEDIUM
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x1a9c8182c09f50c8318d769245bea52c32be35bc`
  - Risk level: MEDIUM
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x4976fb03c32e5b8cfe2b6ccb31c09ba78ebaba41`
  - Risk level: MEDIUM
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.

### Key Findings
- Unaccounted trace addresses
  - Risk level: MEDIUM
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

- Dimension score: 4/10
- Severity: HIGH
- Summary: Claimed business action categories differ from extracted business actions.
- Claimed actions: governance_proposal_creation
- Actual actions: parameter_update

### Matched Functions
- `owner(bytes32)`
- `setText(bytes32,string,string)`

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
  - Unaccounted addresses: 0x00000000000c2e074ec69a0dfb2997ba6c7d2e1e, 0x1a9c8182c09f50c8318d769245bea52c32be35bc, 0x4976fb03c32e5b8cfe2b6ccb31c09ba78ebaba41

### 2. HIGH - Claimed actions do not fully match trace actions

- **Severity**: HIGH
- **Description**: Claimed business action categories differ from extracted business actions.
- **Evidence Source**: rule_engine
- **Confidence**: 0.9
- **Recommendation**: Compare proposal action wording with decoded functions and risk actions before relying on the text.
- **Key Evidence**:
  - Action comparison: claimed=governance_proposal_creation, actual=unable to confirm

---

## Security Conclusion

The proposal has a serious Semantic Gap. Some on-chain actions are not sufficiently covered by the proposal text and may affect governance participants' judgment. Pausing or escalating to manual audit is recommended.

---

## Summary

The proposal text claims: A proposal to officially deploy and recognize Uniswap V3 on the Linea mainnet as a canonical deployment, integrating it with the ConsenSys product ecosystem including MetaMask.
The payload actually shows: parameter_update. Decoded functions include: owner(bytes32), setText(bytes32,string,string).
The most important scoring issue is `function_semantic_match`, which scored 4/10.
High-risk findings include: Claimed actions do not fully match trace actions. Pausing or escalating to manual audit is recommended.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
