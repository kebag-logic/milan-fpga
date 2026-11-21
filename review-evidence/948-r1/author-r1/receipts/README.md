# Receipts, lane 948 round 1

| Directory | What |
|---|---|
| `failing-first/` | each new test on the base RTL (its README lists the runs and their counts) |
| `rtl/` | the new tests at the fix: the `avtp_rxmon` suite, `fanout_mutants.py` (12 of 12), obj_nxn8 with [FAN], the twin's fan-out leg and plant, `milan_dp_mclk` (36 of 36) |
| `twin/` | the twin gate at `73f1113b`: twin, twin-plants, twin-maps, twin-maps-plants, twin-fanout, twin-fanout-plants |
| `sweep-c2e5e5bd/` | the four-shard sweep and its summary |
| `firmware/` | the firmware gate's four shards |
| `budget/` | the twelve CPU budget images against the train's record, the rows' checks (the quick list), the long checks |
| `gates/` | docs workflow steps, lint ratchet, xvlog gate, Yosys on the touched tops, the AAF field campaign with its generator |
| `fit/` | each route's signoff, per-clock slack, utilization, hierarchy moves against the train's gating build, worst paths; `SUMMARY.txt`; the RTL since the routes and the sweep; the superseded `b9a88d25` route |

Host paths are replaced by placeholders (`<scratch>`, `<lane>`, `<tools>`, `<home>`, `<ci-image>`); no report is copied
whole where it is over 200 KB (the logs that are kept are gzipped).
