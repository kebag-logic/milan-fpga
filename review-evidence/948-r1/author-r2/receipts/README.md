# Receipts, lane 948 round 2

| Directory | What |
|---|---|
| `failing-first/` | the new tests on 4ceba3d4's RTL: `sim_fanout` (FO11-FO13 fail, FO1-FO10 pass), `sim_depkt` at both payload leads (DT1's 65-octet probe gives no frame), the [FAN] STOP legs on the clean 8x8 datapath (pass: the gate is right) and on the two stop-gate plants (each caught by name) |
| `rtl/` | the `avtp_rxmon` suite at the head: the N=4 stack, lockstep N=1 and N=8, the four mutant arms, ctxfmt, fanout, depkt at both leads |
| `twin/` | the twin gate (comparison, plants, maps and its plant, the 8x8 fan-out leg and its plant) and `fan-stop-plants` |
| `sweep/` | the affected suites at the head, each the way `run_all_suites.sh` runs one; the milan_dp run that found the 8-channel stimulus |
| `gates/` | lint ratchet, xvlog gate, Yosys on the two touched tops, the docs workflow's steps, the `tsn_fuzz` AAF campaign with its generator |
| `probe/` | the shortest frame whose PDU the receive stack delivers, at the head and on 4ceba3d4's RTL (scratch probe, not a repository test) |
| `fit/` | each route's signoff, utilization and worst paths |

Host paths are replaced by placeholders (`<scratch>`, `<lane>`, `<tools>`, `<home>`, `<ci-image>`); no file is over 200 KB
(the long logs are gzipped).

## Round 2b (`round2b/`)

| Directory | What |
|---|---|
| `round2b/probe/` | the shortest delivered frame at 15168e14, 4ceba3d4, e8252323 and the head (`probe_minframe2.cpp` in `probe/`), accepted and delivered per length |
| `round2b/failing-first/` | the new tests (0b4517c3) on e8252323's RTL: `sim_fanout` (FO14, FO8), `sim_depkt` at both leads (DT4), obj_nxn8's 1-channel rounds |
| `round2b/rtl/` | the `avtp_rxmon` suite at the head, every leg and arm |
| `round2b/sweep/` | the affected suites at the head, milan_dp's `render_mutants` rerun on its own binaries after the wall clock |
| `round2b/twin/` | the twin gate and `fan-stop-plants` at the head |
| `round2b/gates/` | lint, xvlog, Yosys, the docs workflow's steps, the `tsn_fuzz` AAF campaign with its generator, at the head |
| `round2b/fit/` | the six routes at the head: signoff, utilization, per-clock slack, worst paths, moves against round 2 |
