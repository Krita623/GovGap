# DAO Benchmark Collector

Collect raw on-chain governance proposal data from the Tally Governance GraphQL
API for a fixed DAO benchmark set.

Current scope: raw data only. No ABI decoding, decoded calls, Action IR,
mutation samples, or human labels.

## Target DAOs

Configured in `config/dao_registry.json`:

- Compound
- Uniswap
- ENS
- Arbitrum
- Aave
- Nouns DAO

## Setup

```powershell
pip install -r requirements.txt
```

Set your Tally API key:

```powershell
$env:TALLY_API_KEY="your_key_here"
```

Or create a local `.env` file based on `.env.example`.

## Commands

Run commands from the project root:

```powershell
cd dao_benchmark_collector
```

### Fetch governors

```powershell
python -m src.main fetch-governors
```

Prints governor metadata and chain ID checks for each DAO.

### Inspect proposals

```powershell
python -m src.main inspect-proposals
```

Fetches proposal lists and prints per-DAO counts:

- total proposals
- status counts
- missing `created_block` count
- earliest/latest `created_block`

### Sample proposals

```powershell
python -m src.main sample-proposals
```

Samples 20 proposals per DAO using the fixed stratified sampling rules and
writes:

- `outputs/sampling_report.json`

### Collect raw samples

```powershell
python -m src.main collect
```

Runs the full raw collection pipeline:

1. Load DAO registry.
2. Fetch governors.
3. Fetch proposal lists.
4. Sample proposals.
5. Hydrate proposal details.
6. Write raw sample files and indexes.

Outputs:

- `outputs/raw_samples/*.json`
- `outputs/manifest.jsonl`
- `outputs/sampling_report.json`
- `outputs/collection_log.jsonl`

### Prepare ABIs

```powershell
python -m src.main prepare-abis
```

Scans existing `outputs/raw_samples/*.json`, extracts unique target contracts,
and fetches missing ABIs through Etherscan V2.

Outputs:

- `outputs/abi_targets.jsonl`
- `outputs/abi_report.json`
- `outputs/abi_log.jsonl`
- `abis/{chain_id}/{lowercase_target_address}.json`

### Decode samples

```powershell
python -m src.main decode-samples
```

Reads existing `outputs/raw_samples/*.json` and local ABI files, then writes
calldata decoding outputs. This command is offline: it does not call Explorer
APIs, Tally, or `collect`.

Outputs:

- `outputs/decoded_samples/*.json`
- `outputs/decoded_manifest.jsonl`
- `outputs/decode_report.json`

### Prepare and decode

```powershell
python -m src.main decode
```

Runs `prepare-abis` first, then offline `decode-samples`.

## Raw Sample Schema

Each file in `outputs/raw_samples/` uses this shape:

```json
{
  "benchmark_id": "real-uniswap-0007",
  "dao": {
    "name": "Uniswap",
    "chain_id": 1,
    "governor_address": "0x...",
    "governance_system": "GovernorBravo"
  },
  "proposal": {
    "proposal_id": "47",
    "proposal_url": "https://www.tally.xyz/gov/uniswap/proposal/47",
    "source": "tally",
    "created_block": 12345678,
    "executed_block": 12399999,
    "status": "executed"
  },
  "proposal_text": {
    "title": "...",
    "description": "..."
  },
  "payload": {
    "targets": ["0x..."],
    "values": ["0"],
    "signatures": ["transfer(address,uint256)"],
    "calldatas": ["0x..."]
  },
  "transactions": {
    "created_tx_hash": "0x...",
    "executed_tx_hash": "0x..."
  }
}
```

## Sampling

Fixed seed:

```text
20260429
```

Per DAO target: 20 proposals.

Time buckets:

- `early`
- `middle`
- `recent`

Status buckets:

- `executed_like`
- `non_executed_like`

Quota:

| Time bucket | Executed-like | Non-executed-like |
| --- | ---: | ---: |
| early | 4 | 2 |
| middle | 5 | 1 |
| recent | 6 | 2 |

## Notes

- API endpoint: `https://api.tally.xyz/query`
- API header: `Api-Key`
- The collector uses request throttling to reduce Tally rate-limit errors.
- `collection_log.jsonl` records warnings and recoverable collection errors.
- Local ABI lookup path: `abis/{chain_id}/{lowercase_target_address}.json`
- Optional explorer API keys:
  - `ETHERSCAN_API_KEY`
  - `ARBISCAN_API_KEY`
