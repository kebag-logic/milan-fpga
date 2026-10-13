[R632] NEGATIVE - exact head 73b8dcd667aa5bf1254e828dd1dd7217c8a103ce

R632-6 is the internal cleared-context independent review of issue #730 / PR #731 at exact head `73b8dcd667aa5bf1254e828dd1dd7217c8a103ce`, tree `73657b81c74af58dde382e4f9ce49d5a0e9e80bc`. It is a full-PR review, with the Round 6 delta (`ede700b0..73b8dcd6`) examined in depth. All five lenses were applied.

The runtime behaviour at this head is correct on every point in the review focus. That covers the range layout, the derivation, reservation lifetime under races and restarts, verdict invariance, containment and precedence, and the Round 6 closing-window fix (R633-5-F1 is resolved). One MINOR Tests finding is open. The Round 6 branch that keeps a plain interrupt's diagnostic clean has no test that fails without it. One RESIDUE item is recorded in the PR body. Tests is therefore UNCLEAN and the verdict is NEGATIVE. This is a source-review verdict, not merge authorization.

## Reconstruction

The review read, in order:

- AGENTS.md, CONTRIBUTING.md and docs/README.md.
- The issue #730 body and acceptance 1-5.
- The public decisions: assignment 6131408752, no-replay ruling 6131815815, and rounds 6132404197, 6133149921, 6133645896, 6134111240 and 6137869227.
- The full diff `dc4d06cb..73b8dcd6`: `scripts/act_ci.py` +2734/-194 overall, and `docs/testing/CI_WORKFLOWS.md`.
- The fourteen-commit history and the PR body.

Prior public findings were read only after this review's own verdict and ledger had been written. Only the runner and its CI documentation change. No workflow, HDL, testbench, firmware or gitlink change (`receipts/clone_integrity.txt`).

The derivation was checked against the pinned act source, v0.2.89 (`pkg/runner/runner.go` NewPlanExecutor, `pkg/model/workflow.go` GetMaxParallel, `pkg/common/executor.go` NewParallelExecutor). Three facts confirm it:

- Per stage, `GetConcurrentJobs()` jobs run at once.
- Each job runs `min(max-parallel, legs)` legs, with a default of 4 and a floor of 1.
- Docker step containers also receive the container options word (`action.go:436`). Docker steps cannot occur here: `validate_workflow_sandbox` admits only five node actions and refuses `services`, `container` and reusable workflows before the derivation runs.

## Finding

### R632-6-F1 | MINOR | Tests | `scripts/act_ci.py:5362`

**Artifact.** In `execute_act_boundary`, the Round 6 condition `if primary is None or primary is delivered: raise`. Its standing controls are `selftest_act_signal_window` (`:12415`) and `selftest_act_closing_signal` (`:12570`, cases at `:12469`).

**Authority:**

- Round 6 decision 6137869227: normal act stays interruptible, a signal pending before act starts is delivered, and the conventional signal outcome is kept when there is no earlier failure.
- `docs/testing/CI_WORKFLOWS.md:1840-1841`: SIGINT, SIGTERM and SIGHUP "keep their `128 + signal` exit status and diagnostic".
- `:1819-1826`: the closing line is printed beside an already-propagating failure.
- AGENTS.md section 6, Tests: each new test can fail for the defect it claims to detect.
- CONTRIBUTING: changed behaviour has self-checking tests.

**Evidence.** Mutant S8 removes only `or primary is delivered` (`scripts/mutants_r632_6.py`). It survives three checks:

- The full self-test: rc 0, 0 FAIL (`receipts/mutants_r632_6-at-head.log`).
- The unchanged R633-5 boundary-precedence probe: rc 0 (`receipts/probe_boundary_precedence-on-S8.rc`).
- The unchanged R633-4 cleanup-entry probe: rc 0 (`receipts/probe_cleanup_entry-on-S8.rc`).

The existing signal-window arms check the outcome and masks but never stderr. The 18 new closing arms only exercise a signal that arrives after the act stand-in returned.

This review's probe `scripts/probe_r6_interrupt_diag.py` drives the real monitor and boundary, first with a signal during act and then with a signal pending before act. At the head it passes 6/6, each with exactly `act-ci: interrupted by SIG... after cleanup` (`receipts/probe_r6_interrupt_diag-at-head.log`). On S8 it fails 6/6 (`receipts/probe_r6_interrupt_diag-on-S8.log`). Every ordinary interrupt during act then also prints `act-ci: act boundary closing was interrupted (TerminationRequest: SIGINT); the failure already propagating is kept`, although nothing was propagating.

**Impact.** The code at the head is correct. The gap is that a plausible regression of this round's new branch passes every standing control. That regression would put a false "failure already propagating" claim on the most common interrupt path, Ctrl-C during act. An operator would then look for an integrity failure that never happened. The exit status would stay 128 + signal, so only a diagnostic check can catch it. This is the mirror image of R633-5-F1, which was a true diagnostic lost; here a false one is added.

**Required outcome.** A standing self-test arm must deliver a first signal through the real boundary inside the monitor in two cases: during act, and pending before act. With no earlier failure, it must require exit `128 + signal` and exactly the conventional interrupt diagnostic, with no closing line. The arm must fail on S8. All existing arms, the R632-2 and R632-3 campaign outcomes and the R633-5 probe must keep their results.

**Verification:** three checks.

- `scripts/mutants_r632_6.py`, unchanged, must report S8 KILLED by a named FAIL arm.
- `scripts/probe_r6_interrupt_diag.py`, unchanged, must pass at the corrected head.
- The full self-test must pass.

## RESIDUE

### R632-6-R1 | RESIDUE | Docs | PR #731 body, Status section

The body says "Round 6 awaits independent re-review. These two new commits have not been pushed." The PR head is `73b8dcd6`, so both commits are pushed and the sentence is stale. This is wording only: it changes no measurement, figure, verdict, test, code, generated artifact or claim.

**Exact fix:** replace the sentence with "Round 6 awaits independent re-review. The two Round 6 commits are pushed; the PR head is `73b8dcd667aa5bf1254e828dd1dd7217c8a103ce`."

## Suggestions (optional, retained)

- **R632-6-S1 (retains R632-5-S1).** Removing every closing restore (mutant S9) is killed only by the self-test ending with rc 129, not by a named FAIL arm. The gate still fails. Containing the case inside an arm would name the regression.
- **R632-6-S2 (retains R632-5-S3, R632-3-S1).** The R632-3 campaign survivors Q06, Q11, Q13, Q28 and Q29 remain; Q15 is equivalent. Q29 is the derivation reading the runner's own tree instead of the materialized checkout. It is pinned only by probes, including D in `probe_r632_6.py`, not by the standing self-test.
- **R632-6-S3 (retains R632-5-S4).** A join that raises at once is still reported as "survived its bounded shutdown" (`:5596`). The hold itself is accurate.
- Two of this round's mutants survive and are judged equivalent; they are not findings:
  - S5 removes the handler's restore before its diagnostic. The outer `finally` restores the mask, and the latch makes repeat signals no-ops.
  - S6 removes the outer `finally` restore. The inner `finally` and the handler already restore on every path.

## Lens results

- [R632] PASS Conformance - `scripts/act_ci.py:2090`, `:2119`, `:4671`, `:4719`, `:5921`; act v0.2.89 `runner.go`/`workflow.go`/`executor.go`; `receipts/probe_r632_6-at-head.log` (sections L, D, P). Checked against acceptance 1-3 and the rulings:
  - Slot N owns `20N..20N+19`. Staging and every job range are 4 CPUs wide (`nproc` 4). Slots 0-63 at full concurrency own exactly CPUs 0-1279, with no CPU shared.
  - Concurrency is derived from the materialized workflows, not a mirror. Editing rtl.yml's `max-parallel` changes the result: 1, 2, 3, 4, 0→1, 007→7.
  - A too-wide value (5, 64, 999999) is refused before any slot.
  - Non-literal values (expression, padded, negative, float, list, map, empty) and a non-mapping strategy are refused.
  - The derivation takes the maximum in every order. `CONCURRENT_JOB_LIMIT` 2 sums the two widest jobs.
  - A host without the CPUs refuses on every slot, including slot 0, at every boundary tested (1-128 CPUs, slots 0/3/6, ×1/×4).
  - The plan lines for slot 0 and slot 3 match the PR and the docs.
  - The Round 6 contract holds: precedence at the closing restore, interruptible act, pending delivery and conventional status. Its only gap is the test gap in F1, filed under Tests.
- [R632] PASS RTL - `scripts/act_ci.py:5313-5376` (boundary), `:5380-5560` (`JobCpuRanges` state machine), `:5610-5772` (stop and monitor), `:5861-5871` (nesting inside the ownership/lease boundary). Checked as architecture and contracts for this tooling-only diff:
  - The record's state machine is complete. Unknown create/start places. Destroy, inspect-gone and update-`No such container` are the only releases. Die, update and start of a held container re-read. Staging and gone containers are never moved again.
  - There is one writer thread, and the main thread reads only after the join.
  - The mask handoff: hold before yield, the reader inherits it, act's window is reopened and closed, and delivery happens after containment.
  - CPU-index arithmetic and widths are correct (L section).
  - The act options word, memory/swap bounds, `--concurrent-jobs` and the ownership label are unchanged.
  - No hardware interface or CDC is touched.
- [R632] PASS Robustness - `receipts/probe_r632_6-at-head.log` (R section) and `receipts/probe_controls.log`.
  - 3000 randomized lifecycles against a model daemon passed. Act creates, starts, stops, restarts and removes containers while the monitor lags. Moves succeed, fail, time out after or before applying, or land late; reads fail or time out; lifecycle steps interleave inside each CLI call.
  - After every daemon change, no two existing containers sit on one job range, every occupant holds its range, and all ranges are free at the end.
  - The R633-1 restart sequence gives A `4-7` and B `8-11`.
  - Seven planted defects are each detected (C1-C7), so the probe can fail.
  - The earlier unchanged public probes pass: shutdown, lifecycle, monitor, compat, the R633-1 adapter and probe_r3 (300 seeds).
  - Round 6 paths hold: signal during act, signal pending before act, and signal at both closing restores with no earlier failure, a Refusal or a RuntimeError.
- **Tests: UNCLEAN (F1).** Applied artifacts:
  - Self-test at the head: 525 ok, 0 FAIL, PASS (`receipts/gates/act-ci-selftest.log`). The 18 closing arms are at `:12469`/`:12570`.
  - R632-2 campaign, unchanged: 36/36 killed, including K12, K13, K32 and K36.
  - R632-3 campaign, unchanged: 24/30 killed, including Q24; survivors Q06/Q11/Q13/Q15/Q28/Q29, as published.
  - This round's set: 10 mutants, 7 killed (S1, S2, S3, S4, S7, S9, S10). S5 and S6 are equivalent. S8 survives (F1).
  - The R633-5 probe, unchanged, passes at the head and fails at `ede700b0`. The planted-overlap disjointness arms are present and pass.
- [R632] PASS Docs - `docs/testing/CI_WORKFLOWS.md:1551-1558`, `:1724-1891`, `:2177-2191`, `:2397`; PR #731 body at the head. Checked against the code above:
  - Layout and slot blocks; the reservation lifetime; inspect confirmation; the derivation and its refusals.
  - The summary line format (`:5557`) and the plan line.
  - Warning-only staging; the containment ladder and join; the mask and delivery rule.
  - The closing-window paragraph, with its exact diagnostic (`:5366`).
  - The mixed-version rule; measurement stated as not done.
  - R632-5-R1 is applied word for word at `:1833-1834` and R632-5-R2 at `:1838`.
  - All documentation gates pass.
  - One PR-body RESIDUE (R632-6-R1).

## Round-specific checks (Round 6 assignment 6137869227)

| Requirement | Result | Evidence |
|---|---|---|
| First signal at the closing restore keeps the active failure and diagnostic | Met | 18 self-test arms; R633-5 probe rc 0 (9 cases); S1/S2/S3/S7/S10 killed |
| Hold restored before monitor cleanup; containment, reader end and pipe close before teardown | Met | arm masks `[set(), CLEANUP, CLEANUP]`; trail `contained, stream ended, outer teardown` |
| Act stays interruptible; a pending signal is delivered before act starts | Met | `selftest_act_signal_window`; my probe B: act not started, 130/143/129; S4 killed |
| Conventional status with no earlier failure | Met (status); diagnostic not pinned | probe A/B 6/6 at head; F1 |
| Standing control on the real boundary | Met | `act_closing_signal_case` uses the real `job_cpu_range_monitor` and `execute_act_boundary` with a real reader thread |
| R633-5 probe unchanged passes | Met | `receipts/r633-5-probe_boundary_precedence-at-head.rc` 0; at `ede700b0` rc 1 |
| R632-5-R1/R2 applied | Met | `CI_WORKFLOWS.md:1833-1834`, `:1838` |
| No replay | Met | no daemon, act or live dry-run was run by this review |

## Prior public findings at this head

| Finding | Disposition | Evidence at this head |
|---|---|---|
| R633-1-F1 (die freed a restartable range) | Resolved | lifecycle R section; R633-1 sequence; C1 detected |
| R633-1-F2 (uncertain update released) | Resolved | applied-timeout and late-landing cases in R section; C2/C4 detected |
| R633-1-F3 (slot-0 fallback) | Resolved | host-size matrix in L section (slot 0 refuses at 7 and 19) |
| R633-1-F4, R632-1-F1 (reap skipped join; join untested) | Resolved | R632-2 campaign 36/36; shutdown probe PASS |
| R632-1-F2 (verdict invariance) | Resolved | `selftest_cpu_range_warnings` (`:6589`) present and passing; `report_job_cpu_ranges` only prints |
| R632-1-R1/R2 | Applied / superseded | `CI_WORKFLOWS.md:2188-2191`; PR body states refusal on every slot |
| R633-2-F1 (first failure wins) | Resolved | probe_monitor and cleanup-entry probes pass |
| R632-2-F1 (K12/K13/K32/K36) | Resolved | all four KILLED |
| R632-3-F1 (Q24) | Resolved | Q24 KILLED |
| R633-4-F1 (cleanup-entry signal) | Resolved | cleanup-entry probe rc 0 |
| R633-5-F1 (closing restore replaces Refusal) | Resolved | see the round table |
| R632-5-R1, R632-5-R2 | Applied | exact wording present |
| R632-5-S2 (step count by interpreter) | Addressed | PR body: "its step count depends on the interpreter"; this run reports 185 steps on 3.14.7 |
| R632-5-S1, S3, S4 and earlier S-items they retain | Retained as SUGGESTION | R632-6-S1..S3 |

## Executed evidence

All candidate code ran only in an unprivileged disposable sandbox (`scripts/sandbox.sh`: no network, no Docker socket, read-only system), on CPython 3.14.7 with PyYAML 6.0.3, at most 16 jobs at once. The commands are in `receipts/commands.txt`. All 12 public inputs match evidence commit `fa4034a8` (`receipts/public_inputs.txt`).

| Check | Result |
|---|---|
| `act_ci.py --selftest` | rc 0, 525 ok, 0 FAIL |
| `ci_events.py --check` / `--selftest` | rc 0, 2016 items / 2828 arms |
| `act_slot_proof.sh --selftest` | rc 0, 44 cases |
| `check_py_idiom.py` / `--selftest` | rc 0, ratchets hold / 54 PASS |
| `check_baremetal_only.py --check` / `--selftest` | rc 0, 0 findings / 700 arms |
| `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` / `--verify-anchors`, `check_doc_paths.py` | all rc 0 |
| `check_em_dash.py --base dc4d06cb`; `git diff --check dc4d06cb 73b8dcd6` | rc 0, 0 findings over 167 added lines; rc 0 |
| R632-2 / R632-3 campaigns, unchanged | 36/36; 24/30 (Q24 killed; published survivors) |
| `probe_r632_6.py` (3000 seeds) / its 7 controls | rc 0, 99 ok / 7 of 7 detected |
| `mutants_r632_6.py` | 7 killed, S5/S6 equivalent, S8 survives (F1) |
| `probe_r6_interrupt_diag.py` | head 6/6 pass; S8 6/6 fail |
| R633-5, R633-4 and six earlier public probes, unchanged | all rc 0 at head; R633-5 rc 1 at `ede700b0` |

**Hosted, exact head** (`receipts/hosted_check_runs.tsv`, snapshot 04:36Z): 16 completed success and 1 skipped (Physical gPTP; a skip is not executed evidence). Eight are not finished: `docs-check` (which runs the self-test on a 4-vCPU runner), `elaborate`, Verilator shards 0-4 and `rtl-fast`. Hosted acceptance belongs to the manager.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #730 acceptance and rulings; `act_ci.py:2090, 2119, 4671, 4719, 5313-5376, 5921`; act v0.2.89 source; probe L/D/P | R632-6 | 73b8dcd667aa5bf1254e828dd1dd7217c8a103ce |
| RTL | CLEAN | full two-file diff; `act_ci.py:278, 5313-5376, 5380-5560, 5610-5772, 5861-5871`; gitlinks unchanged | R632-6 | 73b8dcd667aa5bf1254e828dd1dd7217c8a103ce |
| Robustness | CLEAN | probe R (3000 lifecycles) and controls C1-C4; six earlier probes; R6 interrupt paths | R632-6 | 73b8dcd667aa5bf1254e828dd1dd7217c8a103ce |
| Tests | UNCLEAN (R632-6-F1) | self-test 525/0; `:12415, 12469, 12570, 6589, 7171, 7502, 14883`; R632-2/R632-3 campaigns; `mutants_r632_6.py`; R633-5 probe | R632-6 applied; not covered clean | 73b8dcd667aa5bf1254e828dd1dd7217c8a103ce |
| Docs | CLEAN (R632-6-R1 RESIDUE) | `CI_WORKFLOWS.md:1551-1558, 1724-1891, 2177-2191, 2397`; PR body; doc gates | R632-6 | 73b8dcd667aa5bf1254e828dd1dd7217c8a103ce |

CLEAN means no BLOCKER, MAJOR or MINOR finding is open under that lens. RESIDUE and SUGGESTION do not affect coverage.

## Real limits

- No live daemon was used. That excludes `docker events`, `docker container update` and `docker container inspect`, live container affinity and `nproc`, act, live `--dry-run` and replays (disk ruling).
- The randomized lifecycle model is this review's own abstraction of daemon and act ordering; it is not a live trace.
- Self-tests ran on CPython 3.14.7, not the author's 3.12.3. Interpreter-dependent step counts differ: 185 here.
- No full parent, processor, gPTP, Yosys, builder or Vivado bank was run.
- Physical calibration was NOT RUN, and field skips are not hardware proof.
- No manager source bank exists at this head, and none is claimed or inferred.

## Integrity

The clone stayed at the exact head throughout:

- Worktree clean. Index identical to the tree.
- Blobs `act_ci.py` `c632615e` (mode 755) and `CI_WORKFLOWS.md` `a9ded0c0`.
- Five gitlinks unchanged (`receipts/clone_integrity.txt`).
- No candidate file was edited. Probes and mutants ran on disposable copies under `scratch/`, which is not published.

## Pending manager duties

- Carry R632-6-F1 to the executor, and R632-6-R1 to the residue checklist.
- Obtain a fresh independent review after the correction.
- Complete hosted acceptance at the corrected head.
- At the merge turn, build and validate the current-dev merge candidate (source base `dc4d06cb`, live dev `49da9fd9...`), including the builder and native banks, and publish its receipts separately.
- Obtain explicit merge authorization and perform post-merge containment.
- Post-merge duties under the no-replay ruling:
  - acceptance 3's same-head verdict comparison;
  - acceptance 4's per-job wall clock and slot memory peak against #721 at `42678ae2` and #715 at `c7d0ad63`;
  - optional acceptance 5.
- Keep #730 open until those duties are done.

R632-6 FINISHED
