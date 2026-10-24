# HANDOFF — [A671] #781 media_phase hosted budget

Lane: branch `781-media-phase-hosted-budget` from dev `a032c6d6e3775f145349d5a495c1e1ad12294936`
(origin `https://github.com/kebag-logic/milan-fpga.git`, confirmed).
Assignment: issue #781 comment 6387505940. TAKEN: issue #781 comment 6387516764. STOP: issue #781 comment 6388138007.

## Status: STOP (assignment STOP condition met). No commit, and the head is unchanged.

The lane head is still `a032c6d6e3775f145349d5a495c1e1ad12294936` and the tree is clean. No budget that
fits hosted with margin fits any worker's bound without a workflow change, and the assignment reserves
that change for the manager.

Full derivation: `receipts/DERIVATION.md`. Index: `receipts/INDEX.md`.

## Findings in one place

1. **Hosted window: more than 900 s, lower bound only.** Shard 10/16 on runs 40098975073 (attempts 1
   and 2) and 40103838859 shows `TIMEOUT media_phase` at 900.0 s each time. The jobs ran 1744 s,
   1725 s and 1868 s (job API). Each artifact log ends
   `make: *** [Makefile:160: cases] Terminated`: builds and the pins/render/blend/ofs/det targets were
   done, and the thirteen loop cases were still running.
2. **Local, serial, uncontended, 4 CPUs (2 cores x 2 SMT), pinned Verilator 5.050, hosted env:**
   787.5 s (run A) and 769.3 s (run B) at CASE_JOBS 3, the value the hosted job actually uses. 725.4 s
   (run C) at CASE_JOBS 4, one case per hosted core. Every run: PASS, 386 checks, 0 failures.
3. **Hosted/local ratio** from the same hosted jobs' other suites (run B as reference):
   `milan_dp__3` 1.074–1.272, `pp_shadow__3` 1.320–1.575. Projected hosted `media_phase`:
   900 s < T <= about 1240 s.
4. **Budget:** the default 1800 s fits hosted with 31% margin at the worst projection. The smallest
   figure with the #673 precedent's 10% margin is 1364 s.
5. **Fit, from the checker's own functions:**
   - On the head's 16 workers, the largest accepted figure is 936 s. Total slack is 202 s
     (24098 s demand against 24300 s capacity).
   - 1800 s fits no regular worker under any balance or worker count: 1800 + 122 = 1922 s alone,
     over 1620 s. The ceiling for any regular worker is 1498 s.
   - 1364 s on 16 workers exceeds total capacity by 262 s, so no rebalancing fits it.
   - 17 workers at 45 minutes accept up to 1498 s (1364 s → busiest regular worker 1605 s).
6. **Observation for a separate Issue, not acted on:** shard 10's two pieces run well over their
   registered `PIECE_SECONDS` on hosted (`milan_dp__3` 231 s registered, 354–419 s hosted;
   `pp_shadow__3` 347 s registered, 378–451 s hosted). The docs already say to refresh those
   predictions "from the next complete hosted run". The table under-predicts worker 10 regardless of
   `media_phase`.
7. **Observation:** `media_phase`'s `CASE_JOBS` defaults to 3 and the workflow does not set it, so on
   the 4-vCPU runner one vCPU is idle during the cases. CASE_JOBS 4 measured only 6% faster locally on
   the same 2-core x 2-SMT shape, so it does not change the fit.

## Options for the ruling (none taken)

- **(a) Default 1800 s on its own worker.** This needs a timeout-minutes change. It is not possible
  under the 1620 s rule, which is both the 60% bound of 45 minutes and the absolute rule in
  `headroom_problems`, so it also needs that rule changed or a second dedicated-worker exception like
  #737's.
- **(b) 1364–1498 s and a 17th worker at 45 minutes.** This keeps every timeout-minutes, but changes the
  workflow matrix and its generator, `ci_events.py --expect 16`, the `matrix.shard == 15 && 60`
  expression (the last worker's index), `WORKER_OVERHEAD_SECONDS` (16 → 17 entries, the new one being
  the 122 s allowance) and the CI_WORKFLOWS.md "sixteen workers" text.
- **(c) Raise regular timeout-minutes.** At 1364 s on 16 workers this needs at least 46 minutes and the
  absolute 1620 s rule raised to match.

## Changes
None. Nothing was committed.

## New checks and planted mutants
None. No change was made, so there is no new check.

## Resources / route timing
Not applicable: no RTL or constraint change, and no Vivado run.

## Gate table

| Gate | Result |
|---|---|
| `python3 scripts/suite_shards.py --selftest` at the unchanged head | rc 0, `selftest: PASS` (receipts/checker/suite_shards-selftest-a032c6d6.txt) |
| `media_phase` local, 3 runs | rc 0, PASS, 386 checks, 0 failures each |
| shard 10/16 local replica, run B (`run_all_suites.sh --ci-pieces --shard 10/16`, SUITE_TIMEOUT 3600) | rc 0, 4/4 PASS |
| `run_all_suites.sh --list`, full 4-shard sweep, lint, docs gates, behave | not run: STOP before any change, so there is nothing to validate |

## Harness notes (local only)
- Run A0 aborted in the cancellation preflight because `nohup` made the HUP control ignore SIGHUP.
  Later runs started with `setsid` alone.
- Run A's two pieces were refused because the scratch clone's `third_party/tsn-c-stack` origin was a
  local path. I fixed it to the canonical URL in the scratch clone only. The lane's own submodule was
  already canonical.
- The scratch clone `781-a671-measure` and the scratch logs live outside the tree and the output
  directory.
