# DAO Proposal Semantic Gap Detector

This project checks whether a DAO proposal description matches the actual effects of its payload.

It does not replay the full governance lifecycle. Instead, it simulates each proposal payload in the expected executor or timelock context, extracts execution facts from traces, compares them with proposal text semantics, and generates deterministic audit reports.

## What It Detects

- Undisclosed contracts, addresses, or execution paths.
- Hidden execution complexity such as multicall, delegatecall, proxy, bridge, or deep call chains.
- Function-level mismatches such as a proposal claiming maintenance or parameter changes while the payload performs upgrades, transfers, approvals, or permission changes.

## Pipeline

```text
proposal data
-> payload simulation
-> trace parsing
-> risk action extraction
-> proposal text semantic extraction
-> deterministic scoring
-> final audit JSON
-> Markdown report
```

LLM usage is limited to proposal text extraction. Trace analysis, risk action extraction, scoring, and report conclusions are rule-based.

## Project Layout

```text
data/
  raw_samples/        proposal samples
  abis/               optional ABI files

outputs/
  traces/             simulation traces
  risk_actions/       extracted risk actions
  semantics/          proposal text semantics
  scores/             final audit JSON
  reports/            Markdown audit reports
  run_summaries/      batch summaries

scripts/              runnable pipeline commands
src/                  project source code
```

## Requirements

- Python 3.11+
- Foundry Anvil
- RPC URLs for the chains used by the samples
- An OpenAI-compatible or provider-compatible LLM endpoint for proposal text extraction

On Windows, this project expects Anvil to be available through WSL:

```powershell
wsl anvil --version
```

## Setup

Create a virtual environment and install the project:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

Create `.env` from the example:

```powershell
Copy-Item .env.example .env
```

`MAINNET_RPC_URL` and `ARBITRUM_RPC_URL` should match the chains present in your sample data.


## Run One Sample

```powershell
python scripts\simulate_sample.py data\raw_samples\real-aave-0001.json
```

This writes the trace and risk-action output for that sample.

## Run The Full Pipeline

Run the stages in order:

```powershell
python scripts\simulate_all_samples.py
python scripts\extract_all_semantics.py
python scripts\build_all_final_json.py
python scripts\generate_all_reports.py
```

The final Markdown reports are written to:

```text
outputs/reports/
```

The final audit JSON files are written to:

```text
outputs/scores/
```

## Batch Summaries

Each batch stage writes a summary under:

```text
outputs/run_summaries/
```

Useful files:

- `batch-summary.json`: trace and risk-action extraction summary.
- `semantics-batch-summary.json`: LLM extraction summary.
- `scores-batch-summary.json`: deterministic scoring summary.
- `reports-batch-summary.json`: report generation summary.

Example checks:

```powershell
Get-Content outputs\run_summaries\batch-summary.json
Get-Content outputs\run_summaries\scores-batch-summary.json
```

## Outputs

For each sample, the pipeline produces:

- `outputs/traces/<sample>-trace.json`
- `outputs/risk_actions/<sample>-risk-actions.json`
- `outputs/semantics/<sample>-semantics.json`
- `outputs/scores/<sample>-score.json`
- `outputs/reports/<sample>-score.md`

Reports are generated from structured JSON. They do not use LLM-generated conclusions.

## Notes

- Simulation failures should not stop the project from producing structured outputs.
- If Anvil simulation is unavailable, the trace stage can fall back to static calldata decoding.
- Unknown or unverified information is preserved as unknown instead of being filled with assumptions.
