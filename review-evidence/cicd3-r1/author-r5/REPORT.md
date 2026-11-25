# [A839] CICD improvement, round 5: every regular Verilator worker within 30 minutes on a 1.41× runner (#1003)

**Summary.** The manager's ruling on #998 acceptance 2 was option one: split the pieces that alone exceed the
budget, add workers only where dealing cannot fit them, and leave every regular worker projecting at most about
1277 s. Two commits on `45d5c35a` do that with the planner's existing mechanisms. One piece cannot be split:
`milan_dp_mclk__0`, media-clock leg A, whose continuous history is indivisible (#737). It is stated over the
budget, not hidden. Nothing was posted; `cicd-3` was pushed once, only to trigger the hosted run.

| # | Item | Result | Commit |
|---:|---|---|---|
| 1 | follow_ring and media_phase as CI cases | Makefile case targets beside unchanged serial runs; follow_ring's two thread-printing drivers print in fixed order | `feb03206` |
| 2 | The 1276-second budget, the splits, 26 workers | Regular workers project 1199-1275 s; leg A 1530 s under #737's exception | `96df313f` |
| 3 | Local proof | 37/37 gate commands at the head in a clean clone; 8/9 planted budget defects refused (the ninth is a redundant copy, explained); the five new pieces pass locally with the same verdicts and tallies as the hosted whole-suite logs | — |
| 4 | Hosted run 45514146494 | **Cancelled before any Verilator worker finished.** rtl-fast's `firmware-boundary` reached its 30-minute limit on a runner at least 1.21× as slow, and the fail-fast watchers cancelled the head's runs. The ruling's stop condition; not re-run | — |

Head: milan-fpga `cicd-3` = `96df313f4e3d8a54b8378357645e744ea86c594c` (eight commits on PR #1001's `fcbc31f3`).
Pushed at 00:56 CET after `push-privacy-check.py . 45d5c35a…` reported 0 private lines (`45d5c35a..96df313f`).

Host: the 96-vCPU VM, load 40-46. Measurement arms ran in units `milan-cicd-a839g-meas`, `-meas2`, `-meas3`,
`-meas4` and `-smoke`, each on a range `cpu_ranges.py pick` returned (24-31, 8-15, 56-63, 8-15, 0-7), two 4-CPU
arms per range, one clone per arm. No range was free for the gates, so they ran in the session pool 64-95, as round
4's arms did. Pinned Verilator 5.050; hosted budgets (`VERILATOR_JOBS=4 SIM_JOBS=4 MAKEFLAGS='-j1
--no-print-directory'`); no compiler cache in any timed arm (`OBJCACHE=` and `CCACHE_DISABLE=1`), since hosted
workers have none. No unit of mine is left running.

## 1. The ruling, and what exceeded the budget

- **The budget.** 1800 s / 1.41 = 1276.6 s, rounded down to 1276 s (`CI_BUDGET_SECONDS`), allowance included.
  It applies to every regular worker and replaces the 1620-second rule. The 60 % rule stays.
- **Round 4's list was short by one.** It named five pieces of 1309-1493 s. A sixth exceeds 1276 s alone:
  `media_phase`'s 1400-second figure. A seventh, `capture_coherence__1`, exceeds it with the allowance (1204 +
  122). The third complete run (45481508309) also raised `capture_coherence__0` from 1436 to 1618.
- **Dealing alone could not fit.** The figures total 28995 s after the splits, against 25 regular workers ×
  1154 s of room. 19 workers cannot hold them under 1276 s each.

## 2. Local measurements (receipts/measure/)

Each pair ran concurrently on two 4-CPU arms of one booking, at `45d5c35a`. Each arm ran in its own clone.

| Old leg | wall | New leg | wall | ratio |
|---|---:|---|---:|---:|
| `milan_dp` 0/4 | 953.5 | 0/8, 4/8 (`aclk`) | 463.8, 741.6 | 0.486, 0.778 |
| `milan_dp` 1/4 | 809.8 | 1/8 (`render-mutants`), 5/8 | 710.5, 222.9 | 0.877, 0.275 |
| `milan_dp` 2/4 | 281.7 | 2/8, 6/8 | 148.2, 153.2 | 0.526, 0.544 |
| `milan_dp` 3/4 | 403.1 | 3/8, 7/8 | 221.6, 245.0 | 0.550, 0.608 |
| `capture_coherence` 0/4 | 859.7 | 0/8, 4/8 | 581.6, 223.5 | 0.677, 0.260 |
| `capture_coherence` 1/4 | 632.2, 661.7 | 1/8, 5/8 | 467.0, 225.6 | 0.739, 0.357 (faster reference) |
| `capture_coherence` 2/4 | 440.8 | 2/8, 6/8 | 220.4, 217.8 | 0.500, 0.494 |
| `capture_coherence` 3/4 | 415.4 | 3/8, 7/8 | 235.6, 259.9 | 0.567, 0.626 |
| `milan_dp_mclk` 0/4 (leg A) | 719.9 | 0/8 | 669.4 | 0.930 |
| `milan_dp_mclk` 1/4 | 612.9 | 1/8 | 530.5 | 0.865 |
| `milan_dp_mclk` 2/4 | 570.2 | 2/8, 4/8 | 497.8, 303.2 | 0.873 |
| `follow_ring` whole (`make`) | 959.5 | b8, pullin, bind, small-pullin, settle-control | 364.2, 42.3, 116.9, 641.7, 15.6 | — |
| `media_phase` whole (`make`) | 755.1 | the thirteen `cases` (log spans) | ramp 314 … carry 51 | — |

- New pieces through `scripts/ci_suite_pieces.py run`, as the sweep runs them, on the work-in-progress tree. Its
  Makefiles equal the head's; it predates the print-order fix of §3.1. `follow_ring__0` 378.0,
  `follow_ring__1` 690.7, `media_phase__0` 263.6, `__1` 262.4, `__2` 282.3 s. Every case passed.
- Their combined logs carry the same verdict lines and the same counted tallies as run 45481508309's whole-suite
  logs: `follow_ring` 97 checks in 3 tallies, `media_phase` 386 checks in 28 (receipts/smoke/).

## 3. The changes

### 3.1 `feb03206`: follow_ring and media_phase as CI cases

- **media_phase.** `ci-list` gives 18 cases: pins, render, blend, ofs, det, then the thirteen `cases`. Each
  `exec-<case>` prints what the default run prints for it: the separator, then the harness output, with a case's
  `t=` trace lines dropped as `cases` drops them. All 18 are tally receipts.
- **follow_ring.** `small-pullin` and `settle-control` print no counted tally, and `ci_make_cases.py` refuses a
  case without one (NOCOUNT). So the five legs are three cases: `b8`; `pullin-small`; `bind-settle`. Each runs its
  legs one after another, so its transcript is fixed.
  - A leg's prerequisite is now `$(LEG_BUILD)`, default `build`. The `small-pullin` fine build is
    `$(if $(LEG_BUILD),$(FINE_BUILD))`.
  - `make -n run` prints the same commands as before. The serial run is unchanged.
- **The print race.** The first local `follow_ring__0` piece printed `settle control 25000000 Hz:
  PASSsettle control 6250000 Hz: PASS`. Python's `print` from four threads interleaved two lines, and the order
  was completion order. A receipt digests the case's output, so `small_pulls.py` and `settle_control.py` now print
  the same lines from the main thread in case order after the pool. Two runs at the head are byte-identical
  (receipts/determinism/). The smoke logs predate this fix.

### 3.2 `96df313f`: the budget, the splits, the workers, the figures

- `scripts/suite_shards.py`:
  - `CI_BUDGET_SECONDS` replaces the regular workers' 1620-second rule.
  - `PIECE_SECONDS`: `milan_dp` and `capture_coherence` get eight legs; `follow_ring` two; `media_phase` three.
  - Thirteen figures raised from run 45481508309 (CI_WORKFLOWS.md lists them).
  - `WORKER_OVERHEAD_SECONDS` covers 26 workers.
  - Controls: 1276 passes and 1277 is refused under a wide timeout. Leg A exactly at a 35-minute job's 60 % bound
    passes and one second over is refused. The budget equals 1800 / 1.41 rounded down, computed without the
    constant.
  - The head arm prints each worker's binding bound (it printed the 60 % bound only).
  - The module is still 1000 lines and `planted_selftest` 96, inside the Python idiom ratchets.
- `scripts/ci_suite_pieces_selftest.py`: the head bound is the budget; the bad-coordinate list follows the leg
  count.
- `scripts/ci_make_cases.py`: `media_phase`'s thirteen case costs order its starts (receipts unchanged by
  construction).
- `.github/workflows/rtl.yml` regenerated: 26 workers, the 60-minute arm on worker 25, `Union follow_ring`,
  `Union media_phase`, `--expect 26`.
- CI_WORKFLOWS.md ("The #998 budget", the projection table, the counts), TESTING.md, RUNNING_TESTS.md.
- **Figures.** Each new leg holds a subset of one old leg's cases (round-robin: `names[k::8]` lies inside
  `names[k % 4::4]`). So on one runner its window is at most the old leg's. Its figure is the old leg's hosted
  figure times the measured ratio above, rounded up. A newly divided suite's pieces scale its whole figure.
  The table is in the PR body and receipts/figures.txt.
- **Why `milan_dp_mclk` keeps four legs.** Eight cut leg A's piece by 7 % (669 against 720 s; about 1309 s at its
  figure, 1431 with the allowance), still over. The four new pieces would each rebuild both models, about
  1900 figure-seconds more. Its other legs already fit.

## 4. The deal at 26 workers (receipts/deal-26.txt)

- Regular workers project 1199-1275 s. The two heaviest are 1 s inside the budget:
  - worker 0: `milan_dp__1` alone, the `render-mutants` leg;
  - worker 24: `capture_coherence__5`, `pp_shadow__0`, `avtp_rxmon`.
- Worker 25: leg A alone, 1530 s, under #737's exception and its own 60 % bound (2160 s).
- 25 workers leave seven over the budget (the worst 1328 s). 26 is the least that fits.

## 5. Leg A, stated

- Its piece projects 1530 s: figure 1408 s plus the 122 s allowance. That figure is the slowest of three hosted
  windows (857, 1408, 779 s), on a runner whose job took 1.49 times as long as the base run's.
- Leg A's history alone is the floor of its piece. Its own simulation is about 590 s locally, out of 669 s for
  the 0/8 piece.
- On a runner 1.41 times as slow as the run that set its figure, its worker would take about 36 minutes. Its
  measured hosted jobs took 13.2, 16.0 and 23.8 minutes.
- Starting the clean legs before the mutant model build would save about 40 s locally (about 78 figure-seconds),
  still over. It was not done.

## 6. Gates (receipts/gates/)

- 37 commands, all rc 0, at `96df313f` in a clean clone: the 35 of rounds 3 and 4, plus `check_sweep_shape.py`
  and `suite_tally.py --selftest`.
- Rounds 3 and 4 reported "36 of 36" for a list of 35 commands. Their summaries have 35 lines; that was a
  miscount.
- The first run, at `bf86e3cd` before the amend, failed `check_py_idiom`: two over-long lines, `suite_shards.py`
  over 1000 lines and `planted_selftest` over 100. That was fixed by compacting this round's own additions, with no
  ratchet raised.
- **Planted defects** (receipts/gates/budget-plants.txt). Eight of nine are refused:
  - the budget at 1620;
  - the rule removed;
  - `>=` for `>`;
  - the budget applied to leg A;
  - 19 workers;
  - `milan_dp` at four legs;
  - `follow_ring` whole;
  - the 60 % rule removed.

  The ninth loosens `ci_suite_pieces_selftest.py`'s own copy of the bound. A compliant head cannot show that;
  `suite_shards.py --selftest` holds the same bound and refuses every real overflow.

## 7. Hosted run 45514146494 at `96df313f`

- **What happened.** Run 45514146494 (rtl-full) was cancelled at 00:29:07Z, before any Verilator worker
  finished (receipts/hosted/).
  - rtl-fast run 45514146566's `firmware-boundary` job started at 23:58:12Z and reached its 30-minute limit at
    00:28:31Z. A timed-out job concludes `cancelled`, and the head's fail-fast watchers then cancelled the head's
    other runs: rtl-full, docs and elaborate.
  - Its one long step, "Hold the TSN stack boundary over the firmware builders' compiles", had run 1743 s when it
    was cut. The same step took 1446 s at `45d5c35a` (run 45481508222) and 1405 s at `13e6d869`
    (run 45457005513). So its runner was at least 1.21 times as slow as the previous head's (at least 1.24 against
    `13e6d869`'s); the step had not finished, so the true factor is larger.
  - Over the last eleven rtl-fast runs, the job took 1304-1549 s when it passed.
  - **Nothing of this change runs there.** The job runs `sw/firmware/ctrl/test/ctrl_boundary.py`. This PR's
    diff touches neither `rtl-fast.yml` nor `sw/`. #998's objective already names this job: 25.8 minutes, and
    one earlier 30-minute timeout that cancelled a whole run.
- **What rtl-full ran** (every job's minutes from the jobs API, receipts/hosted/run-45514146494-jobs.txt):

  | Job | Minutes |
  |---|---:|
  | full-ci-gate | 1.3 |
  | Verilator preflight | 1.9 |
  | Prepare pinned Yosys | 13.1, built from source: its cache key hashes the workflow files, and `rtl.yml` changed |
  | Verilator shard 4/26 | 14.7, then cancelled |
  | the watcher, "Fail fast across this head" | 32.7, then cancelled |

  - Shard 4/26 ran `capture_coherence__0` alone (figure 1095 s) for 861 s without finishing. It restored
    Verilator from the cache; the source-build step was skipped.
  - The other 25 workers, the eight unions and the four Yosys shards never ran. They waited 31 minutes in the
    queue while the same push's docs, elaborate and rtl-fast jobs held the runners. Their API `started_at` is the
    queue time; the table counts them as 0.
- **So no hosted window measures the new deal.** The slowest job of this head's runs is `firmware-boundary`:
  at least 30.3 minutes, runner factor at least 1.21. That is the stop condition in my instructions: a hosted
  job over 30 minutes on a slow runner, reported with its factor. I stopped there.
- I did not re-run anything: the authorisation covered the push only. A re-run (or a new push) would give the
  missing evidence. The re-run must not reach a `firmware-boundary` runner that slow, or that job must first fit
  30 minutes.

## 8. Runner-minutes, before and after

- **Before** (run 45481508309 at `45d5c35a`, receipts/hosted/runner-minutes-estimate.txt):
  - 19 Verilator workers: 353.8 job-minutes (364 rounded up per job);
  - six unions 2.6, the preflight 1.9, the watcher 58.5;
  - the whole rtl-full run: 424.6 job-minutes (445 rounded up).
- **After: no complete hosted run** (§7), so this is a projection.
  - The dealer's projections sum to 32167 s against 29556 s before: +2611 s, +8.8 %.
  - At run 45481508309's measured/projected ratio (0.718), the 26 workers take about 385 worker-minutes,
    31 more (+9 %).
  - Two more union jobs add about 0.4 minutes each. Seven more jobs each round up once when billed.
  - The extra cost is the splits' repeated builds and each new worker's setup.
- **Wall clock.** 26 workers plus the same push's other workflows exceeded the runners this repository got
  tonight. 25 workers waited in the queue for 31 minutes. A run's span, and the watcher's, grows with that queue,
  though no job's own minutes do.

## 9. Said plainly

- **The hosted proof is missing.** The run at the head was cancelled by `firmware-boundary`'s timeout before any
  Verilator worker finished (§7). The new deal is proved locally (gates, plants, pieces), not on hosted runners.
- Leg A is over the budget, as stated in §5. By projection, the ruling's bar is met for every other worker.
- The two heaviest workers' 1-second margins rest on local ratios applied to hosted maxima. The ratios carry
  local noise of a few percent.
- The budget compounds two factors. It assumes a runner 1.41 times as slow as the figures' runs, and the figures
  are already hosted maxima, some from slow runners. That is the ruled method; it is conservative.
- Five fast gate commands (about 5 s) ran pinned to 0-7 while my own smoke arm measured `media_phase__2` there.
  That piece's 282 s may carry those seconds.
- A `py_compile` check left `__pycache__` in the lane's follow_ring directory. Its removal was logged, then done.
  Round 4's 3.2 GB of build clones were removed, logged first.
- Not run: the act replay, the full serial sweep.

## 10. Findings for their own Issues

1. **`firmware-boundary` (rtl-fast) exceeds 30 minutes on a slow runner** (at least 1.21×, cut at its 30-minute
   limit). Its timeout cancels every run of the head. It is in #998's scope but not this ruling's.
2. **Leg A cannot meet a 30-minute bound on a 1.41× runner.** It needs a faster leg or a faster runner class.
3. **The Yosys and Verilator cache keys hash every workflow file.** So the first run after a workflow change
   builds them from source: here "Prepare pinned Yosys" took 13.1 minutes. Shard 4 still restored Verilator,
   because another workflow had saved that key first.
4. **The elaborate workflow's slowest worker projects 1869-1968 s** (CI_WORKFLOWS.md), over 30 minutes.
5. **`WORKER_OVERHEAD_SECONDS` is conservative** (hosted 14-81 s against 122 s). A measured change could lower it
   and free a worker.
6. **26 workers queue behind the head's other workflows.** 25 waited 31 minutes here. A run's span grows,
   though no job's minutes do.
7. Round 3's and 4's open findings stand.
