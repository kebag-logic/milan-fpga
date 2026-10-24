# media_phase hosted budget: derivation (#781)

Head under study: dev `a032c6d6e3775f145349d5a495c1e1ad12294936`, unchanged.

## Hosted (receipts/hosted)

Shard 10/16 = `milan_dp__3`, `pp_shadow__3`, `ifg`, `media_phase` in all three attempts. ubuntu-24.04, `nproc` 4.
`media_phase`'s `CASE_JOBS` is its Makefile default, 3: the workflow sets VERILATOR_JOBS=4 but nothing sets CASE_JOBS.

| Run / attempt / job | Job (API) | Setup | milan_dp__3 | pp_shadow__3 | ifg | media_phase |
|---|---|---|---|---|---|---|
| 40098975073 / 1 / 120887850753 | 13:53:48–14:22:52, 1744 s | 81.8 s | 364.7 s | 386.1 s | 5.2 s | TIMEOUT 900.0 s |
| 40098975073 / 2 / 120934873499 | 17:14:00–17:42:45, 1725 s | 78.7 s | 354.1 s | 378.0 s | 5.0 s | TIMEOUT 900.0 s |
| 40103838859 / 1 / 120902541972 | 15:18:17–15:49:25, 1868 s | 84.2 s | 419.4 s | 451.1 s | 5.2 s | TIMEOUT 900.0 s |

Each artifact `media_phase.log` ends `make: *** [Makefile:160: cases] Terminated`: the five builds and the
pins, render, blend, ofs and det targets finished, and the thirteen loop cases were still running.
The hosted window is therefore only a lower bound, more than 900 s.

## Local (receipts/local)

Serial, uncontended, on 4 CPUs booked to this lane alone (2 physical cores x 2 SMT threads, the 4-vCPU
runner's shape), pinned Verilator 5.050 (the hosted version), the hosted job's env
(CI_*_JOBS=4, VERILATOR_JOBS=4, SIM_JOBS=4, MAKEFLAGS=-j1), a fresh clone at the head, and the suite
wall clock raised so it could finish.

| Run | What | milan_dp__3 | pp_shadow__3 | ifg | media_phase | checks |
|---|---|---|---|---|---|---|
| A | shard 10/16 replica, CASE_JOBS 3 | (harness refusal, see below) | (same) | 5.5 s | **787.5 s** PASS | 386, 0 failures |
| B | shard 10/16 replica, CASE_JOBS 3 | 329.7 s PASS | 286.4 s PASS | 5.5 s | **769.3 s** PASS | 386, 0 failures |
| C | `make -C tb/verilator/media_phase CASE_JOBS=4` | | | | **725.4 s** PASS | 386, 0 failures |

Run A's two pieces were refused before running (`source dependency origin differs: third_party/tsn-c-stack`,
because the scratch clone's submodule origin was a local path). Its `media_phase` window is still valid. An
earlier attempt, run A0, aborted in preflight because `nohup` made the HUP control's process ignore SIGHUP.
That was a harness error. Both are kept.

## Hosted / local ratio, same hosted jobs, run B as the local reference

| Hosted job | milan_dp__3 | pp_shadow__3 | media_phase projected (787.5 s x ratio) |
|---|---|---|---|
| 120887850753 | 1.106 | 1.348 | 871–1062 s |
| 120934873499 | 1.074 | 1.320 | 846–1040 s |
| 120902541972 | 1.272 | 1.575 | 1002–1240 s |

Observed: more than 900 s, so the ratio for `media_phase` is above 900 / 787.5 = 1.143.
Projected hosted window: **900 s < T <= about 1240 s**.

## Budget

At the worst projection, 1240 s, the default 1800 s leaves 560 s (31%), so the default fits hosted
with margin. The smallest figure keeping the #673 precedent's 10% margin over the projection is
1364 s.

## Fit (receipts/checker, from the checker's own `headroom_problems` / `balance`)

- 16 workers, as on the head: balanced demand 24098 s against capacity 15 x 1620 = 24300 s, so 202 s
  of slack. The largest `media_phase` figure accepted is **936 s**. 937 s puts worker 9 at 1621 s.
- **1800 s never fits a regular worker.** That worker would be 1800 + 122 s setup = 1922 s alone,
  over its 1620 s bound (60% of 45 minutes, and the absolute 1620 s rule), however the shards are
  balanced or counted. Any figure over 1498 s has the same problem.
- 1364 s (projection + 10%) with 16 workers puts the busiest regular worker over 1620 s. Total
  demand alone exceeds capacity by 24098 − 900 + 1364 − 24300 = 262 s, so no rebalancing fits it.
- 17 workers at 45 minutes: up to 1498 s is accepted (1364 s → busiest 1605 s). That changes the
  workflow's matrix, `ci_events.py --expect 16`, the `matrix.shard == 15` timeout expression and
  `WORKER_OVERHEAD_SECONDS`.

The assignment's STOP condition holds: no budget that fits hosted with margin fits any worker's bound
without a workflow change (timeout-minutes, or the worker count).
