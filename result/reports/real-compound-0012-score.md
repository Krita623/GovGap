# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:24 UTC
**Proposal ID**: 240
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
- `0x1c9049c48c24111a3546a73c67fd2a4fc6c86fdc`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x24e3c657c27dfc7ea6f9f58e86387d846b3baa59`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x2885d15b8af22648b98b122b22fdf4d2a56c6023`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x2c1d072e956affc0d435cb7ac38ef18d24d9127c`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b`
  - Risk level: LOW
  - Related actions: _setCollateralFactor(address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x525b031c1ee01502c113500a2d1a999cd3f9c98f`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x547a514d5e3769680ce22b2361c10ea13619e8a9`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x553303d460ee0afb37edff9be42922d8ff63220e`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x658aa21601c8c0bb511c21999f7cad35b6a15192`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x6d903f6003cca6255d85cca4d3b5e5146dc33925`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x8cf42b08ad13761345531b839487aa4d113955d9`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x9441d7556e7820b5ca42082cfa99487d56aca958`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x96d6e33b411dc1f4e3f1e894a5a5d9ce0f96738d`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xa027702dbb89fbd58938e4324ac03b58d812b0e1`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xbafe01ff935c7305907c33bf824352ee5979b526`
  - Risk level: LOW
  - Related actions: _setCollateralFactor(address,uint256)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xcc70f09a6cc17553b2e31954cd36e4a2d89501f7`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xd8b9aa6e811c935ef63e877cfa7be276931293da`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xdbd020caef83efd542f4de03e3cf0c28a4428bd5`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xdef8c51d7c1040637a198effc39613865b32ea51`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xe88c679e2d42963acdc76810d21dac2e6a8d7c29`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xe9a6bccde4875f8c1228975f9c84598558a75ac8`
  - Risk level: LOW
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xec1d1b3b0443256cc3860e24a46f108e699484aa`
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
- Actual max depth: 4
- Depth mismatch: yes
- Delegatecall count: 9

Summary: Core business actions match proposal text; observed wrapper depth is within a normal review range.

---

## Function Semantic Match

- Dimension score: 9/10
- Severity: LOW
- Summary: Claimed business actions match; extra execution wrappers are present but do not create a business-action mismatch.
- Claimed actions: parameter_update
- Actual actions: parameter_update

### Matched Functions
- `_setCollateralFactor(address,uint256)`
- `decimals()`
- `getUnderlyingPrice(address)`
- `latestRoundData()`

---

## Potential Risk Findings

### 1. LOW - Unaccounted trace addresses

- **Severity**: LOW
- **Description**: One or more addresses appeared in the trace without direct proposal text disclosure.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review undisclosed execution path components, but prioritize whether the core business action remains covered by proposal text.
- **Key Evidence**:
  - Unaccounted addresses: 0x1c9049c48c24111a3546a73c67fd2a4fc6c86fdc, 0x24e3c657c27dfc7ea6f9f58e86387d846b3baa59, 0x2885d15b8af22648b98b122b22fdf4d2a56c6023, 0x2c1d072e956affc0d435cb7ac38ef18d24d9127c, 0x3d9819210a31b4961b30ef54be2aed79b9c9cd3b, 0x525b031c1ee01502c113500a2d1a999cd3f9c98f, 0x547a514d5e3769680ce22b2361c10ea13619e8a9, 0x553303d460ee0afb37edff9be42922d8ff63220e, 0x658aa21601c8c0bb511c21999f7cad35b6a15192, 0x6d903f6003cca6255d85cca4d3b5e5146dc33925, 0x8cf42b08ad13761345531b839487aa4d113955d9, 0x9441d7556e7820b5ca42082cfa99487d56aca958, 0x96d6e33b411dc1f4e3f1e894a5a5d9ce0f96738d, 0xa027702dbb89fbd58938e4324ac03b58d812b0e1, 0xbafe01ff935c7305907c33bf824352ee5979b526, 0xcc70f09a6cc17553b2e31954cd36e4a2d89501f7, 0xd8b9aa6e811c935ef63e877cfa7be276931293da, 0xdbd020caef83efd542f4de03e3cf0c28a4428bd5, 0xdef8c51d7c1040637a198effc39613865b32ea51, 0xe88c679e2d42963acdc76810d21dac2e6a8d7c29, 0xe9a6bccde4875f8c1228975f9c84598558a75ac8, 0xec1d1b3b0443256cc3860e24a46f108e699484aa

---

## Security Conclusion

The proposal text and the observed payload effects are broadly consistent. No clear Semantic Gap was found. Reviewers should still manually review any low-risk undisclosed addresses or unknown selectors.

---

## Summary

The proposal text claims: Gauntlet recommends decreasing the Collateral Factor by 5% for various Compound v2 collateral assets (AAVE, BAT, COMP, LINK, MKR, SUSHI, UNI, YFI, ZRX) as part of Phase 11 of the v2 deprecation.
The payload actually shows: parameter_update. Decoded functions include: _setCollateralFactor(address,uint256), decimals(), getUnderlyingPrice(address), latestRoundData().
The most important scoring issue is `conflict_detection`, which scored 8/10.
No HIGH or CRITICAL finding was generated. Unknown or unclear fields should still be manually reviewed.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
