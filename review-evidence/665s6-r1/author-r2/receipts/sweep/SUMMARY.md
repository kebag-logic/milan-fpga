head 526f937cde45e3a591fb3b9484ffdcaddbdfa144

Full sweep, 4 shard units (`native-shards.py`; each `bash scripts/run_all_suites.sh <logs> --wait --shard k/4`, pinned Verilator 5.050 and sv2v 0.0.12, one clone and unit per shard, MemoryMax 10G, -j4), started 2026-11-08 04:25 CET, all ended by 05:35 CET. Every shard's exit code is 0 (`shard-k/results.json`).

| Shard | Suites | Passed | Failed | Timed out | Checks | In-suite failures |
|---|---|---|---|---|---|---|
| 0 | 15 | 15 | 0 | 0 | 360987 | 0 |
| 1 | 17 | 17 | 0 | 0 | 1526104 | 0 |
| 2 | 17 | 17 | 0 | 0 | 284228 | 0 |
| 3 | 16 | 16 | 0 | 0 | 21575 | 0 |
| all | 65 | 65 | 0 | 0 | 2192894 | 0 |

Against round 1's sweep at `6584b7bf` (2,192,876 checks), shard 0 holds 18 more: the `milan_dp` split case's 66 checks, which were 48 (`shard-0/milan_dp-split-case.txt`). The other three shards' counts are unchanged.
