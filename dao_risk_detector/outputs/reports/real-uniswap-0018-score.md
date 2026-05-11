# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:24 UTC
**Proposal ID**: 94
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

- Dimension score: 2/10
- Severity: CRITICAL
- Summary: An undisclosed address participates in an uncovered critical business action.

### Addresses Disclosed In Proposal Text
- `0x044aaf330d7fd6ae683eec5c1c1d1fff5196b6b7`
- `0x0c3c1c532f1e39edf36be9fe0be1410313e074bf`
- `0x114a43df6c5f54ebb8a9d70cd1951d3dd68004c7`
- `0x1f98431c8ad98523631ae4a59f267346ea31f984`
- `0x33128a8fc17869897dce68ed026d694621f6fdfd`
- `0x3e40db80450f025b01e45c58b0af763c7a29a8bd`
- `0x5e74c9f42eed283bff3744fbd1889d398d40867d`
- `0x8909dc15e40173ff4699343b6eb8132c65e18ec6`
- `0x94460443ca27ffc1baeca61165fde18346c91abd`
- `0x95e337c5b155385945d407f5396387d0c2a3a263`
- `0x9bd25e67bf390437c8faf480ac735a27bcf6168c`
- `0xabea76658b205696d49b5f91b2a03536cb8a3be1`
- `0xafe208a311b21f13ef87e33a90049fc17a7acdec`
- `0xb13285df724ea75f3f1e9912010b7e491dcd5ee3`
- `0xb8018422bce25d82e70cb98fda96a4f502d89427`
- `0xec23cf5a1db3dcc6595385d28b2a4d9b52503be4`
- `0xf1d7cc64fb4452f05c498126312ebe29f30fbcf9`
- `0xff77c0ed0b6b13a20446969107e5867abc46f53a`
- `0xff7ad5da31fecdc678796c88b05926db896b0699`

### Unaccounted Addresses
- `0x0507aaa21c678976fcdc7e804836acd6ebc17a44`
  - Risk level: CRITICAL
  - Related actions: isFeatureEnabled(bytes32), resourceConfig()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x1a9c8182c09f50c8318d769245bea52c32be35bc`
  - Risk level: CRITICAL
  - Related actions: createRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes), sendMessage(address,bytes,uint32), sendMessage(address[],uint256[],bytes[],address,uint16)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x229047fed2591dbec1ef1118d64f7af3db9eb290`
  - Risk level: CRITICAL
  - Related actions: isFeatureEnabled(bytes32), resourceConfig()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x25ace71c97b33cc4729cf772ae268934f7ab5fa1`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x3c3d457f1522d3540ab3325aa5f1864e34cba9d0`
  - Risk level: CRITICAL
  - Related actions: messageFee(), publishMessage(uint32,bytes,uint8)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x49048044d57e1c92a77f79988d21fa8faf74e97e`
  - Risk level: CRITICAL
  - Related actions: depositTransaction(address,uint256,uint64,bool,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x4dbd4fc535ac27206064b68ffcf827b0a60bab3f`
  - Risk level: CRITICAL
  - Related actions: createRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes), transfer
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x73a79fab69143498ed3712e519a88a918e1f4072`
  - Risk level: CRITICAL
  - Related actions: isFeatureEnabled(bytes32), resourceConfig()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x7c058ad1d0ee415f7e7f30e62db1bcf568470a10`
  - Risk level: CRITICAL
  - Related actions: createRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x8315177ab297ba92a06054ce80a67ed4dbd7ed3a`
  - Risk level: CRITICAL
  - Related actions: delegatecall, transfer
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x866e82a600a1414e583f7f13623f1ac5d58b0afa`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x8efb6b5c4767b09dc9aa6af4eaa89f749522bae2`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x93e8f92327bfa8096f5f6ee5f2a49183d3b3b898`
  - Risk level: CRITICAL
  - Related actions: delegatecall
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x97cebbf8959e2a5476fbe9b98a21806ec234609b`
  - Risk level: CRITICAL
  - Related actions: depositTransaction(address,uint256,uint64,bool,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x98f3c9e6e3face36baad05fe09d375ef1464288b`
  - Risk level: CRITICAL
  - Related actions: messageFee(), publishMessage(uint32,bytes,uint8)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xb686f13aff1e427a1f993f29ab0f2e7383729fe0`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xbeb5fc579115071764c7423a4f12edde41f106ed`
  - Risk level: CRITICAL
  - Related actions: depositTransaction(address,uint256,uint64,bool,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xd392c27b84b1ca776528f2704bc67b82a62132d2`
  - Risk level: CRITICAL
  - Related actions: isFeatureEnabled(bytes32), resourceConfig()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xde1fcfb0851916ca5101820a69b13a4e276bd81f`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xf5f4496219f31cdcba6130b5402873624585615a`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address[],uint256[],bytes[],address,uint16)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.

### Key Findings
- Unaccounted trace addresses
  - Risk level: CRITICAL
  - Description: One or more addresses appeared in the trace without direct proposal text disclosure.
  - Evidence source: trace

---

## Depth Analysis

- Claimed complexity: moderate
- Actual max depth: 5
- Depth mismatch: no
- Delegatecall count: 26

Summary: Observed trace depth is consistent with the claimed complexity.

---

## Function Semantic Match

- Dimension score: 2/10
- Severity: CRITICAL
- Summary: Text claims a low-risk action while the trace includes a sensitive business action.
- Claimed actions: role_change, role_change, parameter_update, role_change, role_change, role_change
- Actual actions: bridge, parameter_update, permission_change, transfer

### Matched Functions
- `createRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes)`
- `depositTransaction(address,uint256,uint64,bool,bytes)`
- `getAddress(string)`
- `isFeatureEnabled(bytes32)`
- `messageFee()`
- `publishMessage(uint32,bytes,uint8)`
- `resourceConfig()`
- `sendMessage(address,bytes,uint32)`
- `sendMessage(address[],uint256[],bytes[],address,uint16)`
- `setFactoryOwner(address)`
- `setOwner(address)`

### Unmatched Or Additional Actions
- `bridge`
  - Risk level: CRITICAL
  - Note: this action was not fully matched to the claimed proposal action. Review the linked evidence before relying on the proposal text.
- `transfer`
  - Risk level: CRITICAL
  - Note: this action was not fully matched to the claimed proposal action. Review the linked evidence before relying on the proposal text.

### Key Findings
- Claimed actions do not fully match trace actions
  - Risk level: CRITICAL
  - Description: Text claims a low-risk action while the trace includes a sensitive business action.
  - Evidence source: rule_engine

---

## Potential Risk Findings

### 1. CRITICAL - Unaccounted trace addresses

- **Severity**: CRITICAL
- **Description**: One or more addresses appeared in the trace without direct proposal text disclosure.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Pause or escalate manual review because an uncovered critical business action is linked to an undisclosed address.
- **Key Evidence**:
  - Unaccounted addresses: 0x0507aaa21c678976fcdc7e804836acd6ebc17a44, 0x1a9c8182c09f50c8318d769245bea52c32be35bc, 0x229047fed2591dbec1ef1118d64f7af3db9eb290, 0x25ace71c97b33cc4729cf772ae268934f7ab5fa1, 0x3c3d457f1522d3540ab3325aa5f1864e34cba9d0, 0x49048044d57e1c92a77f79988d21fa8faf74e97e, 0x4dbd4fc535ac27206064b68ffcf827b0a60bab3f, 0x73a79fab69143498ed3712e519a88a918e1f4072, 0x7c058ad1d0ee415f7e7f30e62db1bcf568470a10, 0x8315177ab297ba92a06054ce80a67ed4dbd7ed3a, 0x866e82a600a1414e583f7f13623f1ac5d58b0afa, 0x8efb6b5c4767b09dc9aa6af4eaa89f749522bae2, 0x93e8f92327bfa8096f5f6ee5f2a49183d3b3b898, 0x97cebbf8959e2a5476fbe9b98a21806ec234609b, 0x98f3c9e6e3face36baad05fe09d375ef1464288b, 0xb686f13aff1e427a1f993f29ab0f2e7383729fe0, 0xbeb5fc579115071764c7423a4f12edde41f106ed, 0xd392c27b84b1ca776528f2704bc67b82a62132d2, 0xde1fcfb0851916ca5101820a69b13a4e276bd81f, 0xf5f4496219f31cdcba6130b5402873624585615a

### 2. CRITICAL - Claimed actions do not fully match trace actions

- **Severity**: CRITICAL
- **Description**: Text claims a low-risk action while the trace includes a sensitive business action.
- **Evidence Source**: rule_engine
- **Confidence**: 0.9
- **Recommendation**: Compare proposal action wording with decoded functions and risk actions before relying on the text.
- **Key Evidence**:
  - Action comparison: claimed=role_change, role_change, parameter_update, role_change, role_change, role_change, actual=unable to confirm

---

## Security Conclusion

The proposal has a critical Semantic Gap or potential attack indicators. The textual commitment and observed on-chain behavior are severely inconsistent. Do not execute without immediate manual security review.

---

## Summary

The proposal text claims: This proposal expands Uniswap protocol fees on v2 and v3 to Arbitrum, Base, Celo, OP Mainnet, Soneium, X Layer, Worldchain, and Zora. It also enables fees uniformly on all v3 pools via a new tier-based v3OpenFeeAdapter on Mainnet and the selected L2s, and routes fees to L2 TokenJars for UNI burn on Mainnet.
The payload actually shows: bridge, parameter_update, permission_change, transfer. Decoded functions include: createRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes), depositTransaction(address,uint256,uint64,bool,bytes), getAddress(string), isFeatureEnabled(bytes32), messageFee(), publishMessage(uint32,bytes,uint8), resourceConfig(), sendMessage(address,bytes,uint32), sendMessage(address[],uint256[],bytes[],address,uint16), setFactoryOwner(address), setOwner(address).
The most important scoring issue is `conflict_detection`, which scored 2/10.
High-risk findings include: Unaccounted trace addresses, Claimed actions do not fully match trace actions. Pausing or escalating to manual audit is recommended.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
