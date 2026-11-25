[A839]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Review findings answered](#review-findings-answered)** — Each open finding of rounds R923-1 and R924-1, the owner's ruling on acceptance 2, and where each is answered.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

`cicd-3`, eight commits stacked on PR #1001 (`cicd-verilator-perf`, head `fcbc31f3`); head
`96df313f4e3d8a54b8378357645e744ea86c594c`. Rebase onto `dev` once #1001 merges; the diff against `fcbc31f3` is
these eight commits only.

- Every local gate this PR touches passes at the head in a clean clone: 37 of 37 commands (list in How to
  validate).
- **The hosted run at the head (45514146494) gives no evidence yet.** It was cancelled before any Verilator worker
  finished. rtl-fast's `firmware-boundary` reached its 30-minute limit on a runner at least 1.21 times as slow as
  the previous head's, and the head's fail-fast watchers cancelled every run of the head. Nothing in this diff
  runs in that job. The new deal is proved locally, not yet on hosted runners.
- The full serial sweep was not run in this lane; the candidate bank runs it.

## Linked Issue / roles

Relates to #998 (the CICD improvement lane). Stacked on #1001.

Executor: `[A839]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

Eight commits. Each was measured, and each kept every verdict identical.

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

**Hosted run 45514146494 at `96df313f`.** Every job's minutes are from the Actions jobs API.

| Job | Minutes |
|---|---:|
| full-ci-gate | 1.3 |
| Verilator preflight | 1.9 |
| Prepare pinned Yosys | 13.1 (built from source: its cache key hashes the workflow files) |
| Verilator shard 4/26 (`capture_coherence__0` alone, figure 1095 s) | 14.7, cancelled after 861 s of the piece, unfinished |
| The other 25 workers, the eight unions, the four Yosys shards | never ran (queued 31 minutes behind the same push's docs, elaborate and rtl-fast jobs, then cancelled) |

- The cancellation came from rtl-fast run 45514146566. Its `firmware-boundary` job ran from 23:58:12Z to its
  30-minute limit at 00:28:31Z.
- Its step "Hold the TSN stack boundary over the firmware builders' compiles" was cut at 1743 s. The same step
  took 1446 s at `45d5c35a` and 1405 s at `13e6d869`, so that runner was at least 1.21 times as slow.
- When it passed, the job took 1304-1549 s across the last eleven rtl-fast runs. #998's objective names it.
- The previous head's rtl-full run (45481508309): 19 workers, 353.8 job-minutes (364 rounded up per job).
- This head's 26 workers are projected at about 385 job-minutes (+9 %). That is the dealer's projection sum
  (32167 s against 29556 s) at that run's measured/projected ratio, 0.718.

## Review findings answered

| Finding | Answer | Where |
|---|---|---|
| R924-1-F1 MAJOR: in-tree staging can erase a held slot across TMPDIRs | Fixed: one lock per physical slot directory; independent-process controls | `d95e95e8` |
| R923-1-F1 MINOR: stage root trusted without proof; lock keyed by an unresolved path | Fixed: root proved or refused with its reason; lock keyed by the resolved inode | `d95e95e8` |
| R923-1-F2 MINOR: shard 1 38.6 minutes | Attributed to the runner; stale `milan_dp` figures refreshed | `59f4f478` |
| R924-1-R1, R923-1-R1, R2 (wording) | Applied | `d95e95e8`, `45d5c35a` |
| R923-1-R3 (PR body wording) | Applied | — |
| #998 acceptance 2, the owner's ruling: every hosted job within 30 minutes, no runner-speed qualifier | Every regular worker projects within 1276 s (30 minutes on a 1.41× runner); leg A, indivisible, is stated over it | `feb03206`, `96df313f` |

## Authoritative references

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
python3 scripts/check_py_idiom.py && python3 scripts/ci_events.py --selftest
```

Every command exits 0 at `96df313f`, except the `follow_ring__0` piece. That ran, and passed, on the
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
45514146494, and compare its receipts and logs per suite, whatever legs dealt them, with run 45481508309.

## Known limitations / out of scope

- **Leg A** projects 1530 s, over the 1276-second budget; it is indivisible (#737). On a runner 1.41 times as slow
  as its figure's run it would take about 36 minutes. Making it faster needs a change to that leg or a faster
  runner class, outside this ruling.
- **Two workers sit 1 s inside the budget.** Their figures are local ratios applied to hosted maxima. The first
  hosted windows of the new pieces replace them (the documented refresh rule).
- **The first run after a workflow change rebuilds cached tools.** The Yosys and Verilator cache keys hash
  `.github/workflows/*.yml`, and this PR changes `rtl.yml`. "Prepare pinned Yosys" took 13.1 minutes to build
  from source. Shard 4 restored Verilator, because another workflow had saved that key first.
- **26 workers queue** behind the head's other workflows when runners are scarce; 25 waited 31 minutes here.
- **`firmware-boundary`** (rtl-fast) can exceed its 30-minute limit on a slow runner, and its timeout cancels
  every run of the head. It is outside this change.
- The elaborate workflow's slowest worker projects 1869-1968 s (CI_WORKFLOWS.md), over 30 minutes; it is not a
  Verilator worker and not part of this change.
- `WORKER_OVERHEAD_SECONDS` stays 122 s, though hosted workers measured 14-81 s outside their suites.
- Not run here: the act replay and the full serial sweep.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (acceptance 2: leg A stated over the budget)
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
