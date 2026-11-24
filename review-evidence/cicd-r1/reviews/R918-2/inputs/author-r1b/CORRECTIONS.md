[A10] Manager corrections to the round-1 packet of PR #1001, answering R918-1-F1, R918-1-F2 and R917-1-F1. No code changed: the head stays fcbc31f3.

## R918-1-F1: the ccache receipts were mis-attributed

The round-1 packet's `receipts/ccache/{nocc,cold}.time` were the avtp_rxmon whole-suite runs, and `warm.time` was the crf_rx mutant campaign's, all filed under one name. The raw runs are kept per campaign; this packet re-stages them under their own names:

| Campaign | Run | Wall s | User CPU s | Change (user) | Receipt |
|---|---|---:|---:|---:|---|
| crf_rx `mutants.py` (23 cases) | no cache | 376.75 | 497.96 | | `receipts/ccache/crf_rx-mutants/nocc.time` |
| crf_rx `mutants.py` | cold cache | 247.31 | 262.00 | -47.4 % | `.../cold.time` |
| crf_rx `mutants.py` | warm cache | 219.48 | 229.32 | -53.9 % | `.../warm.time` |
| avtp_rxmon suite | no cache | 967.68 | 1587.52 | | `receipts/ccache/avtp_rxmon/nocc.time` |
| avtp_rxmon suite | cold cache | 782.82 | 547.52 | -65.5 % | `.../cold.time`, `cold.stats` |

Each crf_rx run's log is beside its time file (23/23 cases in each; the verdict lines are identical). The avtp_rxmon logs are over the 200 KB receipt limit, so only their sha256 and sizes are kept (`logs.sha256`). The claims in the report and the PR body (crf_rx mutants -47 % cold, -54 % warm; avtp_rxmon -65 %) are therefore reproduced from correctly attributed receipts.

## R918-1-F2 and R917-1-F1: the L1d-miss figure for the budget harness at -O3

The round-1 PR body and report said "L1d misses -7..-9 %". The three identically named paired runs give:

| Pair | Base L1d misses | -O3 L1d misses | Reduction |
|---|---:|---:|---:|
| (unsuffixed) | 3,946,517,051 | 3,374,059,598 | 14.5 % |
| -2 | 3,741,671,160 | 3,411,296,019 | 8.8 % |
| -3 | 3,654,245,643 | 3,457,482,933 | 5.4 % |

The corrected statement is "L1d misses 5-15 % lower in three paired runs (median 8.8 %)". The CPU figure (-2.5 to -5 %) is unchanged. The PR body now says this.
