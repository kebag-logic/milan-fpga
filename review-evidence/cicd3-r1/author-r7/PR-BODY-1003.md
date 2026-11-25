[A839]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Review findings answered](#review-findings-answered)** — Each open finding of rounds R923-1 and R924-1, the owner's ruling on acceptance 2, the manager's rulings on the two later findings, and where each is answered.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

`cicd-3` against `dev-soft-core`, head `9c62539365fea8316dae2b9fd7c68defeff5cb31`.

- The PR's nine commits sit on `fcbc31f3`, the head of PR #1001. #1001 has since merged into `dev-soft-core`
  (`2f2a8152`), so the diff against the base is these nine commits only.
- Every local gate this PR touches passes at the head in a clean clone: 37 of 37 commands (list in How to
  validate).
- **Hosted, at the head: all four runs are green.**
  - The `firmware-boundary` split's three jobs took 13.2, 14.1 and 5.5 minutes, with the whole run's verdict.
  - Every job this PR touches is within the bound with margin; leg A is stated (#737).
  - The jobs it does not touch are #1008, including two rtl-fast jobs over 30 minutes.
- **Receipts against the base: identical.** `milan_dp`'s `gptp` and `gptp-lat` receipts differed from the previous
  hosted run, because the base moved between the two runs: #995 re-pinned the gPTP processor (below). At one base
  they are identical with and without this change.
- The full serial sweep was not run in this lane; the candidate bank runs it.

## Linked Issue / roles

Relates to #998 (the CICD improvement lane). Stacked on #1001.

Executor: `[A839]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

Nine commits. Each was measured, and each kept every verdict identical.

1. **`66b092e1` Preflight once per head.**
   - A `verilator-preflight` job runs the sweep's eight preflight self-tests once, through
     `scripts/run_all_suites.sh --preflight-only`, beside the workers.
   - The workers run `--ci-pieces --no-preflight`. `--no-preflight` is refused without `--ci-pieces`, so the
     serial sweep, the physical leg and local runs keep their preflight.
   - `verilator-suites` needs the job, verifies its `suite-preflight` SHA record with `ci_events.py
     --require-target-sha --expect 1`, and is red unless the job's result is `success`.
   - Shard 9/19 replica: the first suite starts at +2 s instead of +535 s, with 134 CPU-s less. Logs and receipts
     are IDENTICAL.
2. **`f6c11a25` Stable mutant staging.** Every mutation driver (38) stages its planted RTL through
   `scripts/mutant_stage.py` at a path that is the same in every run, so a warm ccache answers the mutant model
   compiles. Warm hits: crf_rx 79/115 → 115/115 (−25 % CPU), avtp_rxmon depkt 37/48 → 48/48 (−64 %). Every mutant
   is still killed by the same named check.
3. **`13e6d869` Longest case first.** `scripts/ci_make_cases.py` starts a piece's cases longest first by a measured
   cost table (`CASE_SECONDS`), and prints and records them in driver order. milan_dp__0 through its driver:
   3411.9 s → 2711.8 s wall (−20.5 %), same instructions. Receipts are IDENTICAL.
4. **`d95e95e8` One lock domain for every staging slot, and a proved stage root** (R924-1-F1, R923-1-F1).
   - The lock is an exclusive `flock` on the slot directory's own inode, re-checked after locking, so every caller
     that names one physical directory meets one lock: any TMPDIR, a link to the parent, any user.
   - A slot owned by another user is never emptied or taken. A taken slot is emptied without following a link.
   - The root is created by one `mkdir(…, 0o700)` and proved by `lstat` (a real directory, the caller's, writable
     by nobody else, directly inside the resolved temporary directory, not swapped), or refused with its reason;
     the driver then stages at a random private directory, correct and merely cold.
   - `--selftest`: 17 controls, six with independent holder processes. Ten planted defects each fail it. The
     reviewers' collisions reproduce at the previous head and not at this one, with a real second uid. Five
     drivers' logs are identical, warm hits 100 %.
5. **`59f4f478` Re-key the dealer's figures from two complete hosted runs** (R923-1-F2).
   - Shard 1's 38.6 minutes was the runner: the same suites' identical builds took 1.36-1.40 times as long; on one
     host with equal bookings the head ran shard 1's pieces faster than the base, at equal instructions.
   - What made shard 1 the heaviest worker even at the base was a stale figure (#804): `milan_dp` leg 1 measured
     995 s against 508.
   - All 38 worker logs of runs 45383854694 and 45457006166 were measured with `suite_shards.py --measure`;
     `milan_dp`'s four legs carry their windows, and every other figure a window exceeded carries that window.
6. **`45d5c35a` Wording** (R924-1-R1, R923-1-R1, R923-1-R2).
7. **`feb03206` follow_ring and media_phase as CI cases.**
   - `tb/verilator/media_phase/Makefile` names the default run's five harness targets and each of `cases`'
     thirteen as a case (`ci-list`, `ci-receipts`, `ci-prepare`, `build-<case>`, `exec-<case>`). Each case prints
     what the default run prints for it.
   - `tb/verilator/follow_ring/Makefile` names its five default legs as three cases: `b8`; `pullin-small`
     (`pullin`, then `small-pullin`); `bind-settle` (`bind`, then `settle-control`). `small-pullin` and
     `settle-control` print no counted tally of their own, and a case must carry one. A leg's build prerequisite
     is now `$(LEG_BUILD)`, `build` by default, so a CI case runs a leg its piece has just built without
     rebuilding it. The serial `run` and every target's commands are unchanged (`make -n run` is the same).
   - `small_pulls.py` and `settle_control.py` printed each result from its worker thread as it finished. Their
     lines came in completion order and, once, two ran together on one line in a local piece. A receipt digests a
     case's output, so both now print the same lines from the main thread, in case order, after the pool. Two
     `make settle-control` runs at the head are byte-identical.
8. **`96df313f` The owner's 30-minute bound, by splitting and dealing** (the ruling on #998 acceptance 2).
   - **The budget.** `CI_BUDGET_SECONDS` = 1800 / 1.41 = 1276 s: 30 minutes on a runner 1.41 times as slow as the
     figures' runs (run 45481508309's slowest worker). It replaces the 1620-second rule for every regular worker.
     The 60 % rule stays for every worker.
   - **What exceeded it.** Six pieces exceeded 1276 s alone: `follow_ring` 1493, `media_phase` 1400 (round 4's
     list of five missed it), `capture_coherence__0` 1618 (refreshed below), `milan_dp_mclk__0` (leg A) 1408, and
     `milan_dp__0`/`__1` 1309/1313. `capture_coherence__1` (1204) exceeded it with the 122 s allowance.
   - **The splits**, with the planner's existing mechanisms only:
     - `milan_dp`: eight legs instead of four. `capture_coherence`: eight instead of four. Each new leg holds half
       of one old leg's cases.
     - `follow_ring`: two legs (`b8` + `bind-settle`; `pullin-small`). `media_phase`: three legs.
     - Workers: 19 → 26, because dealing alone could not: the figures total 28995 s, against 25 × 1154 s of
       room for the regular workers.
   - **Each new figure.** It is the old leg's hosted figure, or the whole suite's, times the ratio of local walls,
     new over old, measured concurrently on equal four-CPU bookings with hosted budgets and no compiler cache.
     Every derivation is in the table below. A new leg is a subset of one old leg, so where a light leg was not
     measured it would keep the old leg's figure; every leg was measured.
   - **The third complete run's windows.** Run 45481508309 exceeded thirteen figures. Those not re-dealt carry
     its window: `aaf_audio_loop` 22, `clkvalid` 18, `gptp_txts` 107, `i2spb` 15, `mbx` 299, `render_queue` 126,
     `shaper_core` 7, `tcam` 29, `milan_dp_mclk` leg 2 1051, `milan_dp_render` legs 0 and 1 620 and 90.
     `capture_coherence` legs 0 and 1 (1618, 1204) enter the new legs' derivation as their old legs' figures.
   - **The projection.** Regular workers project 1199-1275 s, the two heaviest (`milan_dp__1` alone, and
     `capture_coherence__5` with `pp_shadow__0` and `avtp_rxmon`) 1 s inside the budget. That is 525 s inside
     30 minutes at the figures' speed, and inside 30 minutes on a runner 1.41 times as slow.
   - **Leg A is the one worker over the budget, stated.** `milan_dp_mclk__0` alone projects 1530 s, its figure
     1408 s (the slowest of three hosted windows: 857, 1408, 779) plus 122. Its continuous history is indivisible
     (#737), so it keeps #737's explicit exception and its 60 % bound (2160 s). Splitting `milan_dp_mclk` to eight
     legs was measured: leg A's piece went from 720 to 669 s locally (−7 %, about 1309 s at its figure). That is
     still over the budget, and it costs four more pieces that each build both models, so `milan_dp_mclk` keeps
     four legs. On a runner 1.41 times as slow as the run that set its figure, leg A's worker would take
     about 36 minutes.
   - **Gates.** `suite_shards.py --selftest` refuses a regular worker over 1276 s. Its new controls: a 1276-second
     worker passes and a 1277-second one is refused under a wide timeout; leg A exactly at a 35-minute job's 60 %
     bound passes and one second over is refused; the budget equals 1800 / 1.41 rounded down, computed without the
     constant. Eight of nine planted defects are refused (the budget loosened to 1620, the rule removed, `>=`
     for `>`, the budget applied to leg A, 19 workers, four `milan_dp` legs, `follow_ring` whole, the 60 % rule
     removed). The ninth, loosening `ci_suite_pieces_selftest.py`'s own copy of the bound, is not visible at a
     compliant head; `suite_shards.py --selftest` holds the same bound.
   - CI_WORKFLOWS.md ("The #998 budget", the projection table), TESTING.md and RUNNING_TESTS.md say all this.

**The new figures and their derivation** (local walls in seconds; each pair ran concurrently on two four-CPU
bookings):

| Piece | Figure | Derivation |
|---|---:|---|
| `milan_dp__0` | 637 | 1309 × 463.8 / 953.5 (0/8 over 0/4) |
| `milan_dp__1` | 1153 | 1313 × 710.5 / 809.8 (1/8 over 1/4) |
| `milan_dp__2` | 145 | 275 × 148.2 / 281.7 |
| `milan_dp__3` | 220 | 399 × 221.6 / 403.1 |
| `milan_dp__4` | 1019 | 1309 × 741.6 / 953.5 (the `aclk` leg) |
| `milan_dp__5` | 362 | 1313 × 222.9 / 809.8 |
| `milan_dp__6` | 150 | 275 × 153.2 / 281.7 |
| `milan_dp__7` | 243 | 399 × 245.0 / 403.1 |
| `capture_coherence__0` | 1095 | 1618 × 581.6 / 859.7 |
| `capture_coherence__1` | 890 | 1204 × 467.0 / 632.2 (the faster of two 1/4 runs) |
| `capture_coherence__2` | 348 | 695 × 220.4 / 440.8 |
| `capture_coherence__3` | 411 | 724 × 235.6 / 415.4 |
| `capture_coherence__4` | 421 | 1618 × 223.5 / 859.7 |
| `capture_coherence__5` | 430 | 1204 × 225.6 / 632.2 |
| `capture_coherence__6` | 344 | 695 × 217.8 / 440.8 |
| `capture_coherence__7` | 453 | 724 × 259.9 / 415.4 |
| `follow_ring__0` | 589 | 1493 × 378.0 / 959.5 (piece over the whole suite) |
| `follow_ring__1` | 1075 | 1493 × 690.7 / 959.5 |
| `media_phase__0` | 489 | 1400 × 263.6 / 755.1 |
| `media_phase__1` | 487 | 1400 × 262.4 / 755.1 |
| `media_phase__2` | 524 | 1400 × 282.3 / 755.1 |

9. **`9c625393` rtl-fast's `firmware-boundary` within the same budget** (the ruling on #998 acceptance 2:
   `firmware-boundary` is a hosted job too, and must project at most 1276 s).
   - **What exceeded it.** Over the fourteen hosted rtl-fast runs 45147231523 to 45481508222 the job took
     1302-1667 s. Its projection by the workers' method was 1765 s: its slowest step, 1613 s, plus its slowest
     setup, 152 s. Its builders run one after another under one capture and are 1033-1366 s of each step; the
     judgement after them takes 197-247 s.
   - **The split, with the existing mechanisms** (a literal matrix, artifacts within one run, the aggregate's
     result list):
     - `ctrl_boundary.py --leg K/2 --capture-out DIR` runs only leg K's builders, by their own commands in
       `ctrl_configs.BUILDERS`, under a capture of their own at DIR, and judges nothing. `ctrl_runs.LEGS`: leg 0
       is the control gate's build; leg 1 is every other builder the run judges.
     - `firmware-boundary-capture` runs `leg: [0, 1]` (`fail-fast: false`, 30 minutes, firmware-boundary's
       setup). Each leg uploads `firmware-boundary-capture-<leg>-<sha>`.
     - `firmware-boundary` needs both legs, downloads each capture to the path its leg made it at, and runs the
       unchanged judge: `--selftest --without verilator --capture <leg 0> --capture <leg 1>`. The image builders,
       the stack's own gate, the 112 boundary controls, 192 pin controls and 4 figure controls run there, as
       before.
     - The `rtl-fast` aggregate needs `firmware-boundary-capture` and lists its result. A failed leg skips the
       judge, and the aggregate counts a skipped job as a pass.
   - **Required contexts, cancellation and fork safety are unchanged.** `rtl-fast` is still the one verdict.
     The watcher's expected jobs gain the two legs (generated). Each new job records its job evidence as every
     job does. Nothing new needs a token.
   - **The contract** (`ci_events.py`): both jobs' whole step lists are pinned, and `strategy` is allowed on the
     capture job only. `check_boundary_legs` holds the matrix exactly and as many legs as `ctrl_runs.LEGS`
     holds, plus the judge's need of the legs and both 30-minute limits. The RV32 arms cover the capture job too.
     Six new arms are each caught: a leg dropped, fail-fast, the judge without the need, either timeout raised,
     a third leg in the gate.
   - **Same verdict.** A local replica of the three jobs ran each in a fresh clone at one checkout path. Each
     capture passed through an artifact-like copy (hidden files left out, exec bits dropped). With the paths and
     seconds normalised, the judge's log equals the whole step's, except the eight builder lines the legs print.
     That holds through the final count: `4033 compiled sources of 4326 recorded invocations … 0 finding(s),
     112 boundary, 192 pin and 4 figure controls, 0 misbehaved`, `PASS`. Given one leg's capture alone, the
     judge exits 2 and names each builder of the missing leg. Every `--leg` refusal was run.
   - **Projections** (a figure is the slowest hosted window of that job's part of the step in the fourteen runs;
     a projection adds the slowest setup, 152 s):

     | Job | Figure | Projection |
     |---|---:|---:|
     | `firmware-boundary-capture` leg 0, the control gate's build | 769 s | 921 s |
     | `firmware-boundary-capture` leg 1, the other five builders | 597 s | 749 s |
     | `firmware-boundary`, the step less its builds | 247 s | 399 s |

   - CI_WORKFLOWS.md (the job list, the aggregate's list, "The #998 budget"), the firmware README, the gate's
     docstrings.

**Hosted runs at `9c625393`.** All four succeeded on their first attempt: rtl-full 45528738040, rtl-fast
45528738009, elaborate 45528738049, docs 45528737977. Every job's minutes are from the Actions jobs API
(`completed_at − started_at`). Each factor is the job over the median of its own earlier successful windows.

| Job | Minutes | Note |
|---|---:|---|
| `firmware-boundary-capture (0)` | 13.2 | the control gate's build 711 s (1.02 × its median) |
| `firmware-boundary-capture (1)` | 14.1 | five builders 774 s, on a slow runner (1.54 × median, 1.30 × the slowest earlier window) |
| `firmware-boundary` | 5.5 | `PASS` with the whole run's counts and controls |
| **`firmware-control-mutants`** | **38.8** | **over 30 minutes**: 1.39 × median, 0.99 × its slowest; 45-minute limit; untouched by this PR, #1008 |
| **`publication-census`** | **37.2** | **over 30 minutes**: 1.12 × median, 0.84 × its slowest; 45-minute limit; untouched by this PR, #1008 |
| Verilator shard 1/26 (the slowest worker) | 27.7 | 1.33 × its 1250-second projection |
| `firmware-aecp-mutants` | 26.3 | 1.30 × median |
| Verilator workers, all 26 | 389.0 job-minutes | round 5's projection about 385; 353.8 before. Leg A 14.1 minutes |
| Fail-fast watchers | 64.7, 54.6, 38.3, 26.3 | each waits for its whole run; a documented exception (#1008) |
| `split-cdc`, rtl-full's `Prepare pinned Yosys` | 14.2, 12.7 | each built Yosys from source on a tool-cache miss (735 s, 726 s); the key hashes the workflow files, which this PR changes, so this happens once after any workflow change |
| Yosys shards 1/4 and 2/4 | 5.1, 13.7 | 4.2 × and 10.5 × their medians, 1.07 × and 0.97 × their slowest windows. #995's new gPTP ROM invalidated every cached result (the ROM digest in each top's key covers `gptp_ucode.hex`), so `KL_pp_shadow` (237 s) and `KL_gptp_shadow` (631 s) were re-synthesised |

- **The judge's verdict matches the last whole-step run, 45481508222.** It printed the same counts, `4032 compiled
  sources of 4325 recorded invocations`, the same 112 boundary, 192 pin and 4 figure controls, and `PASS`. Its step
  output equals that run's, except the eight builder lines (printed by the legs) and one random temporary
  sysroot name.
- **firmware-boundary's runner-minutes.**
  - Before: 1461 s on average over fourteen runs, 1528 s at the previous head (26 billed minutes).
  - After: 792 + 848 + 328 = 1968 s, +35 % (35 billed minutes). The excess is two more setups and a slow leg-1
    runner; at the earlier runs' mean phases the cost is 1630 s, +12 %.
  - The family's wall span was 22.6 minutes, against 25.5.
- **No job got slower.** Against the slowest window of the same job in the 60 earlier successful runs, every job
  at the head is within it but four:
  - the new preflight, 116 s against 113;
  - Yosys shard 1/4, 307 against 288, explained in the table above;
  - `elaborate-gates-4`, 1422 against 1412;
  - `docs-gates-2`, 1389 against 1359.

  The last two are jobs this PR does not change (1-2 %, runner variance). The preflight's two earlier windows are
  this PR's own. Every touched job is within the bound:
  - the slowest Verilator worker took 27.7 minutes; shard 1 took 38.6 in the run R923-1-F2 cites;
  - the `firmware-boundary` family's jobs took 13.2, 14.1 and 5.5 minutes, 22.6 minutes of wall, where the single
    job took 25.5.
- **Round 5's deal, suite by suite against 45481508309.** These two runs tested different merges, so this is not
  yet a comparison against one base:
  - 45481508309 tested `45d5c35a` merged into `2509db68` (merge `dd5cf579`);
  - 45528738040 tested `9c625393` merged into `e608f8d8` (merge `241f036e`).

  Each worker's checkout log and every receipt's `head` field record these. Between them, `dev-soft-core` merged
  #995 (`e608f8d8`, 18 minutes before the second run): the `gptp-processor` gitlink `1616fc8f` → `1213ac5b`, the
  `gptp_shadow` testbench and the Yosys ROM digests. The two merge trees differ in this PR's 18 files and in
  #995's 25, and in nothing else.
  - Verdict lines are identical for 63 of 65 suites.
    - `capture_coherence` differs only in its per-leg tallies, with 44 checks in both runs.
    - `gptp_shadow`'s 11 verdict lines became 15: #995 added its #106/#107 phases (326 → 424 checks, four new
      mutants caught).
    - `follow_ring` and `media_phase` ran as new case suites.
  - Case receipts are identical for `capture_coherence` (4 → 8 legs), `maap`, `milan_dp_mclk`, `milan_dp_render`
    and `pp_shadow`, and for 24 of `milan_dp`'s 26 cases.
  - **`milan_dp`'s `gptp` and `gptp-lat` differ, and #995 is the cause.**
    - Both pass. One diagnostic line changed: `[#207] full-queue window: level 1, rp 0->0, wp 1->1` became `rp
      1->1, wp 2->2` (`tb/verilator/milan_dp/sim_gptp.cpp:1893`). It prints the gPTP engine's 2-bit event-queue
      pointers, the events queued and taken since reset modulo 4. Its check is relative (`rp1 == rp0 && wp1 ==
      wp0`). `1213ac5b` changes what the gPTP program queues before that arm, for example "Send a new master's
      first Announce in the handler that takes the role".
    - Locally, six trees were built: the base alone, this head, and the head before the deal (`45d5c35a`), each on
      `2509db68` and on `e608f8d8`. Two of the tree ids equal the two hosted merges'. Within each base, both
      binaries and every input are byte-identical across the three trees. Across bases, the gPTP image and both
      binaries differ.
    - The two cases ran 40 times: 28 direct runs under three CPU loads (one, then two, simulations per CPU), and 12
      inside CI pieces under both deals (0/4, 1/4, 0/8, 1/8). Each pin gave one output per case every time, and
      its sha256 is the hosted receipt's `output_sha256` for that pin. On `e608f8d8` the base and the head, under
      either deal, agree on every case they share; on `2509db68` the pre-change head and the head do too.
    - So the line is deterministic for its input, and against one base this change moves no receipt. Nothing is
      masked or excepted in any comparison.
  - No hosted run of the pre-change head at `e608f8d8` exists to set beside the head's. The local same-base runs
    are tied to the hosted runs by identical tree ids and output digests.

## Review findings answered

| Finding | Answer | Where |
|---|---|---|
| R924-1-F1 MAJOR: in-tree staging can erase a held slot across TMPDIRs | Fixed: one lock per physical slot directory; independent-process controls | `d95e95e8` |
| R923-1-F1 MINOR: stage root trusted without proof; lock keyed by an unresolved path | Fixed: root proved or refused with its reason; lock keyed by the resolved inode | `d95e95e8` |
| R923-1-F2 MINOR: shard 1 38.6 minutes | Attributed to the runner; stale `milan_dp` figures refreshed | `59f4f478` |
| R924-1-R1, R923-1-R1, R2 (wording) | Applied | `d95e95e8`, `45d5c35a` |
| R923-1-R3 (PR body wording) | Applied | — |
| #998 acceptance 2, the owner's ruling: every hosted job within 30 minutes, no runner-speed qualifier | Every regular worker projects within 1276 s (30 minutes on a 1.41× runner); leg A, indivisible, is stated over it | `feb03206`, `96df313f` |
| #998 acceptance 2, the manager's ruling on round 5's stop: rtl-fast's `firmware-boundary` is a hosted job too | Split into two capture legs and a judge; each projects within 1276 s | `9c625393` |
| #998 acceptance 2, the manager's ruling on round 6's finding 1: other hosted jobs over the bound | For this PR, the criterion is that every job the PR touches is within the bound with margin and no job gets slower; both hold (Hosted runs). The untouched jobs are [#1008](https://github.com/kebag-logic/milan-fpga/issues/1008). The four "Fail fast across this head" watchers span their run by design: a documented exception, recorded in #1008 with rtl-full's nightly physical gPTP job | — |
| #998 acceptance 1, the manager's ruling on round 6's finding 2: `milan_dp`'s `gptp` and `gptp-lat` receipts differ | The cause is the base, not the change and not nondeterminism. #995 re-pinned the gPTP processor between the two hosted runs. At one base the receipts are identical with and without this change, under either deal, and each pin's local output digest equals its hosted receipt | — |

## Authoritative references

- [CI_WORKFLOWS.md "Fast feedback"](../docs/testing/CI_WORKFLOWS.md#fast-feedback): `firmware-boundary` and `firmware-boundary-capture`, the aggregate's list.
- [CI_WORKFLOWS.md "Exhaustive validation"](../docs/testing/CI_WORKFLOWS.md#exhaustive-validation): the preflight job, the dealer, "The #998 budget", the figures and the projection table.
- [TESTING.md section 1](../docs/testing/TESTING.md#1-verilator-rtl-harnesses---tbverilator-the-live-regression): the two sweep modes, mutant staging, case start order.
- REQUIREMENTS.md REQ-VER-01, REQ-VER-04; Issue #998 acceptance 1 (identical outputs) and 2 (30-minute hosted jobs).

## How to get into the same state

```sh
git fetch origin cicd-3
git worktree add ../cicd-3-review origin/cicd-3
cd ../cicd-3-review
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
export VERILATOR_JOBS=4 SIM_JOBS=4 MAKEFLAGS='-j1 --no-print-directory'
```

## How to validate

```sh
python3 scripts/suite_shards.py --selftest          # every regular worker <= 1276 s, leg A <= 2160 s, the new controls
python3 scripts/ci_suite_pieces_selftest.py         # 65 parents, 94 units, the eight unions' omission controls
python3 scripts/ci_gate_workflows.py --check && python3 scripts/ci_events.py --check
python3 scripts/ci_make_cases_selftest.py           # media_phase's start-order names are live cases
make -s -C tb/verilator/follow_ring ci-list; make -s -C tb/verilator/media_phase ci-list
make -n -C tb/verilator/follow_ring run            # the serial run's commands, unchanged
python3 scripts/ci_suite_pieces.py run follow_ring__0 --receipts /tmp/r   # b8 and bind-settle, both pass
python3 scripts/mutant_stage.py --selftest && python3 scripts/test_suite_cancellation.py
python3 scripts/check_py_idiom.py
python3 scripts/ci_events.py --selftest            # includes the six boundary-leg arms and the capture job's RV32 arms
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --without verilator --leg 2/2 --capture-out /tmp/x   # refused, exit 2
# the hosted shape, at one checkout path (each command in a fresh clone there, as each hosted job is):
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --without verilator --leg 0/2 --capture-out "$T/firmware-boundary-capture-0"
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --without verilator --leg 1/2 --capture-out "$T/firmware-boundary-capture-1"
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator \
  --capture "$T/firmware-boundary-capture-0" --capture "$T/firmware-boundary-capture-1"   # PASS, the whole run's lines
```

Every command exits 0 at `9c625393` (the `--leg 2/2` refusal exits 2 by design), except the `follow_ring__0` piece. That ran, and passed, on the
work-in-progress tree with the same Makefiles, before `small_pulls.py` and `settle_control.py` printed in fixed
order; two `make settle-control` runs at the head are byte-identical. Also green at the head, in a clean clone: the `ci_gate_workflows`,
`ci_case_receipts`, `ci_maap_cases`, `ci_capture_cases`, `ci_suite_collect`, `ci_fail_fast`, `ci_runtime_evidence`,
`ci_install_cache`, `ci_workflow_plan` and `ci_manifest` self-tests; `generate_ci_evidence_pins --check`; the
gptp_shadow lifecycle test; the sh idiom, hygiene, naming, fail-fast, test-evidence and TODO ratchets; doc paths,
doc style, `docs_check`, archive, docs inventory, TOC and em-dash; `check_sweep_shape.py` and
`suite_tally.py --selftest`. That is 37 commands. Earlier rounds reported "36 of 36" for the same list, which has
35; the 36th and 37th are the last two named here.

Locally, on that work-in-progress tree, the five new pieces ran through `scripts/ci_suite_pieces.py run` on four
CPUs. Every case passed. Their
combined logs carry the same verdict lines and the same counted tallies as run 45481508309's whole-suite logs:
`follow_ring` 97 checks in 3 tallies, `media_phase` 386 in 28.

The hosted figures: read each job's minutes from the Actions jobs API (`completed_at − started_at`) for run
45528738040, and compare its receipts and logs per suite, whatever legs dealt them, with run 45481508309.
First read the merge each run tested: the checkout step's `HEAD is now at <merge> Merge <head> into <base>`,
or any receipt's `head`. Where the bases differ, a suite whose inputs the base changed is compared across
different inputs.

To hold the base for `milan_dp`'s two gPTP cases:

```sh
# T0: the base alone; T1: this head merged into the same base (git merge --no-ff 9c625393)
make -s -C tb/verilator/milan_dp ci-prepare build-gptp build-gptp-lat    # in each tree
sha256sum tb/verilator/milan_dp/obj_gptp/Vmilan_dp_gptp tb/verilator/milan_dp/obj_gptplat/Vmilan_dp_gptplat   # equal
make -s -C tb/verilator/milan_dp exec-gptp | sha256sum      # equal in both trees, and equal to the hosted receipt
                                                            # of a run on that base
```

## Known limitations / out of scope

- **Leg A** projects 1530 s, over the 1276-second budget; it is indivisible (#737). On a runner 1.41 times as slow
  as its figure's run it would take about 36 minutes. Making it faster needs a change to that leg or a faster
  runner class, outside this ruling.
- **Two workers sit 1 s inside the budget.** Their figures are local ratios applied to hosted maxima. The first
  hosted windows of the new pieces replace them (the documented refresh rule).
- **The first run after a workflow change rebuilds cached tools.** The Yosys and Verilator cache keys hash
  `.github/workflows/*.yml`, and this PR changes them. At `9c625393`:
  - rtl-full's "Prepare pinned Yosys" took 12.7 minutes, building from source;
  - rtl-fast's `split-cdc` took 14.2 minutes, building Yosys itself.

  Each is a one-time cost of any workflow change.
- **A base that changes a ROM re-synthesises every Yosys top once.** The result cache's key carries one ROM digest
  for every top, and it covers `gptp_ucode.hex`. So #995's re-pin made Yosys shards 1/4 and 2/4 re-synthesise
  `KL_pp_shadow` and `KL_gptp_shadow` (5.1 and 13.7 minutes, within their slowest earlier windows).
- **26 workers queue** behind the head's other workflows when runners are scarce; 25 waited 31 minutes here.
- **Jobs this PR does not touch, over the bound: [#1008](https://github.com/kebag-logic/milan-fpga/issues/1008).**
  - By the manager's ruling, #998 acceptance 2 means two things for this PR: every job it touches is within the
    bound with margin (the Verilator workers, the preflight and `firmware-boundary`), and no job gets slower. Both
    are shown above.
  - The untouched jobs over the bound are #1008's: rtl-fast's `publication-census` and `firmware-control-mutants`
    (over 30 minutes on ordinary runners), `firmware-unit` and three more firmware jobs, two docs workers and three
    elaborate workers. The elaborate workflow's projection of 1869-1968 s (CI_WORKFLOWS.md) is among them.
  - The four "Fail fast across this head" watchers span their run by design. They are a documented exception,
    with rtl-full's nightly physical gPTP job (#1008, "Documented exceptions").
- **Comparing two hosted PR runs compares two merges.** When the base moves between them, every suite whose inputs
  it changed is compared across different inputs. Round 6's comparison missed this for `milan_dp` and
  `gptp_shadow` (Hosted runs, above).
- **The capture artifacts** are about 46 MB zipped each, kept three days. The manifest collector downloads them
  too, as it downloads every artifact of the run, and reads none of their files.
- `ci/image/tool-inventory.json` and `exec-audit-receipt.json` still name `firmware-boundary`'s old step indices,
  as they did the old `rtl.yml`. No hosted workflow checks them; they are the image work's to regenerate.
- `WORKER_OVERHEAD_SECONDS` stays 122 s, though hosted workers measured 14-81 s outside their suites.
- Not run here: the act replay and the full serial sweep.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (acceptance 1: identical against one base, with `milan_dp`'s two differences explained by #995 and shown locally at one base; acceptance 2, as ruled for this PR: every touched job within the bound and none slower, leg A stated over the budget (#737), the untouched jobs in #1008). For reviewers to confirm
- [ ] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
