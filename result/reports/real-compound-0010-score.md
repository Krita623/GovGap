# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:24 UTC
**Proposal ID**: 341
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
- `0x023ee795361b28cdbb94e302983578486a0a5f1b`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x0a4f4f9e84fc4f674f0d209f94d41fafe5af887d`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x18084fba666a33d37592fa2633fd49a74dd93a88`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x1ec63b5883c3481134fd50d5daebc83ecd2e8779`
  - Risk level: HIGH
  - Related actions: upgradeTo(address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x1f9840a85d5af5bf1d1762f925bdaddc4201f984`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x2260fac5e5542a773aa44fbcfedf7c193bc2c599`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x24e3c657c27dfc7ea6f9f58e86387d846b3baa59`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x2c1d072e956affc0d435cb7ac38ef18d24d9127c`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x316f9708bb98af7da9c68c1c3b5e79039cd336e3`
  - Risk level: HIGH
  - Related actions: addAsset(address,(address,address,uint8,uint64,uint64,uint64,uint128)), deploy(address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x43506849d7c04f9138d1a2050bbf3a0c054402dd`
  - Risk level: HIGH
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x4a3411ac2948b33c69666b35cc6d055b27ea84f1`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x514910771af9ca656af840dff83e8264ecf986ca`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x553303d460ee0afb37edff9be42922d8ff63220e`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x5f4ec3df9cbd43714fe2740f5e3616155c5b8419`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x6d903f6003cca6255d85cca4d3b5e5146dc33925`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x7458bfdc30034eb860b265e6068121d18fa5aa72`
  - Risk level: HIGH
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x7d4e742018fb52e48b08be73d041c18b21de6fb5`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x8fffffd4afb6115b954bd326cbe7b4ba576818f6`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x96d6e33b411dc1f4e3f1e894a5a5d9ce0f96738d`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48`
  - Risk level: HIGH
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xa7f7de6ccad4d83d81676717053883337ac2c1b4`
  - Risk level: HIGH
  - Related actions: contract_creation
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xaa9527bf3183a96fe6e55831c96de5cd988d3484`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xbbc07b3e52e0a62e4b8e7f5780f68268af907584`
  - Risk level: HIGH
  - Related actions: contract_creation
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xc00e94cb662c3520282e6f5717214004a7f26888`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xc3d688b66703497daa19211eedff47f25384cdc3`
  - Risk level: HIGH
  - Related actions: upgradeTo(address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xc9e1a09622afdb659913fefe800feae5dbbfe9d7`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf`
  - Risk level: HIGH
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xcfc1fa6b7ca982176529899d99af6473ad80df4f`
  - Risk level: HIGH
  - Related actions: addAsset(address,(address,address,uint8,uint64,uint64,uint64,uint128)), deploy(address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xdbd020caef83efd542f4de03e3cf0c28a4428bd5`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xdef8c51d7c1040637a198effc39613865b32ea51`
  - Risk level: HIGH
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xf4030086522a5beea4988f8ca5b36dbc97bee88c`
  - Risk level: HIGH
  - Related actions: unable to confirm
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
- Actual max depth: 6
- Depth mismatch: yes
- Delegatecall count: 4

Summary: Observed trace depth exceeds claimed complexity.

### Key Findings
- Trace complexity exceeds textual complexity disclosure
  - Risk level: MEDIUM
  - Description: Observed trace depth exceeds claimed complexity.
  - Evidence source: trace

---

## Function Semantic Match

- Dimension score: 2/10
- Severity: CRITICAL
- Summary: Text claims a low-risk action while the trace includes a sensitive business action.
- Claimed actions: parameter_update, upgrade
- Actual actions: contract_creation, upgrade

### Matched Functions
- `addAsset(address,(address,address,uint8,uint64,uint64,uint64,uint128))`
- `clone((address,address,address,address,address,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint104,uint104,uint104,(address,address,uint8,uint64,uint64,uint64,uint128)[]))`
- `decimals()`
- `deploy(address)`
- `deployAndUpgradeTo(address,address)`
- `upgradeTo(address)`

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
  - Unaccounted addresses: 0x023ee795361b28cdbb94e302983578486a0a5f1b, 0x0a4f4f9e84fc4f674f0d209f94d41fafe5af887d, 0x18084fba666a33d37592fa2633fd49a74dd93a88, 0x1ec63b5883c3481134fd50d5daebc83ecd2e8779, 0x1f9840a85d5af5bf1d1762f925bdaddc4201f984, 0x2260fac5e5542a773aa44fbcfedf7c193bc2c599, 0x24e3c657c27dfc7ea6f9f58e86387d846b3baa59, 0x2c1d072e956affc0d435cb7ac38ef18d24d9127c, 0x316f9708bb98af7da9c68c1c3b5e79039cd336e3, 0x43506849d7c04f9138d1a2050bbf3a0c054402dd, 0x4a3411ac2948b33c69666b35cc6d055b27ea84f1, 0x514910771af9ca656af840dff83e8264ecf986ca, 0x553303d460ee0afb37edff9be42922d8ff63220e, 0x5f4ec3df9cbd43714fe2740f5e3616155c5b8419, 0x6d903f6003cca6255d85cca4d3b5e5146dc33925, 0x7458bfdc30034eb860b265e6068121d18fa5aa72, 0x7d4e742018fb52e48b08be73d041c18b21de6fb5, 0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0, 0x8fffffd4afb6115b954bd326cbe7b4ba576818f6, 0x96d6e33b411dc1f4e3f1e894a5a5d9ce0f96738d, 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48, 0xa7f7de6ccad4d83d81676717053883337ac2c1b4, 0xaa9527bf3183a96fe6e55831c96de5cd988d3484, 0xbbc07b3e52e0a62e4b8e7f5780f68268af907584, 0xc00e94cb662c3520282e6f5717214004a7f26888, 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2, 0xc3d688b66703497daa19211eedff47f25384cdc3, 0xc9e1a09622afdb659913fefe800feae5dbbfe9d7, 0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf, 0xcfc1fa6b7ca982176529899d99af6473ad80df4f, 0xdbd020caef83efd542f4de03e3cf0c28a4428bd5, 0xdef8c51d7c1040637a198effc39613865b32ea51, 0xf4030086522a5beea4988f8ca5b36dbc97bee88c

### 2. MEDIUM - Trace complexity exceeds textual complexity disclosure

- **Severity**: MEDIUM
- **Description**: Observed trace depth exceeds claimed complexity.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review whether the proposal text should describe the actual call depth or indirect execution paths.
- **Key Evidence**:
  - Complexity: claimed=moderate, actual_max_depth=6

### 3. CRITICAL - Claimed actions do not fully match trace actions

- **Severity**: CRITICAL
- **Description**: Text claims a low-risk action while the trace includes a sensitive business action.
- **Evidence Source**: rule_engine
- **Confidence**: 0.9
- **Recommendation**: Compare proposal action wording with decoded functions and risk actions before relying on the text.
- **Key Evidence**:
  - Action comparison: claimed=parameter_update, upgrade, actual=unable to confirm

---

## Security Conclusion

The proposal has a critical Semantic Gap or potential attack indicators. The textual commitment and observed on-chain behavior are severely inconsistent. Do not execute without immediate manual security review.

---

## Summary

The proposal text claims: Compound Growth Program (AlphaGrowth) proposes to add tBTC as collateral into the cUSDCv3 market on the Ethereum Mainnet, setting risk parameters based on Gauntlet's recommendations, and upgrading Comet to a new version.
The payload actually shows: contract_creation, upgrade. Decoded functions include: addAsset(address,(address,address,uint8,uint64,uint64,uint64,uint128)), clone((address,address,address,address,address,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint104,uint104,uint104,(address,address,uint8,uint64,uint64,uint64,uint128)[])), decimals(), deploy(address), deployAndUpgradeTo(address,address), upgradeTo(address).
The most important scoring issue is `function_semantic_match`, which scored 2/10.
High-risk findings include: Unaccounted trace addresses, Claimed actions do not fully match trace actions. Pausing or escalating to manual audit is recommended.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
