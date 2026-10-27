# Void runs (kept out of every result table)

| Run | Pin | Why void |
|---|---|---|
| parent full sweep, serial, inside the lane's own unit (session 1) | scratch parent `764d1253` | session 1 was stopped by the memory cap of its unit at `capture_coherence` (suites before it: PASS); no completed sweep result |
| parent `[GSI]` mutation campaign `make -C tb/verilator/milan_dp gsi-mutants` (session 1) | `764d1253` | stopped with session 1 while the clean control ran; no verdict |
| parent full sweep, 4 shard units, `VERILATOR_JOBS` unset (session 2, label `pp206-a691-parent`) | `764d1253` | shard 2 was stopped by its unit's 13 GB memory limit while building `capture_coherence`'s datapath model (`VERILATOR_JOBS ?= 0` lets Verilator build with one job per host CPU, not per CPU of the unit); shards 0, 1 and 3 were stopped on purpose so the sweep could be re-run in one configuration. Every suite that finished in it passed. Replaced by the sweep with `VERILATOR_JOBS=4` (label `pp206-a691-parentb`), which changes build parallelism only |
