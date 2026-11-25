[A839]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Review findings answered](#review-findings-answered)** — Each finding of rounds R923-1, R924-1, R923-2 and R924-2, the owner's ruling on acceptance 2, the manager's rulings on the two later findings, and where each is answered.
- **[How a failed capture leg cancels its sibling on a fork](#how-a-failed-capture-leg-cancels-its-sibling-on-a-fork)** — The native matrix mechanism, what it needs, and what is and is not shown.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

`cicd-3` against `dev-soft-core`, head `b0f2bc1a784d9f006204491c883ac2b1783e970a`.

- The PR's twelve commits sit on `fcbc31f3`, the head of PR #1001. #1001 has since merged into `dev-soft-core`
  (`2f2a8152`), so the diff against the base is these twelve commits only.
- The last three answer round 2's reviews: `firmware-boundary-capture` keeps GitHub's own `fail-fast: true`
  (R924-2-F1); follow_ring's two fine-build lines are recursive again, so `make -n run` is the base's byte for
  byte and no pipe jobserver warns (R923-2-F1); and the wording residues.
- Every local gate this PR touches passes at the head in a clean clone: 37 of 37 commands (list in How to
  validate).
- **Hosted, at the head: all four runs are green on their first attempt** (45550366428, 45550366444,
  45550366332, 45550366343).
  - The `firmware-boundary` split's three jobs took 15.3, 11.0 and 5.0 minutes, with the whole run's verdict.
  - Every job this PR touches is within 30 minutes; the slowest, a Verilator worker, took 25.0 including a
    Verilator rebuild on a cache miss. Leg A took 14.1 and is stated (#737).
  - The jobs it does not touch are #1008, including three rtl-fast jobs over 30 minutes at this head.
- **Receipts against one base, hosted: identical.** These runs and the previous head's both merged into
  `e608f8d8`. All 8 case suites' receipts and all 65 suites' verdict lines are identical (below). That includes
  `milan_dp`'s `gptp` and `gptp-lat`, whose earlier difference came from #995's base change.
- The full serial sweep was not run in this lane; the candidate bank runs it.

## Linked Issue / roles

Relates to #998 (the CICD improvement lane). Stacked on #1001.

Executor: `[A839]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

Twelve commits. Each was measured, and each kept every verdict identical.

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
     rebuilding it. As first committed here, the two fine-build lines reached `$(MAKE)` only through a variable,
     so make did not treat them as recursive: `make -n run` stopped showing the fine build, and under a pipe
     jobserver the serial run warned (R923-2-F1). Item 11 fixes that; at the head the serial `run` and every
     target's commands are the base's (`make -n run` is byte-identical).
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
     - `firmware-boundary-capture` runs `leg: [0, 1]` (`fail-fast: true` since item 10, 30 minutes,
       firmware-boundary's setup). Each leg uploads `firmware-boundary-capture-<leg>-<sha>`.
     - `firmware-boundary` needs both legs, downloads each capture to the path its leg made it at, and runs the
       unchanged judge: `--selftest --without verilator --capture <leg 0> --capture <leg 1>`. The image builders,
       the stack's own gate, the 112 boundary controls, 192 pin controls and 4 figure controls run there, as
       before.
     - The `rtl-fast` aggregate needs `firmware-boundary-capture` and lists its result. A failed leg skips the
       judge, and the aggregate counts a skipped job as a pass.
   - **Required contexts, cancellation and fork safety.** `rtl-fast` is still the one verdict. The watcher's
     expected jobs gain the two legs (generated). Each new job records its job evidence as every job does.
     Nothing new needs a token. As first committed, the matrix set `fail-fast: false`, which broke the
     policy that every hosted matrix keeps native cancellation (R924-2-F1). Item 10 restores it.
   - **The contract** (`ci_events.py`): both jobs' whole step lists are pinned, and `strategy` is allowed on the
     capture job only. `check_boundary_legs` holds the matrix exactly and as many legs as `ctrl_runs.LEGS`
     holds, plus the judge's need of the legs and both 30-minute limits. The RV32 arms cover the capture job too.
     Seven arms are each caught: a leg dropped, cancellation disabled (`fail-fast: false`), `fail-fast` left to
     the default, the judge without the need, either timeout raised, a third leg in the gate.
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
10. **`468c7e47` Native fail-fast on the capture matrix** (R924-2-F1).
    - `firmware-boundary-capture`'s `strategy` is `fail-fast: true` in the template and in the generated
      `rtl-fast.yml`, as `rtl.yml`'s two matrices already are. The fork guard on the watcher and the fail-closed
      aggregate are unchanged.
    - `ci_events.py`: `FIRMWARE_BOUNDARY_STRATEGY` holds `fail-fast: True`. The arm that expected `true` to be
      refused now plants `false` and is caught ("cancellation disabled"); a new arm removes the key and is caught
      too ("left to the default"), so the value stays spelled out. 5967 → 5968 arms.
    - Planted in a clean clone and refused by `ci_events.py --check`: `false` in the template, regenerated; the key
      removed, regenerated. `false` in the generated file alone is refused by both `ci_gate_workflows.py --check`
      ("regenerate the gate jobs") and `ci_events.py --check` (the generated jobs' inventory).
    - R924-2's own probe, unchanged, now fails at its assertion that `false` is production; its inverse passes.
    - CI_WORKFLOWS.md (the capture legs' paragraph), the template's comment and the checker's docstring say so.
    - How the cancellation works on a fork is in its own section below.
11. **`222362ff` follow_ring's fine build is a recursive make line again** (R923-2-F1).
    - `small-pullin`'s `+$(if $(LEG_BUILD),$(FINE_BUILD))` and `build-pullin-small`'s `+$(FINE_BUILD)`: GNU make
      treats a line as recursive only if it starts with `+` or names `$(MAKE)` itself. The Makefile's comment says
      why.
    - R923-2's `follow_ring_make_probe.sh`, with this head added to its head list, against the base `13e6d869`
      (both trees by `git archive`):
      - GNU make 4.4.1, `make -j4 --jobserver-style=pipe small-pullin`: base 0 warnings, head 0. At
        `9c625393` the same probe gives head 1 warning.
      - GNU make 4.3 (pipe jobserver only), `make -j4 small-pullin`: base 0, head 0; at `9c625393`, head 1.
        This is the case the review could only infer.
      - `make -n run`: IDENTICAL under both versions (sha256 `f5c44c63…` for both trees); at `9c625393`,
        DIFFERS.
      - The two `small-pullin` transcripts differ only in the stub run's traceback and Makefile line numbers.
        The probe builds no model, so `small_pulls.py` fails on purpose there.
    - `make -n exec-pullin-small` (with `LEG_BUILD=` empty) runs `pullin`, then `small_pulls.py`, and builds
      nothing. `make -n build-pullin-small` builds both models.
    - Both `follow_ring` CI pieces, run at the head in a clean clone as a hosted worker runs them
      (`ci_make_cases.py --suite follow_ring --shard L/2 --jobs 2`, eight CPUs): see the hosted section and the
      receipt comparison below.
12. **`b0f2bc1a` Wording** (R924-2-R1, R924-2-R2, R923-2-R1).
    - R924-2-R1: `Issue #998; REQ-VER-01 and REQ-VER-04.` added to each listed explanatory block: the follow_ring
      Makefile's leg-build block, `small_pulls.py`'s and `settle_control.py`'s print-order comments, the
      template's capture-job block, `ctrl_boundary.py`'s THE CAPTURE paragraph, `ctrl_configs.py`'s known-set
      block, `ctrl_runs.py`'s THE LEGS paragraph, and the six boundary-leg blocks in `ci_events.py`.
    - R924-2-R2: `sw/firmware/ctrl/README.md` now opens with the sentence as written: "Those standalone builders
      run in firmware-boundary-capture; firmware-boundary still runs its owned image builders, the stack gate and
      controls, then judges the joined captures." The leg and argument explanation follows unchanged.
    - The same overbroad phrase was in `docs/testing/CI_WORKFLOWS.md` ("`firmware-boundary` needs both legs and
      runs no builder itself"). It now says "runs none of their builders itself", since the next sentence there
      lists the image builders and the stack's gate it does run. No review named this sentence.
    - R923-2-R1: CI_WORKFLOWS.md now says each new piece's figure "is in PR #1003's description (its derivation
      table)", as written.

**Hosted runs at `b0f2bc1a`.** All four succeeded on their first attempt: rtl-full 45550366428, rtl-fast
45550366444, elaborate 45550366332, docs 45550366343. Each tested `b0f2bc1a` merged into `e608f8d8` (merge
`c5327b25`), the same base as the previous head's runs (`241f036e` = `9c625393` into `e608f8d8`). So this pair
is a hosted comparison against one base. Every job's minutes are from the Actions jobs API (`completed_at −
started_at`). Each factor is the job over the median, and over the slowest, of its own earlier successful
windows in 64 runs (the previous head's four included).

| Job | Minutes | Note |
|---|---:|---|
| `firmware-boundary-capture (0)` | 15.3 | the control gate's build; 1.16 × its one earlier window (13.2) |
| `firmware-boundary-capture (1)` | 11.0 | five builders; 0.78 × its earlier window (14.1) |
| `firmware-boundary` | 5.0 | `PASS`, `4032 compiled sources of 4325 recorded invocations`, 0 findings, 112 boundary, 192 pin and 4 figure controls, as at `9c625393` |
| `rtl-fast` (the aggregate) | 0.3 | success |
| Verilator preflight | 1.9 | 117 s against its slowest earlier 116 |
| Verilator shard 2/26 (the slowest worker) | 25.0 | `mmcm_servo` alone: 405 s building Verilator on a cache miss, then 1058 s of suite |
| Verilator shard 9/26 | 24.3 | no rebuild; its suite step 1436 s against 947 at `9c625393`, on unchanged suites |
| Verilator workers, all 26 | 397.6 job-minutes | 389.0 at `9c625393`; seven workers built Verilator on a cache miss (278-405 s each) |
| Unions, `verilator-suites`, `yosys-portability` | at most 0.5 | all success |
| rtl-full's `Prepare pinned Yosys` | 17.4 | built Yosys from source on a cache miss (1024 s), within its slowest earlier window (1084 s) |
| **`publication-census`** | **36.7** | **over 30 minutes**: 1.03 × median, 0.83 × its slowest; untouched by this PR, #1008 |
| **`firmware-srp-mutants`** | **30.5** | **over 30 minutes**: 1.39 × median, 1.33 × its slowest; untouched, #1008. Its campaign step took 1789 s here and 1233 s at `9c625393`, whose inputs differ from this head's only in comments |
| **`firmware-control-mutants`** | **30.1** | **over 30 minutes** by 6 s: 1.07 × median, 0.77 × its slowest; untouched, #1008 |
| `firmware-unit` | 29.2 | untouched; 1.28 × median, 0.98 × its slowest |
| Fail-fast watchers | 110.9, 90.9, 44.5, 36.4 | each waits for its whole run, here including about 25 minutes of queueing; a documented exception (#1008) |

- **Against one base, every receipt and verdict is identical.** The suite-by-suite comparison of rtl-full
  45528738040 (`9c625393`) and 45550366428 (`b0f2bc1a`), both merged into `e608f8d8`:
  - case tables identical for all 8 case suites: `capture_coherence` 43 cases, `follow_ring` 3, `maap` 66,
    `media_phase` 18, `milan_dp` 26 (`gptp` and `gptp-lat` included), `milan_dp_mclk` 36, `milan_dp_render`,
    `pp_shadow`;
  - verdict line sets identical for 65 of 65 suites; 0 problems.
- **follow_ring's two pieces, locally, as a hosted worker runs them** (`ci_make_cases.py --suite follow_ring
  --shard L/2 --jobs 2`, eight CPUs, shared compiler cache, a clean clone each): both pass at `b0f2bc1a` (351 s,
  465 s) and at `9c625393` (351 s, 472 s). The three case receipts (outcome, rc, `output_sha256`) are equal in
  both trees, and equal to run 45528738040's hosted receipts. Each piece built its models first and its exec
  phase rebuilt nothing.
- **Every job this PR touches is within 30 minutes.** The slowest is the Verilator worker at 25.0 minutes,
  including its tool rebuild. Three untouched rtl-fast jobs ran over 30 minutes; they are #1008's.
- **"No job got slower" does not hold at this head for every job.** The untouched `firmware-srp-mutants` and
  Verilator shard 9's unchanged suites ran 1.33 × and 1.52 × their earlier windows on the same inputs, and seven
  workers rebuilt Verilator. Neither is caused by this change: the same work at `9c625393` ran in the times
  quoted above, and the rebuild happens once after any workflow change. Worker 2's single earlier window is 852 s.
- **The previous head's runs** (rtl-full 45528738040, rtl-fast 45528738009, elaborate 45528738049, docs
  45528737977) are described in rounds 6 and 7. Their comparison with run 45481508309 crossed a base change
  (#995's gPTP re-pin), which explains `milan_dp`'s `gptp`/`gptp-lat` and `gptp_shadow` differences there. At
  one base, hosted, those receipts are now shown identical (above).

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
| #998 acceptance 2, the manager's ruling on round 6's finding 1: other hosted jobs over the bound | For this PR, the criterion is that every job the PR touches is within the bound with margin and no job gets slower. The first holds at `b0f2bc1a`. The second held at `9c625393`; at `b0f2bc1a`, two jobs ran slower than their earlier windows on unchanged work (runner speed), and seven workers rebuilt Verilator once after the workflow change (Hosted runs). The untouched jobs are [#1008](https://github.com/kebag-logic/milan-fpga/issues/1008). The four "Fail fast across this head" watchers span their run by design: a documented exception, recorded in #1008 with rtl-full's nightly physical gPTP job | — |
| #998 acceptance 1, the manager's ruling on round 6's finding 2: `milan_dp`'s `gptp` and `gptp-lat` receipts differ | The cause is the base, not the change and not nondeterminism. #995 re-pinned the gPTP processor between the two hosted runs. At one base the receipts are identical with and without this change, under either deal, and each pin's local output digest equals its hosted receipt | — |

| R924-2-F1 MINOR: the capture matrix disables the fork-safe cancellation mechanism | Fixed: `fail-fast: true` in template, generated workflow, contract constant and its arm; planted `false` and a removed key are refused | `468c7e47`; the section below |
| R923-2-F1 MINOR: follow_ring's fine build is no longer a recursive make line | Fixed: both lines start with `+`; `make -n run` byte-identical to the base's and 0 pipe-jobserver warnings, under make 4.4.1 and 4.3 | `222362ff` |
| R924-2-R1, R924-2-R2, R923-2-R1 (wording) | Applied as written | `b0f2bc1a` |
| R923-2-S1 to S3, R924-2's retained R923-1-S1 to S3 (optional) | Not adopted in this PR: no defect is claimed; each stays open for the reviewers or a later issue | — |
| R923-2-S4 (optional): the derivation table's walls are rounded to 0.1 s, so `milan_dp__1` reproduces as 1152, not 1153 | Not adopted: the tree's figure is the ceiling of the unrounded walls, which is conservative, as the review says | — |

## How a failed capture leg cancels its sibling on a fork

- **The mechanism is GitHub's, not a job's.** `strategy.fail-fast: true` is applied by the Actions service that
  runs the workflow. When one job of a matrix fails, the service cancels that matrix's other jobs that are queued
  or running. No step runs for it and no token is used, so a fork's read-only token and its missing secrets do not
  matter. It is the same mechanism `rtl.yml`'s two Verilator and Yosys matrices use, and CI_WORKFLOWS.md says
  every hosted matrix keeps it, fork PRs included.
- **On a fork, nothing else changes.** The `ci-fail-fast` watcher, the only job with a write token, still runs only
  for a push or a same-repository pull request (its `if`, unchanged). A fork never enters it, and the capture
  legs get no `permissions` of their own.
- **The verdict stays red.** The matrix's result, as its dependants read it, is `failure` when a leg failed.
  - `firmware-boundary` needs it and is skipped.
  - The `rtl-fast` aggregate reads `needs.firmware-boundary-capture.result` and fails on anything but `success`
    or `skipped`.
  - A cancelled sibling never reports `success`. The aggregate is not weakened, and its list is unchanged.
- **On a same-repository event**, the native cancellation acts inside the matrix, and the watcher still cancels
  the head's other workflows, as before.
- **What is shown, and what is not.** The contract check holds `fail-fast: true` exactly, and the planted `false`
  and removed key are refused (item 10). The fork guard is unchanged and checked by `ci_fail_fast_selftest.py`
  ("fork zero-write"). No hosted leg failure was injected: that needs a failing commit on a fork, which this
  round did not push.

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
make -n -C tb/verilator/follow_ring run            # the serial run's commands, byte-identical to 13e6d869's
python3 scripts/ci_suite_pieces.py run follow_ring__0 --receipts /tmp/r   # b8 and bind-settle, both pass
python3 scripts/mutant_stage.py --selftest && python3 scripts/test_suite_cancellation.py
python3 scripts/check_py_idiom.py
python3 scripts/ci_events.py --selftest            # 5968 arms: the seven boundary-leg arms and the capture job's RV32 arms
sh follow_ring_make_probe.sh <repo> <out>           # R923-2's probe, this head in its head list: IDENTICAL, 0 warnings
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --without verilator --leg 2/2 --capture-out /tmp/x   # refused, exit 2
# the hosted shape, at one checkout path (each command in a fresh clone there, as each hosted job is):
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --without verilator --leg 0/2 --capture-out "$T/firmware-boundary-capture-0"
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --without verilator --leg 1/2 --capture-out "$T/firmware-boundary-capture-1"
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator \
  --capture "$T/firmware-boundary-capture-0" --capture "$T/firmware-boundary-capture-1"   # PASS, the whole run's lines
```

Every command exits 0 at `b0f2bc1a` in a clean clone (the `--leg 2/2` refusal exits 2 by design; the `ctrl_boundary.py` legs and judge were run at `9c625393`, and the delta since touches only their comments). Both `follow_ring` pieces ran at the head, as a hosted worker runs them, and passed. Also green at the head, in a clean clone: the `ci_gate_workflows`,
`ci_case_receipts`, `ci_maap_cases`, `ci_capture_cases`, `ci_suite_collect`, `ci_fail_fast`, `ci_runtime_evidence`,
`ci_install_cache`, `ci_workflow_plan` and `ci_manifest` self-tests; `generate_ci_evidence_pins --check`; the
gptp_shadow lifecycle test; the sh idiom, hygiene, naming, fail-fast, test-evidence and TODO ratchets; doc paths,
doc style, `docs_check`, archive, docs inventory, TOC and em-dash; `check_sweep_shape.py` and
`suite_tally.py --selftest`. That is 37 commands.

Locally, on that work-in-progress tree, the five new pieces ran through `scripts/ci_suite_pieces.py run` on four
CPUs. Every case passed. Their
combined logs carry the same verdict lines and the same counted tallies as run 45481508309's whole-suite logs:
`follow_ring` 97 checks in 3 tallies, `media_phase` 386 in 28.

The hosted figures: read each job's minutes from the Actions jobs API (`completed_at − started_at`) for run
45550366428, and compare its receipts and logs per suite, whatever legs dealt them, with run 45528738040 (the
same base, `e608f8d8`).
First read the merge each run tested: the checkout step's `HEAD is now at <merge> Merge <head> into <base>`,
or any receipt's `head`. Where the bases differ, a suite whose inputs the base changed is compared across
different inputs.

To hold the base for `milan_dp`'s two gPTP cases:

```sh
# T0: the base alone; T1: this head merged into the same base (git merge --no-ff b0f2bc1a)
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
  `.github/workflows/*.yml`, and this PR changes them.
  - At `9c625393`, rtl-full's "Prepare pinned Yosys" took 12.7 minutes, building from source, and rtl-fast's
    `split-cdc` took 14.2 minutes, building Yosys itself.
  - At `b0f2bc1a`, "Prepare pinned Yosys" took 17.4 minutes (1024 s building), and seven Verilator workers built
    Verilator (278-405 s each) before the cache was filled.

  Each is a one-time cost of any workflow change.
- **A base that changes a ROM re-synthesises every Yosys top once.** The result cache's key carries one ROM digest
  for every top, and it covers `gptp_ucode.hex`. So #995's re-pin made Yosys shards 1/4 and 2/4 re-synthesise
  `KL_pp_shadow` and `KL_gptp_shadow` (5.1 and 13.7 minutes, within their slowest earlier windows).
- **26 workers queue** behind the head's other workflows when runners are scarce. At `9c625393`, 25 waited 31
  minutes. At `b0f2bc1a`, 19 workers waited over 10 minutes from job creation to start, the last 70 minutes, and
  the two capture legs 24 and 59 minutes; the watchers' 110.9 and 90.9 minutes include those waits.
- **Jobs this PR does not touch, over the bound: [#1008](https://github.com/kebag-logic/milan-fpga/issues/1008).**
  - By the manager's ruling, #998 acceptance 2 means two things for this PR: every job it touches is within the
    bound with margin (the Verilator workers, the preflight and `firmware-boundary`), and no job gets slower. The
    first is shown above at `b0f2bc1a`; the second, and its exceptions at this head, are stated there.
  - The untouched jobs over the bound are #1008's: rtl-fast's `publication-census`, `firmware-control-mutants` and
    `firmware-srp-mutants` (over 30 minutes at this head), `firmware-unit` and two more firmware jobs, two docs
    workers and three elaborate workers. The elaborate workflow's projection of 1869-1968 s (CI_WORKFLOWS.md) is among them.
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
- No hosted failure of a capture leg was injected; the fork cancellation rests on GitHub's documented matrix
  behaviour, the contract check and the unchanged watcher guard (section above).
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
