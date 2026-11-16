# HANDOFF — lane 925 ([A790]), round 2

**Status (21:5x CET 2026-11-16): round 2 done; REVIEW READY posted once on #925 (issuecomment-6929001329, REVIEW-READY-COMMENT.md).**
Head `09a948d4`: three commits on `16ba667d`, then one `--no-ff` merge of dev-soft-core `70f4056f`, which changes no
file. Not pushed. Ruling #925 issuecomment-6908876793 on round 1's STOP: the route misses are the base's, owed to
#927 (scope widened in #927 issuecomment-6908876362). No seeds or extra directives were run, and no further route is
owed, because the merge touches no gateware.

## 1. The merge

- `09a948d4` = `git merge --no-ff 70f4056f` (dev-soft-core, #901's merge of #895) onto `1be0a6c4`; no conflict.
- `70f4056f`'s tree is `16ba667d`'s (`ed63495c`), so the merge's tree is `1be0a6c4`'s (`a7ff40db`): the merge changes
  no file, and against dev-soft-core the diff is this lane's 11 files.

## 2. Rows re-measured

The merge affects no row: it changes no file (tree `a7ff40db` = `1be0a6c4`'s).
- **The legs.** Round 1's budget legs at both points ran at `a9f0dbc0`; `a9f0dbc0..09a948d4` touches only
  `srp_kind_mutants.py` (a line wrap) and `coverage.ratchet` (srp_mbx.c's counts), neither compiled.
- **The images.** Every image the legs and the routes used relinks byte-identical at `09a948d4`: budget 1x1
  `311430e7`, budget 8x8/1if `6d2a5d0e`, route 1x1 `e85cd3a5`, route 8x8 `b648575d` (receipts/identity/).
- **The harness's own reuse check.** `run.py --regrade` from a merge-head clone refuses: "reused build is stale:
  tree:firmware changed". Its firmware digest spans sw/firmware/ctrl, ctrl_nvm and gtest whole, so the two files
  above move it. Carrying by image identity is the practice the #901 lane used in its rounds 9 and 10.
- **The statement rows, re-run on the merge's clone:**
  - `flip_grade.py --check --point 1x1/1if` PASS, its rows identical to `1be0a6c4`'s (R4 13.25 of 20, R5 75.84 of 90,
    R6 73.36 of 90, first 14.72 of 20, last 136.65 of 140, R4L 203.57 of 238, ACMP 29.63, ADP 27.86, MAAP 27.96 of
    30, tx 34.00 of 49, txL 48.58 of 49).
  - `load_grade.py --check` PASS (1x1/1if 0.517 / 0.514 against 0.70).
  - `flip_grade.py --check` over every point exits 1 at 8x8/2if alone, which is reported and not held, as at the base
    (load 0.798, tx 104.25 ms).
- **The 8x8/1if stated-cost lines** (round 1's leg: 77 polls base up to 24,499 against 22,500; 3 ACMP items against
  5,500; 4 declined ACMP offers against 2,000) are #914's per-shape statements, as at the base (the ruling). None is
  SRP's. SRP's items are within at both points.
- No stated cost changes.

## 3. Routes (recorded per the ruling)

Both shapes' routes are **misses at the base, owed to #927** (ruling #925 issuecomment-6908876793; #927
issuecomment-6908876362 widens #927 to every split image at both shapes). No seeds or extra directives were run. No
further route is owed: the merge changes no gateware or image (section 2). Figures (Slow WNS / Fast WHS, ns; image
at `a9f0dbc0` = `09a948d4`'s):

| Shape | ExtraPostPlacementOpt (recipe) | ExtraTimingOpt | AltSpreadLogic_high |
|---|---|---|---|
| 1x1/1if | +0.024 / +0.036 | +0.008 / +0.023 | +0.177 / +0.023 |
| 8x8/1if | +0.011 / +0.034 | +0.171 / +0.014 | +0.215 / +0.014 |
| 1x1/1if at the base `16ba667d` | +0.208 / +0.014 | +0.260 / +0.014 | not run |

The receipts are round 1's: `round1/receipts/route/`.

## 4. Sweep

The 65 suites, in 4 shards, at `09a948d4`, each shard's command recorded by the recorded-gates runner:

| Shard | Recorded rc | Suites | Passed | Failed | Timed out | Checks | Run |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 15 | 15 | 0 | 0 | 361,003 | sweep3, `-j4`, 4,040 s |
| 1 | 1 | 17 | 14 | 1 (`gptp_shadow`) | 2 (`milan_dp_gm_steps`, `milan_dp_render`) | 2,046,218 | sweep3, `-j4`, 9,122 s |
| 1, the three re-run | 0 | 3 | 3 | 0 | 0 | | sweep6/rr, uncontended: 241, 695, 908 s |
| 2 | 0 | 17 | 17 | 0 | 0 | 284,233 | sweep5/s2, the hosted 4-core budget, 3,735 s |
| 3 | 0 | 16 | 16 | 0 | 0 | 21,575 | sweep5/s3rr, `-j4`, 4,987 s |

- Every suite has a recorded pass; the shards' tallies total 2,713,029 checks, 0 in-suite failures.
- Shard 1's three not passed were the host's contention (load average 300 to 950 on 128 CPUs):
  - `gptp_shadow`: its 325 checks passed; its `lifecycle` target overran a fixed 12 s subprocess timeout.
  - `milan_dp_gm_steps` and `milan_dp_render`: cut by the 1,800 s wall clock.
  - Each was re-run one at a time in a clean clone with the driver's per-suite logic (`rerun_suites.sh`:
    `timeout make`, then `suite_tally.py --verdict`), at the default wall clocks; each passed within them.
- Shard 2 ran with the hosted verilator-suites job's own budget (`VERILATOR_JOBS=4 SIM_JOBS=4 CI_CAMPAIGN_JOBS=4`;
  rtl.yml, "Set CPU-derived job budgets"). Without it, `capture_coherence` builds with every core the host has and
  overran the 10G unit cap three times (section 7).
- Runs the host cut (OOM kills, the 15:40 power cycle, the 18:46 crash, the 19:39 shutdown) recorded no rc. Their
  output is set aside in scratch (`sweep2-oom/`, `cut-1540/`, `cut-1846/`, `cut-1939/`) and is not cited.
- Receipts: `receipts/sweep/` (summaries, results.json, specs, a sha256 manifest of every suite log, shard 1's three
  logs and their re-runs).

## 5. Gate table

`1be0a6c4` has the merge's tree, so its results are `09a948d4`'s. Gates at `a9f0dbc0` carry by section 2. Round 1's
receipts: `round1/receipts/`.

| Gate | Head | Result |
|---|---|---|
| Merge, `--no-ff` of 70f4056f | 09a948d4 | no conflict; tree = 1be0a6c4's; `git diff --check` rc 0; four one-line commits, no body, no trailer |
| Image identity (budget 1x1, 8x8/1if; routes 1x1, 8x8) | 09a948d4 vs a9f0dbc0 | 4 of 4 byte-identical |
| flip_grade --check --point 1x1/1if | 09a948d4 | PASS, every row within its bound |
| load_grade --check | 09a948d4 | PASS, 0.517 / 0.514 vs 0.70 |
| flip_grade --check (every point) | 09a948d4 | rc 1 at 8x8/2if alone, reported not held, as at the base |
| Budget 1x1/1if | a9f0dbc0 (carried) | rc 0: 96 groups, 0 refusals, 0 passes over the share, 7 backlog-owed misses (pre-existing) |
| Budget 8x8/1if | a9f0dbc0 (carried) | STATED lines only: #914's per-shape statements, as at the base; SRP's items within |
| Firmware self-test shards 0-3 | a9f0dbc0, SRP shard at 1be0a6c4 | PASS; 716/716, 299, 441 caught, 0 escaped |
| fw_coverage --check | a9f0dbc0, again in firmware-unit at 1be0a6c4 | PASS, srp_mbx.c 741/741, 671/671 |
| Workflow replays rtl-fast, elaborate, docs | a9f0dbc0; docs, firmware-unit, changes at 1be0a6c4 | every step rc 0 or not run with a reason |
| plat_ledger, test_ctrl_memory | a9f0dbc0 | PASS |
| Release image | 16ba667d vs a9f0dbc0 | byte-identical |
| Routes (both shapes) | a9f0dbc0 = 09a948d4's image | misses at the base, owed to #927 (section 3) |
| Sweep, 65 suites, 4 shards | 09a948d4 | every suite a recorded pass (section 4) |

## 6. Run history

- 07:12 resume; ruling and #927's widening read; HEAD 1be0a6c4 clean, no units; dev-soft-core fetched (tip 70f4056f).
- 07:1x merge `09a948d4`.
- 07:1x image identity at the merge head (4 images byte-identical); budget regrade from merge-head clones refused
  (tree:firmware digest, see section 2); flip check, load gate re-run on the merge's clone.
- 07:22 sweep, serial (MemAvailable 28 GB, under the 30 GB the four parallel shards need), one unit, MemoryMax 10G,
  `MAKEFLAGS=-j6`, on 64-79.
- 07:43 that unit was OOM-killed at its 10G MemoryMax in `capture_coherence` (journal: "The kernel OOM killer killed
  some processes in this unit", 10G memory peak); 11 suites had passed. Noticed 08:01 (the unit wrote no rc).
- 08:01 the sweep restarted on a fresh clone at `-j4` (the shard tool's width under the same cap), as the four shards
  in sequence in one recorded spec (`--shard k/4`, k = 0..3), on 0-7.

## 7. Incidents

- 21:00-21:51 the re-runs (rc 0, 21:31) and shard 2 (rc 0, 21:51) completed: every suite a recorded pass.

- 12:11 the sweep unit was OOM-killed a second time, again in `capture_coherence`, in its model build
  (`make: *** [Makefile:82: build] Terminated`; journal: oom-kill, 10G memory peak). Its build needs more than 10G at
  `-j4`. Missed for 18 minutes: my wait loop then watched only for an rc file and a shard's END line. The completion
  (sweep4/spec.json): shard 3 through the driver at `-j4`, then shard 2's suites from `capture_coherence` on with the
  driver's per-suite logic (`capture_coherence` at `-j2`, wall clock 3,600 s), then shard 1's three re-runs. It waits
  for a CPU range and MemAvailable >= 20 GB (12:3x: 11-13 GB available, load near 1,000, no range).

- The first sweep's OOM kill (above): `-j6` was too wide for `capture_coherence` under 10G. Its logs are kept in
  scratch `sweep2-oom/`; nothing from it is cited as evidence.
- Two regrade units picked 80-87 a second apart; both refused at once on the stale digest, so no CPUs were shared.
- 12:0x the sweep's pace under the host load (load average 300 to 950): shard 0 67 min, shard 1 152 min; shards 2 and 3
  and the re-runs are expected to run past the 14:00 tripwire. REVIEW READY follows them (no comment before).
- 14:27 the completion (sweep4) started on 80-87; 15:40 the host was power-cycled (a memory upgrade to 82 GiB); every
  unit was cut. Cut work, no rc recorded, set aside in scratch `cut-1540/` (shard 2's OOM'd logs, shard 3's 12
  partial logs, sweep4's runner output); nothing from it is cited.
- 16:39 resume: tree clean at `09a948d4`, no units; shards 0 and 1 have recorded rcs (0, 1) and stand. Re-run as
  `sweep5`: shard 2 at `-j2` on a fresh clone (16-23, from 16:41); shard 3 at `-j4` then shard 1's three re-runs
  (gptp_shadow, milan_dp_gm_steps, milan_dp_render, default wall clocks) in the cleaned sweep clone, one unit
  (24-31, from 17:13; two earlier picks lost their range to other lanes before the start).
- 17:17 shard 2 (sweep5) OOM-killed at 10G in `capture_coherence` a third time, at `-j2`. The cause: its Makefile's
  `VERILATOR_JOBS ?= 0` lets Verilator build with every core it sees (the host's 128, whatever the unit's 8-CPU
  affinity), and its mutation driver builds concurrently. The hosted job sets `VERILATOR_JOBS` and `SIM_JOBS` to the
  runner's cores (rtl.yml, verilator-suites, "Set CPU-derived job budgets"); my sweeps never did. 17:21 shard 2
  re-run on a cleaned clone with the hosted 4-core budget (`VERILATOR_JOBS=4 SIM_JOBS=4 CI_CAMPAIGN_JOBS=4`,
  `MAKEFLAGS=-j4`) on 80-87: `capture_coherence` 42 of 42 PASS at 18:1x, no OOM.
- 18:3x shard 3 (sweep5, s3rr) recorded rc 0: 16 of 16, 21,575 checks, 4,987 s. Then its re-runs: `gptp_shadow`
  passed uncontended (make rc 0, verdict clean, 388 s); `milan_dp_gm_steps` was running.
- 18:46 the host hard-reset (rebooted 19:06). Cut, no rc recorded, set aside in scratch `cut-1846/`: shard 2's
  sweep5 re-run (15 of 17 suites run, `capture_coherence` passed in it) and the re-run command (its `gptp_shadow`
  pass is not cited, the command recorded no rc). No output file of the lane was torn (none empty, none written
  after 18:30); the tree is clean, `git fsck` clean.
- 19:09 both re-run on cleaned clones with the hosted 4-core budget (`VERILATOR_JOBS=4 SIM_JOBS=4
  CI_CAMPAIGN_JOBS=4`, `-j4`): shard 2 (sweep5/s2, on 40-47) and the three re-runs (sweep6/rr, in the cleaned
  sweep clone, on 0-7).
- 19:39 host shutdown for maintenance (back 19:43): shard 2 (sweep5/s2) and the re-runs (sweep6/rr) cut again, no
  rc; their output set aside in scratch `cut-1939/` (the re-runs' `gptp_shadow` had passed again, 294 s; not cited).
  No torn output file; tree and `git fsck` clean. Both clones cleaned again.
- 19:44-20:48 every CPU range was booked by other lanes (budget legs, another sweep). 20:48 shard 2 on 48-55; 21:00
  the re-runs on 8-15, both with the hosted 4-core budget.
- 21:5x REVIEW READY posted once on #925 (issuecomment-6929001329). No unit of this lane runs.

## 8. For the manager

- Push `925-srp-ta-tf` at `09a948d4` (four commits on `16ba667d`: the three of round 1, then the `--no-ff` merge of
  `70f4056f`); open the PR against dev-soft-core with round2/PR-BODY.md.
- Not this change's, recorded as found:
  - the route misses, owed to #927;
  - the 8x8/1if STATED lines, #914's per-shape statements;
  - three stale AECP lines in `coverage.ratchet`;
  - `srp_mbx.cpp`'s two startup tests at the 8x8 entity;
  - `capture_coherence`'s `VERILATOR_JOBS ?= 0` outside CI, which builds with every host core.
- Scratch: `/data-2/milan/tmp/925-a790` (about 10 GB); sweep clone `$LANES/925-a790r2-sweepb`.
