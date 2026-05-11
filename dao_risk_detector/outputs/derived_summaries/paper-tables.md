# GovGap Paper Tables

## Output Completeness

| Item | Count |
| --- | ---: |
| raw_samples | 120 |
| decoded_samples | 120 |
| traces | 120 |
| risk_actions | 120 |
| semantics | 120 |
| scores | 120 |
| reports | 120 |

## Risk Levels

| Risk level | Count |
| --- | ---: |
| CRITICAL | 22 |
| HIGH | 21 |
| LOW | 64 |
| MEDIUM | 13 |

## Risk Action Types

| Type | Count |
| --- | ---: |
| delegatecall | 246 |
| transfer | 102 |
| bridge | 32 |
| approval | 24 |
| unknown | 22 |
| contract_creation | 14 |
| upgrade | 7 |
| arbitrary_call | 5 |
| permission_change | 1 |

## DAO Breakdown

| DAO | Count | CRITICAL | HIGH | MEDIUM | LOW | Average score |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Aave | 20 | 12 | 1 | 5 | 2 | 3.7 |
| Arbitrum | 20 | 0 | 2 | 0 | 18 | 7.6 |
| Compound | 20 | 6 | 7 | 1 | 6 | 4.7 |
| ENS | 20 | 2 | 2 | 1 | 15 | 7.05 |
| Nouns DAO | 20 | 1 | 6 | 3 | 10 | 6.05 |
| Uniswap | 20 | 1 | 3 | 3 | 13 | 6.8 |

## Dataset Sampling

| DAO | Indexed | Eligible | Sampled |
| --- | ---: | ---: | ---: |
| aave | 401 | 379 | 20 |
| arbitrum | 85 | 84 | 20 |
| compound | 531 | 531 | 20 |
| ens | 69 | 68 | 20 |
| nouns-dao | 962 | 958 | 20 |
| uniswap | 88 | 88 | 20 |

## Notes

- Generated from final score JSON files, not from stale batch logs.
- Unknown risk actions are conservative review signals, not confirmed vulnerabilities.
