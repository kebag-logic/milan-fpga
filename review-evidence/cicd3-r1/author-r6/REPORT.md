# [A839] CICD improvement, round 6: rtl-fast's firmware-boundary within 30 minutes on a 1.41× runner (#1003)

**Summary.** The manager ruled that rtl-fast's `firmware-boundary` is a hosted job under #998's bound, and that it
must fit with the same margin as the Verilator workers: a projection of at most about 1277 s. One commit on
round 5's `96df313f` splits it with the workflow's existing mechanisms (a literal matrix, run artifacts, the
aggregate's result list). The builders run in two capture legs on runners of their own. `firmware-boundary`
judges both legs' captures together, with the same controls and the same verdict.

| # | Item | Result | Commit |
|---:|---|---|---|
| 1 | `firmware-boundary-capture` (two legs) and `firmware-boundary` judging their captures | Projections 921 s, 749 s, 399 s against 1276 s; the whole job projected 1765 s | `9c625393` |
| 2 | Local proof | A replica of the three jobs at one checkout path prints the whole step's lines, except the eight builder lines, which the legs print instead; one leg's capture alone is refused by name; 37/37 gate commands; 6 new contract arms caught | — |
| 3 | Hosted run at `9c625393` | All four runs green on their first attempt. The three new jobs took 13.2, 14.1 and 5.5 min, with the whole run's verdict. **Two other rtl-fast jobs still exceed 30 minutes:** `firmware-control-mutants` 38.8 (factor 1.39) and `publication-census` 37.2 (1.12). That is the stop condition | — |

Head: milan-fpga `cicd-3` = `9c62539365fea8316dae2b9fd7c68defeff5cb31`, one commit on `96df313f`.
Pushed at 02:50 CET, only to trigger the hosted run, after `push-privacy-check.py . 96df313f…` reported 0
private lines. The command ran bare.

Host: the 96-vCPU VM, load 59-63. `cpu_ranges.py pick` returned no free range at 01:44 and at 02:44. So, as in
rounds 4 and 5, every local arm ran in the session pool 64-95: the whole step on 88-91, the split replica on
92-95, both at once; the gates on 88-95; the short checks on 80-87. Hosted budgets (`CI_*_JOBS=4`, `MAKEFLAGS='-j1
--no-print-directory'`), no compiler cache (`OBJCACHE=`, `CCACHE_DISABLE=1`). Units: `milan-cicd-a839h-base`,
`-split`, `-gates`, `-gates2` (stopped, see §5), `-gates3`, `-poll`.

## 1. What exceeded the budget, and where its time goes

- **The job.** Over the fourteen hosted rtl-fast runs from 45147231523 to 45481508222, `firmware-boundary`
  took 1302-1667 s from its log's first line to its last (the jobs API's windows: 1304-1671 s, mean 1461 s). By the Verilator workers' method its projection was 1765 s: its slowest step,
  1613 s, plus its slowest setup, 152 s. That is 489 s over the 1276-second budget. Run 45514146566's job was
  cut at its 30-minute limit (round 5).
- **The step, phase by phase** (each hosted log prints every builder's seconds; receipts/hosted/fb-phases.tsv).
  The builders run one after another under one capture:

  | Phase | min | mean | max (s) |
  |---|---:|---:|---:|
  | setup (job less step) | 45 | 86 | 152 |
  | control gate build (`test_ctrl_firmware.py --build-only`) | 571 | 661 | 769 |
  | the other five builders (RV32 self-test, store, coverage, reset entry, F5 at two shapes) | 446 | 499 | 597 |
  | the rest of the step: image builders, stack gate, controls, pins, figures | 197 | 212 | 247 |

  The builders are 1033-1366 s of each step. The judgement after them is a sixth.

## 2. The change (`9c625393`)

- **`ctrl_boundary.py --leg K/2 --capture-out DIR`.** Runs only leg K's builders, by their own commands from
  `ctrl_configs.BUILDERS`, under a capture of their own at DIR, and judges nothing. `ctrl_runs.LEGS` names the
  legs: leg 0 is the control gate's build; leg 1 names nothing and holds every other builder the run judges.
  - Refusals: K or N out of range; `--leg` without `--capture-out`, or with `--selftest`, `--capture` or
    `--only`; an existing DIR (a capture is appended to, so a stale one would add compiles); a leg naming a
    builder the run does not judge; a leg that would run nothing. Each one was run (receipts/negative/).
- **The judge is unchanged code.** `firmware-boundary` runs the existing `--capture` path once per leg: it
  refuses a builder run that exited non-zero or ran outside this checkout, and `held()` refuses a known builder
  that the joined captures hold nothing of.
- **The workflow** (`.github/ci-templates/rtl-fast.yml`, regenerated):
  - `firmware-boundary-capture`: `needs: changes`, the same relevance `if`, a literal matrix `leg: [0, 1]` with
    `fail-fast: false`, 30 minutes. Its setup is firmware-boundary's. Each leg uploads
    `firmware-boundary-capture-<leg>-<sha>` (`if-no-files-found: error`, three days).
  - `firmware-boundary`: `needs: [changes, firmware-boundary-capture]`, 30 minutes. It downloads each leg's
    artifact by name to the path the leg made it at (`$RUNNER_TEMP/firmware-boundary-capture-<leg>`; every hosted
    job checks out at one workspace path), then runs the gate with `--selftest --without verilator` and the two
    `--capture` arguments.
  - The `rtl-fast` aggregate needs `firmware-boundary-capture` and lists its result. A failed leg skips the judge,
    and the aggregate counts a skipped job as a pass, so without this a failed leg would turn rtl-fast green.
  - Required contexts are unchanged: `rtl-fast` is still the one verdict, and the job ids `firmware-boundary`
    and `firmware-verilator` keep their names. The fail-fast watcher's expected-job list now carries
    `firmware-boundary-capture (0)` and `(1)` (generated). Each new job records and uploads its job evidence
    through the generator's usual steps.
  - Fork safety: nothing new needs a token. Artifacts pass between jobs of one run, and the watcher's
    same-repository condition is untouched.
- **The contract** (`scripts/ci_events.py`): both jobs' whole step lists pinned (shared setup
  `FIRMWARE_BOUNDARY_SETUP`); `strategy` allowed on the capture job only; the verdict env allowlist;
  `check_boundary_legs`: the matrix exactly `{"fail-fast": false, "matrix": {"leg": [0, 1]}}`, as many legs as
  `ctrl_runs.LEGS` holds (read from its source with `ast`), the judge's need of the legs, both 30-minute limits.
  The RV32 arms cover the capture job too. Six new arms: one leg dropped, fail-fast, the judge without the
  need, either timeout raised, a third leg in the gate; each is caught.
- **Docs:** CI_WORKFLOWS.md (the job list, the aggregate's list, the #998 budget with the three projections), the
  firmware README, the gate's and modules' docstrings.

## 3. Local proof (receipts/local/)

- **Same verdict.** The whole step at `96df313f` (clone `wt/base`, 1893 s), and a replica of the three hosted
  jobs at `6a8260e3`. The replica ran each job in a fresh clone at one path (`wt/split`), the previous clone
  moved aside. Each leg's capture went through an artifact-like copy (hidden files left out as
  upload-artifact@v4 does, exec bits dropped) into the path the judge is given.
  - Leg 0: 901 s, 1834 invocations from 1 builder run. Leg 1: 671 s, 1716 invocations from 6 builder runs.
    Judge: 336 s. Each capture is about 20 MB in about 2100 files.
  - With the clone paths, temporary paths and seconds normalised, the judge's log equals the whole step's but
    for the eight builder lines, which the legs print (receipts/local/whole-vs-judge.diff, 9 lines). That
    includes the capture summary, every boundary control, pin control and figure control, and the final
    count: `4033 compiled sources of 4326 recorded invocations (2464 the firmware's, 425 the stack's, 1144 test
    equipment's and builders' own) … 0 finding(s), 112 boundary, 192 pin and 4 figure controls, 0 misbehaved`, then `PASS`.
  - `6a8260e3` differs from the head only in CI_WORKFLOWS.md and a reflowed comment in `ctrl_configs.py`
    (`git diff 6a8260e3 9c625393 --stat`).
- **A missing leg is refused.** The judge given only leg 0's capture exits 2. It names each of leg 1's five
  builders: `the capture holds no invocation of sw/firmware/gtest/fw_rv32_selftest.py from a run of its own…`.
- **Leg cost locally.** A leg's own overhead is about 1 s (pin check, load). The control gate's build took 900 s
  in leg 0 and 880 s in the whole run, the two running at once on separate CPUs. The judge took 336 s against the
  whole step's 336 s after its builders. So exposing the stack gate's build (it ran beside the builders) costs
  nothing measurable: it finishes beside the image builders.

## 4. Projections (the #998 method)

A figure is the slowest hosted window of that job's part of the step, over the fourteen runs. A projection adds
the slowest setup, 152 s. Artifact transfer of about 20 MB is a few seconds, inside the setup's spread.

| Job | Figure | Projection | Budget |
|---|---:|---:|---:|
| `firmware-boundary-capture` leg 0 | 769 | 921 | 1276 |
| `firmware-boundary-capture` leg 1 | 597 | 749 | 1276 |
| `firmware-boundary` (judge) | 247 | 399 | 1276 |
| before: `firmware-boundary` whole | 1613 | 1765 | 1276 |

So on a runner 1.41 times as slow as the run behind each figure, leg 0 would take about 1299 s, 21.7 minutes.

## 5. Gates (receipts/gates/)

- 37 commands, all rc 0, at `9c625393` in a clean clone (summary-9c625393.txt). These are round 5's 37. The
  self-test ran 5967 arms over 2378 contract items, and the new ones are listed in
  ci_events-selftest-new-arms.txt.
- The first run, at `04eb7f9b` before an amend, failed `check_py_idiom`: one comment line in `ctrl_configs.py` at
  189 columns, from my own edit. It was reflowed and no ratchet was raised. A second run was stopped
  after I found a second over-long line of the same comment. Both are recorded.
- Not run: `ci_tool_inventory.py --check`. No hosted workflow runs it, and this host refuses it at the base
  head too (`CI_IMAGE_SHFMT must name the checksum-pinned Bash parser`). `ci/image/tool-inventory.json` and
  `exec-audit-receipt.json` name firmware-boundary's old step indices. Round 5's rtl.yml changes left them
  stale too; they are the image lane's to regenerate.
- Not run: the act replay, the full serial sweep.

## 6. Hosted run at `9c625393`

- **The runs.** I pushed at 02:50 CET. All four runs succeeded on their first attempt, so I used no
  re-run: rtl-full 45528738040, rtl-fast 45528738009, elaborate 45528738049 and docs 45528737977 (01:51-02:56Z).
- **The split, hosted** (receipts/hosted/run-9c625393/):

  | Job | Minutes | Its part of the step | Against the same part's 14 earlier windows |
  |---|---:|---|---|
  | `firmware-boundary-capture (0)` | 13.2 (792 s) | control gate build 711 s | 1.02 × median, 0.92 × slowest |
  | `firmware-boundary-capture (1)` | 14.1 (848 s) | five builders 774 s (coverage 560, store 127) | 1.54 × median, 1.30 × slowest |
  | `firmware-boundary` | 5.5 (328 s) | the step less its builds, 221 s; both downloads 9 s | 1.04 × median, 0.89 × slowest |

  - Leg 1 drew a slow runner. Its coverage build took 560 s, where 14 earlier windows took 433 s at most. Its
    job exceeded its 749-second projection by 99 s and still took 14.1 minutes.
  - Each capture uploaded as a 46 MB zip in about 5 s (2120 and 1914 files).
  - **Same verdict, hosted.** The judge printed `4032 compiled sources of 4325 recorded invocations (2464 the
    firmware's, 425 the stack's, 1143 test equipment's and builders' own) … 0 finding(s), 112 boundary, 192 pin
    and 4 figure controls, 0 misbehaved`, then `PASS`. Those are the counts of the last complete whole-step run,
    45481508222. Its step output equals that run's in every line but two kinds:
    - the eight builder lines, which the legs print;
    - one line's random temporary sysroot name (`/tmp/fw-rv32-…`).

    The diff is hosted-whole-vs-judge.diff.
- **Jobs over 30 minutes.** These are the stop condition.
  - rtl-fast `firmware-control-mutants`: **38.8 min** (2330 s, 45-minute limit). It is 1.39 times the median of
    its 14 earlier windows, and 0.99 times the slowest.
  - rtl-fast `publication-census`: **37.2 min** (2230 s, 45-minute limit). It is 1.12 times its median, and 0.84
    times the slowest.
  - So both are long on ordinary runners. The ruling did not split either.
  - The fail-fast watchers span their runs: rtl-full 64.7 min, rtl-fast 54.6, elaborate 38.3 (docs 26.3).
  - **The slowest job that is not a watcher** is `firmware-control-mutants`, with runner factor 1.39 against its
    median.
- **Every other job is within 30 minutes.** The next slowest:
  - Verilator shard 1/26: 27.7 min (1662 s, 1.33 times its projection of 1250 s);
  - `firmware-aecp-mutants` 26.3 (1.30 × median), shard 15/26 24.9, `elaborate-gates-4` 23.7 (1.52 ×),
    `docs-gates-2` 23.1 (1.43 ×), shard 24/26 22.8, `firmware-unit` 22.2, shard 8/26 21.9.
- **Round 5's deal, first hosted evidence.**
  - All 26 workers passed, in 389.0 job-minutes. Round 5 projected about 385; the run before took 353.8.
  - Each job's minutes over its projection ran from 0.41 to 1.33. Leg A took 845 s (14.1 min).
- **Suite by suite against run 45481508309** (round 5's comparison tool, suite-compare-…txt):
  - The verdict lines are identical for 63 of 65 suites.
  - The case receipts are identical for 5 of 6 suites that keep receipts: `capture_coherence` (43 cases, 4 → 8
    legs), `maap`, `milan_dp_mclk`, `milan_dp_render` and `pp_shadow`. `follow_ring` and `media_phase` are new
    case suites.
  - `capture_coherence`'s verdict lines differ by construction. They are per-leg tally lines, and the totals are
    equal: 44 checks in both runs (2 × 11 + 12 + 10, and 5 × 5 + 2 × 6 + 7).
  - **`milan_dp`'s cases `gptp` and `gptp-lat` differ.** Both pass in both runs. Each prints one diagnostic line
    that differs: `[#207] full-queue window: level 1, rp 0->0, wp 1->1` before, `rp 1->1, wp 2->2` now.
    - The earlier value is in every log I have from rounds 3-5, 26 occurrences, hosted and local. These
      include round 5's local 8-leg pieces 0/8 and 1/8, which run these two cases.
    - So the 8-leg deal alone did not change it locally. The cause is not established.
    - The receipts differ, so #998 acceptance 1 (identical outputs) is not shown for `milan_dp`. This is open.
- Every job's minutes are in the table at the end of this report (84 jobs; the nightly physical leg was skipped).

## 7. Runner-minutes, before and after (firmware-boundary only)

- **Before:** `firmware-boundary` took 1461 s on average over the fourteen runs (1304-1671 s). It took 1528 s at
  the previous head (45481508222), billed as 26 minutes.
- **After (run 45528738009):** 792 + 848 + 328 = 1968 s, 32.8 job-minutes, billed as 14 + 15 + 6 = 35 minutes.
  That is +507 s against the mean (+35 %), and +9 billed minutes.
- **Why more:** two more setups (checkout, packages, SDK: 45-152 s each), and this run's slow leg-1 runner (1.54
  times the median). At the fourteen runs' mean phases the three jobs would take 1630 s, +12 %.
- **Wall clock:** the judge waits for the slower leg, so the family's span here was 01:52:25-02:15:03Z, 22.6
  minutes. That includes 3 minutes in the queue before the judge started. The whole job took 25.5 minutes at the
  previous head.
- **The rest of the head:** the 26 Verilator workers took 389.0 job-minutes (353.8 before, +10 %). The rtl-fast
  run took 282.9 job-minutes (242.0 at the previous head; its mutation jobs ran slower this time as well).

## 8. Said plainly

- One local mistake. A refusal check meant to show `--leg` without an RV32 compiler was not one: the SDK is on
  this host's PATH. It started a real leg-0 build in the lane checkout at 02:04. I killed it within about a
  minute. It had written bytecode only: three `__pycache__` directories and two `.pyc` files, all ignored by git.
  I logged them to disk-cleanup.log and then removed them. `git status` was clean before and after. No tracked file
  changed.
- The whole-step and replica arms ran at the same time on neighbouring 4-CPU sets of a host at load 60, so the
  local seconds carry contention. The projections use hosted windows only.
- The figures add per-phase maxima from different runs, so they are conservative.
- The two capture artifacts also reach the manifest collector, which downloads every artifact of the run. Its
  reader opens only `job-evidence.json`, `union.json` and `gate-union.json`, and the captures hold none of these.
- A second slip: I started two artifact downloads in parallel, and my `cd` held for the first only. The second
  wrote 26 suite-log directories (12 MB) into the lane as `new/` and `new.out`. I moved them out with `mv` and the
  lane is clean. To make room I ran `rmdir` on the empty scratch directory I had made for them, and logged that
  only afterwards, against the logging rule.
- Removals this round: the bytecode above, logged first; that one `rmdir`, logged after. Nothing else.

## 9. Findings for their own Issues (or a ruling)

1. **Other hosted jobs exceed the bound too**, by the ruling's own measure (receipts/hosted/all-jobs-60-runs.txt,
   the successful jobs of the 60 successful runs among the last 120). Slowest window and mean, in seconds:
   - rtl-fast `publication-census`: 2657 max, 1922 mean, over 1276 in 14 of 14. Its mean is over 30 minutes on
     ordinary runners (45-minute limit).
   - rtl-fast `firmware-control-mutants`: 2357 / 1841, 14 of 14.
   - rtl-fast `firmware-unit`: 1782 / 1472, 12 of 14. `firmware-aecp-mutants`: 1587 / 1297, 6 of 14.
     `firmware-srp-mutants`: 1377 / 1288, 10 of 14. `firmware-verilator`: 1630 / 1021, 1 of 14.
   - docs `docs-gates-0`: 1717 / 1365, 9 of 18. `docs-gates-2`: 1359 / 1046, 2 of 18.
   - elaborate `elaborate-gates-1`: 1453 / 1167; `-4`: 1412 / 911; `-0`: 1343 / 986.
   - The four "Fail fast across this head" watchers (65-113 minutes, 120-minute limit) wait for their run to end,
     so their span is the run's span; no split shortens them.
   - rtl-full's nightly physical gPTP job (145-minute limit) is the documented exception.

   The ruling named `firmware-boundary`, so this round did that alone. Each of the others is its own split, with
   its own mechanism, and needs a decision on scope. Round 5's report missed all but the elaborate worker: I read
   the jobs of one rtl-full run only.
2. **`milan_dp`'s `gptp` and `gptp-lat` receipts differ** between runs 45481508309 and 45528738040 (§6). A
   diagnostic FIFO-pointer line changed while both pass. The cause is not established: round 5's local 8-leg
   pieces print the old value. This is round 5's deal's work, and it blocks #998 acceptance 1 for that suite
   until it is explained.
3. Round 5's findings 2-7 stand. Its finding 1 (`firmware-boundary`) is this round's work.

## Appendix: every job of the four runs at `9c625393`

Minutes are `completed_at − started_at` from the jobs API. A job that never started counts 0. The factor is
the job's minutes over the median of the same job's earlier successful windows (60 runs); new jobs and
renumbered workers have none.

| Workflow | Job | Minutes | × median | Conclusion |
|---|---|---:|---:|---|
| rtl-full | Fail fast across this head | 64.7 | 0.85 | success |
| rtl-fast | Fail fast across this head | 54.6 | 0.82 | success |
| rtl-fast | firmware-control-mutants | 38.8 | 1.39 | success |
| elaborate | Fail fast across this head | 38.3 | 1.27 | success |
| rtl-fast | publication-census | 37.2 | 1.12 | success |
| rtl-full | Verilator shard 1/26 | 27.7 | — | success |
| docs | Fail fast across this head | 26.3 | 0.70 | success |
| rtl-fast | firmware-aecp-mutants | 26.3 | 1.30 | success |
| rtl-full | Verilator shard 15/26 | 24.9 | — | success |
| elaborate | elaborate-gates-4 | 23.7 | 1.52 | success |
| docs | docs-gates-2 | 23.1 | 1.43 | success |
| rtl-full | Verilator shard 24/26 | 22.8 | — | success |
| rtl-fast | firmware-unit | 22.2 | 0.96 | success |
| rtl-full | Verilator shard 8/26 | 21.9 | — | success |
| rtl-fast | firmware-srp-mutants | 21.1 | 0.96 | success |
| rtl-fast | firmware-verilator | 18.9 | 1.27 | success |
| rtl-full | Yosys shard 0/4 | 18.8 | 1.16 | success |
| docs | docs-gates-0 | 18.4 | 0.86 | success |
| rtl-full | Verilator shard 23/26 | 16.8 | — | success |
| rtl-full | Verilator shard 9/26 | 16.2 | — | success |
| elaborate | elaborate-gates-1 | 15.7 | 0.85 | success |
| rtl-full | Verilator shard 12/26 | 15.6 | — | success |
| elaborate | elaborate-gates-0 | 14.9 | 1.00 | success |
| docs | docs-gates-1 | 14.6 | 1.16 | success |
| rtl-fast | split-cdc | 14.2 | 5.88 | success |
| rtl-full | Verilator shard 2/26 | 14.2 | — | success |
| rtl-fast | firmware-boundary-capture (1) | 14.1 | — | success |
| rtl-full | Verilator shard 16/26 | 14.1 | — | success |
| rtl-full | Verilator shard 25/26 | 14.1 | — | success |
| rtl-full | Verilator shard 3/26 | 14.1 | — | success |
| rtl-full | Yosys shard 2/4 | 13.7 | 10.51 | success |
| rtl-full | Verilator shard 17/26 | 13.4 | — | success |
| rtl-full | Verilator shard 22/26 | 13.3 | — | success |
| rtl-full | Verilator shard 6/26 | 13.3 | — | success |
| rtl-fast | firmware-boundary-capture (0) | 13.2 | — | success |
| rtl-full | Verilator shard 14/26 | 13.2 | — | success |
| rtl-full | Verilator shard 20/26 | 13.1 | — | success |
| rtl-full | Verilator shard 19/26 | 12.8 | — | success |
| rtl-full | Verilator shard 21/26 | 12.8 | — | success |
| rtl-fast | yosys-elaboration | 12.7 | 1.00 | success |
| rtl-full | Prepare pinned Yosys | 12.7 | 24.52 | success |
| rtl-full | Verilator shard 0/26 | 12.6 | — | success |
| rtl-full | Verilator shard 13/26 | 12.6 | — | success |
| rtl-full | Verilator shard 5/26 | 12.6 | — | success |
| rtl-full | Verilator shard 7/26 | 12.6 | — | success |
| rtl-full | Verilator shard 10/26 | 12.2 | — | success |
| rtl-full | Verilator shard 18/26 | 12.0 | — | success |
| elaborate | elaborate-gates-2 | 11.9 | 1.61 | success |
| rtl-full | Verilator shard 11/26 | 11.8 | — | success |
| elaborate | elaborate-gates-3 | 11.7 | 1.15 | success |
| rtl-full | Verilator shard 4/26 | 8.4 | — | success |
| rtl-fast | firmware-boundary | 5.5 | 0.22 | success |
| rtl-full | Yosys shard 1/4 | 5.1 | 4.21 | success |
| rtl-full | Yosys shard 3/4 | 2.4 | 1.72 | success |
| rtl-full | Verilator preflight | 1.9 | 1.05 | success |
| rtl-fast | changes | 1.3 | 0.97 | success |
| rtl-full | full-ci-gate | 1.3 | 0.86 | success |
| elaborate | Collect CI manifest | 0.9 | 1.24 | success |
| rtl-fast | verilator-lint | 0.8 | 0.99 | success |
| rtl-fast | Collect CI manifest | 0.7 | 0.87 | success |
| rtl-full | Collect CI manifest | 0.7 | 0.88 | success |
| docs | Collect CI manifest | 0.6 | 0.79 | success |
| rtl-fast | bdd-conformance | 0.6 | 1.26 | success |
| rtl-full | Union media_phase | 0.6 | — | success |
| docs | docs-check | 0.5 | 0.65 | success |
| rtl-full | Union milan_dp_render | 0.5 | 1.20 | success |
| docs | docs-check-no-git | 0.4 | 0.98 | success |
| docs | wire-accountability | 0.4 | 1.09 | success |
| rtl-full | Union maap | 0.4 | 0.96 | success |
| elaborate | elaborate | 0.3 | 0.95 | success |
| rtl-fast | rtl-fast | 0.3 | 0.95 | success |
| rtl-full | Union follow_ring | 0.3 | — | success |
| rtl-full | yosys-portability | 0.3 | 0.87 | success |
| docs | Cancel late CI failures | 0.2 | 1.33 | success |
| elaborate | Cancel late CI failures | 0.2 | 1.67 | success |
| rtl-fast | Cancel late CI failures | 0.2 | 1.47 | success |
| rtl-fast | Prepare pinned Yosys | 0.2 | 0.72 | success |
| rtl-full | Union capture_coherence | 0.2 | 0.54 | success |
| rtl-full | Union milan_dp | 0.2 | 0.60 | success |
| rtl-full | Union milan_dp_mclk | 0.2 | 0.61 | success |
| rtl-full | Union pp_shadow | 0.2 | 0.68 | success |
| rtl-full | verilator-suites | 0.2 | 0.68 | success |
| rtl-full | Cancel late CI failures | 0.1 | 0.67 | success |
| rtl-full | Physical gPTP (nightly and manual) | 0.0 | — | skipped |
