# DAO Proposal Semantic Gap Audit Report

**Generated At**: 2026-05-08 11:15:24 UTC
**Proposal ID**: 442
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

### Unaccounted Addresses
- `0x055e53f50b84fd91c4be367220efd36c3d091e1f`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x10707fbc5ec533c11939c236c0b798dada1eb78d`
  - Risk level: CRITICAL
  - Related actions: contract_creation
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x18084fba666a33d37592fa2633fd49a74dd93a88`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x1923dfee706a8e78157416c29cbccfde7cdf4102`
  - Risk level: CRITICAL
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x1a2058b0dd6a97beb2796fcd6c3024fb47cf01cd`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x1ec63b5883c3481134fd50d5daebc83ecd2e8779`
  - Risk level: CRITICAL
  - Related actions: upgradeTo(address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x1fa408992e74a42d1787e28b880c451452e8c958`
  - Risk level: CRITICAL
  - Related actions: contract_creation
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x229047fed2591dbec1ef1118d64f7af3db9eb290`
  - Risk level: CRITICAL
  - Related actions: resourceConfig()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x25ace71c97b33cc4729cf772ae268934f7ab5fa1`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x2665701293fcbeb223d11a08d826563edcce423a`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x28e4f3a7f651294b9564800b2d01f35189a5bfbe`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x316f9708bb98af7da9c68c1c3b5e79039cd336e3`
  - Risk level: CRITICAL
  - Related actions: deploy(address), setBaseTrackingSupplySpeed(address,uint64)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x31b844dbc7cdbaa27d22fd6d54986836d023bf3f`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x340f923e5c7cbb2171146f64169ec9d5a9ffe647`
  - Risk level: CRITICAL
  - Related actions: resourceConfig()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x353e98f34b6e5a8d9d1876bf6df01284d05837cb`
  - Risk level: CRITICAL
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x3781a9f2f2391ef3a2c808cfd55af5af750f74da`
  - Risk level: CRITICAL
  - Related actions: contract_creation
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x3d0bb1ccab520a66e607822fc55bc921738fafe3`
  - Risk level: CRITICAL
  - Related actions: upgradeTo(address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x3ff744cf6078714bb9d3c4fe5ab37fa6d05dec4e`
  - Risk level: CRITICAL
  - Related actions: contract_creation
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x427ea0710fa5252057f0d88274f7aeb308386caf`
  - Risk level: CRITICAL
  - Related actions: resourceConfig()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x49048044d57e1c92a77f79988d21fa8faf74e97e`
  - Risk level: CRITICAL
  - Related actions: depositTransaction(address,uint256,uint64,bool,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x4c9edd5852cd905f086c759e8383e09bff1e68b3`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x4dbd4fc535ac27206064b68ffcf827b0a60bab3f`
  - Risk level: CRITICAL
  - Related actions: createRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes), transfer
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x4e7991e5c547ce825bdeb665ee14a3274f9f61e0`
  - Risk level: CRITICAL
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x56072c95faa701256059aa122697b133aded9279`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x592700e4fcdd674dc54d2681ded3b63f54f63f9a`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x5d409e56d886231adaf00c8775665ad0f9897b56`
  - Risk level: CRITICAL
  - Related actions: upgradeTo(address)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x5d5a095665886119693f0b41d8dfee78da033e8b`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x5e2420cace3650622f62b2713b2b3727fc8bcdd1`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x5f4ec3df9cbd43714fe2740f5e3616155c5b8419`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x60ff20bacd9a647e4025ed8b17ce30e40095a1d2`
  - Risk level: CRITICAL
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x676a795fe6e43c17c668de16730c3f690feb7120`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x6968f3f16c3e64003f02e121cf0d5ccbf5625a42`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x6d903f6003cca6255d85cca4d3b5e5146dc33925`
  - Risk level: CRITICAL
  - Related actions: createRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes), sendMessage(address,bytes,uint32), sendMessageToChild(address,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x6dbb7d9c5dc60844b8cf442ddc6be081c060b2e3`
  - Risk level: CRITICAL
  - Related actions: resourceConfig()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x72e9b6f907365d76c6192ad49c0c5ba356b7fa48`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x73a79fab69143498ed3712e519a88a918e1f4072`
  - Risk level: CRITICAL
  - Related actions: resourceConfig()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x7458bfdc30034eb860b265e6068121d18fa5aa72`
  - Risk level: CRITICAL
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x7c058ad1d0ee415f7e7f30e62db1bcf568470a10`
  - Risk level: CRITICAL
  - Related actions: createRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x7d4e742018fb52e48b08be73d041c18b21de6fb5`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x7de363b6bf0a892b94a1cd0c9df76826bfc14228`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x8315177ab297ba92a06054ce80a67ed4dbd7ed3a`
  - Risk level: CRITICAL
  - Related actions: delegatecall, transfer
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x8350b7de6a6a2c1368e7d4bd968190e13e354297`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x866e82a600a1414e583f7f13623f1ac5d58b0afa`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0x87641f6bc5ad796ea2f30af2a79ab2cf30f74188`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
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
- `0x9bd289b14dd6e0782af82eeb3fcfeed4354cda2c`
  - Risk level: CRITICAL
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xa1290d69c65a6fe4df752f95823fae25cb99e5a7`
  - Risk level: CRITICAL
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xa3931d71877c0e7a3148cb7eb4463524fec27fbd`
  - Risk level: CRITICAL
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xa569d910839ae8865da8f8e70fffb0cba869f961`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xb443da3e07052204a02d630a8933dac05a0d6fb4`
  - Risk level: CRITICAL
  - Related actions: depositTransaction(address,uint256,uint64,bool,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xb8de82551fa4ba3be4b3d9097763edbeed541308`
  - Risk level: CRITICAL
  - Related actions: sendMessage(address,bytes,uint32)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xba8f83fffc7097cbcd89fe323d31753cfac33867`
  - Risk level: CRITICAL
  - Related actions: contract_creation
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xbeb5fc579115071764c7423a4f12edde41f106ed`
  - Risk level: CRITICAL
  - Related actions: depositTransaction(address,uint256,uint64,bool,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xbf5495efe5db9ce00f80364c8b423567e58d2110`
  - Risk level: CRITICAL
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xc49399814452b41da8a7cd76a159f5515cb3e493`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xc54cb22944f2be476e02decfcd7e3e7d3e15a8fb`
  - Risk level: CRITICAL
  - Related actions: depositTransaction(uint256,uint256,address,uint256,uint64,bool,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xc7986b6318c3f3ab5be12baf22892961158d3c24`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf`
  - Risk level: CRITICAL
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xcc16f670129f965b396f2e81312f6e339ffdb18e`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xcd5fe23c85820f7b72d0926fc9b05b43e359b7ee`
  - Risk level: CRITICAL
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xcfc1fa6b7ca982176529899d99af6473ad80df4f`
  - Risk level: CRITICAL
  - Related actions: deploy(address), setBaseTrackingSupplySpeed(address,uint64)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xd11c452fc99cf405034ee446803b6f6c1f6d5ed8`
  - Risk level: CRITICAL
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xd1a622566f277aa76c3c47a30469432aaec95e38`
  - Risk level: CRITICAL
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xd4ec911b8fd79139736950235a93d3ea9c3f68ed`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xdae05e337c56cd1b988fd7a6b74e8bbd3028c4c6`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xdc035d45d973e3ec169d2276ddab16f1e407384f`
  - Risk level: CRITICAL
  - Related actions: decimals()
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xdddf3dee5ed072f3b9e20917e6b462ae0ea4fc10`
  - Risk level: CRITICAL
  - Related actions: contract_creation
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xde1fcfb0851916ca5101820a69b13a4e276bd81f`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xe1399f54ba2597b4eada9e3450c34d393fb131a7`
  - Risk level: CRITICAL
  - Related actions: depositTransaction(uint256,uint256,address,uint256,uint64,bool,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xe54cf0f468963881d44898348669f6b321b463a1`
  - Risk level: CRITICAL
  - Related actions: contract_creation
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xea2a6e7b41505d62d404f927f991edc9e45883c2`
  - Risk level: CRITICAL
  - Related actions: contract_creation
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xef819fe60af67698567f03095a029ae1a1935007`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xfe5e5d361b2ad62c541bab87c45a0b9b018389a2`
  - Risk level: CRITICAL
  - Related actions: sendMessageToChild(address,bytes)
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.
- `0xff30586cd0f29ed462364c7e81375fc0c71219b1`
  - Risk level: CRITICAL
  - Related actions: unable to confirm
  - Evidence source: trace
  - Note: this address was not explicitly disclosed in the proposal text. If the system cannot verify its role, manual review is required.

### Key Findings
- Unaccounted trace addresses
  - Risk level: CRITICAL
  - Description: One or more addresses appeared in the trace without direct proposal text disclosure.
  - Evidence source: trace

---

## Depth Analysis

- Claimed complexity: simple
- Actual max depth: 8
- Depth mismatch: yes
- Delegatecall count: 22

Summary: Observed trace depth exceeds claimed complexity.

### Key Findings
- Trace complexity exceeds textual complexity disclosure
  - Risk level: HIGH
  - Description: Observed trace depth exceeds claimed complexity.
  - Evidence source: trace

---

## Function Semantic Match

- Dimension score: 2/10
- Severity: CRITICAL
- Summary: Text claims a low-risk action while the trace includes a sensitive business action.
- Claimed actions: parameter_update
- Actual actions: bridge, contract_creation, parameter_update, transfer, upgrade

### Matched Functions
- `assetListFactory()`
- `clone((address,address,address,address,address,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint104,uint104,uint104,(address,address,uint8,uint64,uint64,uint64,uint128)[]))`
- `createAssetList((address,address,uint8,uint64,uint64,uint64,uint128)[])`
- `createRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes)`
- `decimals()`
- `deploy(address)`
- `deployAndUpgradeTo(address,address)`
- `depositTransaction(address,uint256,uint64,bool,bytes)`
- `depositTransaction(uint256,uint256,address,uint256,uint64,bool,bytes)`
- `getAddress(string)`
- `resourceConfig()`
- `sendMessage(address,bytes,uint32)`
- `sendMessageToChild(address,bytes)`
- `setBaseTrackingSupplySpeed(address,uint64)`
- `syncState(address,bytes)`
- `upgradeTo(address)`

### Unmatched Or Additional Actions
- `bridge`
  - Risk level: CRITICAL
  - Note: this action was not fully matched to the claimed proposal action. Review the linked evidence before relying on the proposal text.
- `contract_creation`
  - Risk level: CRITICAL
  - Note: this action was not fully matched to the claimed proposal action. Review the linked evidence before relying on the proposal text.
- `transfer`
  - Risk level: CRITICAL
  - Note: this action was not fully matched to the claimed proposal action. Review the linked evidence before relying on the proposal text.
- `upgrade`
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
  - Unaccounted addresses: 0x055e53f50b84fd91c4be367220efd36c3d091e1f, 0x10707fbc5ec533c11939c236c0b798dada1eb78d, 0x18084fba666a33d37592fa2633fd49a74dd93a88, 0x1923dfee706a8e78157416c29cbccfde7cdf4102, 0x1a2058b0dd6a97beb2796fcd6c3024fb47cf01cd, 0x1ec63b5883c3481134fd50d5daebc83ecd2e8779, 0x1fa408992e74a42d1787e28b880c451452e8c958, 0x229047fed2591dbec1ef1118d64f7af3db9eb290, 0x25ace71c97b33cc4729cf772ae268934f7ab5fa1, 0x2665701293fcbeb223d11a08d826563edcce423a, 0x28e4f3a7f651294b9564800b2d01f35189a5bfbe, 0x316f9708bb98af7da9c68c1c3b5e79039cd336e3, 0x31b844dbc7cdbaa27d22fd6d54986836d023bf3f, 0x340f923e5c7cbb2171146f64169ec9d5a9ffe647, 0x353e98f34b6e5a8d9d1876bf6df01284d05837cb, 0x3781a9f2f2391ef3a2c808cfd55af5af750f74da, 0x3d0bb1ccab520a66e607822fc55bc921738fafe3, 0x3ff744cf6078714bb9d3c4fe5ab37fa6d05dec4e, 0x427ea0710fa5252057f0d88274f7aeb308386caf, 0x49048044d57e1c92a77f79988d21fa8faf74e97e, 0x4c9edd5852cd905f086c759e8383e09bff1e68b3, 0x4dbd4fc535ac27206064b68ffcf827b0a60bab3f, 0x4e7991e5c547ce825bdeb665ee14a3274f9f61e0, 0x56072c95faa701256059aa122697b133aded9279, 0x592700e4fcdd674dc54d2681ded3b63f54f63f9a, 0x5d409e56d886231adaf00c8775665ad0f9897b56, 0x5d5a095665886119693f0b41d8dfee78da033e8b, 0x5e2420cace3650622f62b2713b2b3727fc8bcdd1, 0x5f4ec3df9cbd43714fe2740f5e3616155c5b8419, 0x60ff20bacd9a647e4025ed8b17ce30e40095a1d2, 0x676a795fe6e43c17c668de16730c3f690feb7120, 0x6968f3f16c3e64003f02e121cf0d5ccbf5625a42, 0x6d903f6003cca6255d85cca4d3b5e5146dc33925, 0x6dbb7d9c5dc60844b8cf442ddc6be081c060b2e3, 0x72e9b6f907365d76c6192ad49c0c5ba356b7fa48, 0x73a79fab69143498ed3712e519a88a918e1f4072, 0x7458bfdc30034eb860b265e6068121d18fa5aa72, 0x7c058ad1d0ee415f7e7f30e62db1bcf568470a10, 0x7d4e742018fb52e48b08be73d041c18b21de6fb5, 0x7de363b6bf0a892b94a1cd0c9df76826bfc14228, 0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0, 0x8315177ab297ba92a06054ce80a67ed4dbd7ed3a, 0x8350b7de6a6a2c1368e7d4bd968190e13e354297, 0x866e82a600a1414e583f7f13623f1ac5d58b0afa, 0x87641f6bc5ad796ea2f30af2a79ab2cf30f74188, 0x8efb6b5c4767b09dc9aa6af4eaa89f749522bae2, 0x93e8f92327bfa8096f5f6ee5f2a49183d3b3b898, 0x9bd289b14dd6e0782af82eeb3fcfeed4354cda2c, 0xa1290d69c65a6fe4df752f95823fae25cb99e5a7, 0xa3931d71877c0e7a3148cb7eb4463524fec27fbd, 0xa569d910839ae8865da8f8e70fffb0cba869f961, 0xb443da3e07052204a02d630a8933dac05a0d6fb4, 0xb8de82551fa4ba3be4b3d9097763edbeed541308, 0xba8f83fffc7097cbcd89fe323d31753cfac33867, 0xbeb5fc579115071764c7423a4f12edde41f106ed, 0xbf5495efe5db9ce00f80364c8b423567e58d2110, 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2, 0xc49399814452b41da8a7cd76a159f5515cb3e493, 0xc54cb22944f2be476e02decfcd7e3e7d3e15a8fb, 0xc7986b6318c3f3ab5be12baf22892961158d3c24, 0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf, 0xcc16f670129f965b396f2e81312f6e339ffdb18e, 0xcd5fe23c85820f7b72d0926fc9b05b43e359b7ee, 0xcfc1fa6b7ca982176529899d99af6473ad80df4f, 0xd11c452fc99cf405034ee446803b6f6c1f6d5ed8, 0xd1a622566f277aa76c3c47a30469432aaec95e38, 0xd4ec911b8fd79139736950235a93d3ea9c3f68ed, 0xdae05e337c56cd1b988fd7a6b74e8bbd3028c4c6, 0xdc035d45d973e3ec169d2276ddab16f1e407384f, 0xdddf3dee5ed072f3b9e20917e6b462ae0ea4fc10, 0xde1fcfb0851916ca5101820a69b13a4e276bd81f, 0xe1399f54ba2597b4eada9e3450c34d393fb131a7, 0xe54cf0f468963881d44898348669f6b321b463a1, 0xea2a6e7b41505d62d404f927f991edc9e45883c2, 0xef819fe60af67698567f03095a029ae1a1935007, 0xfe5e5d361b2ad62c541bab87c45a0b9b018389a2, 0xff30586cd0f29ed462364c7e81375fc0c71219b1

### 2. HIGH - Trace complexity exceeds textual complexity disclosure

- **Severity**: HIGH
- **Description**: Observed trace depth exceeds claimed complexity.
- **Evidence Source**: trace
- **Confidence**: 0.9
- **Recommendation**: Review whether the proposal text should describe the actual call depth or indirect execution paths.
- **Key Evidence**:
  - Complexity: claimed=simple, actual_max_depth=8

### 3. CRITICAL - Claimed actions do not fully match trace actions

- **Severity**: CRITICAL
- **Description**: Text claims a low-risk action while the trace includes a sensitive business action.
- **Evidence Source**: rule_engine
- **Confidence**: 0.9
- **Recommendation**: Compare proposal action wording with decoded functions and risk actions before relying on the text.
- **Key Evidence**:
  - Action comparison: claimed=parameter_update, actual=unable to confirm

---

## Security Conclusion

The proposal has a critical Semantic Gap or potential attack indicators. The textual commitment and observed on-chain behavior are severely inconsistent. Do not execute without immediate manual security review.

---

## Summary

The proposal text claims: Gauntlet recommends adjusting the COMP rewards for both the supply and borrow sides across various comets (including Base AERO, Mantle USDe, Mainnet USDS, etc.) to aid optimal utilization and lower COMP burn.
The payload actually shows: bridge, contract_creation, parameter_update, transfer, upgrade. Decoded functions include: assetListFactory(), clone((address,address,address,address,address,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint64,uint104,uint104,uint104,(address,address,uint8,uint64,uint64,uint64,uint128)[])), createAssetList((address,address,uint8,uint64,uint64,uint64,uint128)[]), createRetryableTicket(address,uint256,uint256,address,address,uint256,uint256,bytes), decimals(), deploy(address), deployAndUpgradeTo(address,address), depositTransaction(address,uint256,uint64,bool,bytes), depositTransaction(uint256,uint256,address,uint256,uint64,bool,bytes), getAddress(string), resourceConfig(), sendMessage(address,bytes,uint32), sendMessageToChild(address,bytes), setBaseTrackingSupplySpeed(address,uint64), syncState(address,bytes), upgradeTo(address).
The most important scoring issue is `conflict_detection`, which scored 2/10.
High-risk findings include: Unaccounted trace addresses, Trace complexity exceeds textual complexity disclosure, Claimed actions do not fully match trace actions. Pausing or escalating to manual audit is recommended.

---

## Machine-Verifiable Controls

- LLM used for scoring: false
- LLM used for trace analysis: false
- Unsupported claims allowed: false
- Unknown fields preserved as unknown: true

This report is generated from structured rule-engine output and a deterministic template. The LLM is only used for proposal-text semantic extraction and is not used for scoring, trace analysis, or final conclusions.
