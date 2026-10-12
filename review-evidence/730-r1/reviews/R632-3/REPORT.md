[R632] NEGATIVE - exact head 5c6f489ac65f51763a6ccc41f338dde0e5fc90b5

Round R632-3: internal cleared-context review of PR #731 (issue #730), a full review plus the Round 2 and Round 3 deltas.

- Head `5c6f489ac65f51763a6ccc41f338dde0e5fc90b5`, tree `f2e72c84ee50dbd84ea0d37c98f18d2fc8bbdc24`.
- `scripts/act_ci.py` is blob `1f2fa87f`, sha256 `5a9f4aa0…90bf`.
- Source base `dc4d06cb`; live dev is `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`.

This is a source review. It does not authorize a merge.

**Result:** one MINOR finding remains, under `Tests`. A self-test arm says it proves "the most of any selected workflow", but it cannot fail if the code takes the last workflow instead. Conformance, RTL, Robustness and Docs are clean at this head. Every prior public finding is resolved. Two earlier suggestions (R632-2-S2 and S3) are kept as optional.

## Reconstruction (public sources only)

I read these in this order:

1. AGENTS.md and CONTRIBUTING.md.
2. docs/README.md.
3. The body of issue #730: acceptance 1-5.
4. The assignment (6131408752), the ruling (6131815815: no replays in the lane, measurement after the merge), and the Round 2 (6132404197) and Round 3 (6133149921) instructions.
5. The three REVIEW READY comments.
6. `git diff dc4d06cb..5c6f489a` (2 files: `scripts/act_ci.py` +1981/-82 and `docs/testing/CI_WORKFLOWS.md` +141) and its 6 commits.
7. The public evidence tree `50e9635d:review-evidence/730-r1`. From it I fetched only scripts, before forming my verdict.

I read the earlier review comments (R633-1, R632-1, R633-2, R632-2) only after my own pass over the diff, the probes and the mutants was finished.

## Executed evidence (receipts listed in MANIFEST.sha256)

Every run of candidate code used `scripts/sandbox.sh`: no network, no Docker socket, `/run` not mounted, read-only system, private `/tmp`. The input was a `git archive` of the exact head; its `act_ci.py` has the same sha256 as the clone's. No Docker, act, host-side runner or live self-test ran.

| Run | Result |
| --- | --- |
| `act_ci.py --selftest`, unmutated (CPython 3.14.7, PyYAML 6.0.3) | rc 0, `selftest: PASS`, 497 `ok`, 0 FAIL, 6.3 s (`receipts/selftest-head.*`) |
| R632-2's `mutants_r2.py`, unchanged (sha256 `c78da783…5ec0b`, same as published) | `mutants: 36, killed 36, survived [], bad anchors []`. K12 (3 arms), K13 (4), K32 (1) and K36 (1) are KILLED, and so are K29 and K31 (`receipts/mutants-r2-at-head.log`) |
| R632-2's `probe_shutdown.py`, unchanged | rc 0, S1-S4 PASS |
| R633-2's `probe_monitor.py`, unchanged | rc 0. A signal plus a failed reap exits 143, with `act-ci: interrupted by SIGTERM after cleanup` and the reap line printed beside it. A body error plus a failed reap propagates the body's `RuntimeError`, with the reap line beside it. A reap failure alone gives a Refusal, rc 2. Its no-join mutant leaves the reader alive when the boundary exits. Staging warnings leave PASS and FAILED (3) unchanged |
| R633-2's `probe_lifecycle.py`, unchanged | rc 0: 4 fault models x 64 seeds x 300 transitions, plus 88 capacity combinations |
| R633-1's `probe_cpu_ranges.py`, unchanged | Its 5 derivation probes PASS, then it stops at setup with a `TypeError`. Since Round 2, `JobCpuRanges` takes a fifth field, `read_cpus`. This is an API change, not a regression |
| R633-2's `probe_cpu_ranges_compat.py` and R632-2's `r633-1-probe-adapted.py` (each R633-1 probe, adapted only to that API) | rc 0, `CONTRACT VIOLATIONS=0`: F1 restart, F2 applied-then-timeout, F3 slot-0 refusal at 19 CPUs, F4 reap failure still joins |
| My `probe_r3.py` | rc 0, P1-P5 PASS (details below) |
| `probe_r3.py` against two planted mutants (sensitivity check) | `die` frees a range: P1 FAIL. Last workflow instead of most: P2 FAIL (`receipts/probe-r3-sanity-*.log`) |
| My `mutants_r3.py` (30 mutants, sandboxed self-test each) | 23 killed. Q15 is equivalent. Q06, Q11, Q13, Q24, Q28 and Q29 survive: Q24 is F1 below, the rest are S1 (`receipts/mutants-r3-own.log`) |
| Repository gates, sandboxed on a git copy of the head (`run_gates.sh`, `run_gates_r2.sh`) | All 14 rc 0 (`receipts/gates-summary.txt`, `receipts/gates/`). `ci_events.py --check`: 2016 items; `--selftest`: 2016 items and 2828 arms. `act_slot_proof.sh --selftest`: 44. `check_py_idiom.py` and `--selftest`: 54/54. `check_baremetal_only.py --check` and `--selftest`: 700 arms. `docs_check.py`: 0 findings. `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`: 480 links. `check_em_dash.py --base dc4d06cb`: 0 findings over 133 lines. `check_doc_paths.py`: 964 paths. `git diff --check dc4d06cb HEAD` |
| Clone integrity after all probes (`verify_clone.sh`) | HEAD, tree and index match. Status is clean. Tracked bytes and modes match HEAD. The 5 gitlinks match HEAD (`receipts/clone_integrity.txt`) |
| Hosted check runs at the exact head, snapshot | `full-ci-gate`, Yosys shards 0-3, firmware-unit/srp/aecp, verilator-lint, bdd, changes, docs-check-no-git and wire-accountability: success. Physical gPTP: skipped. Verilator shards 0-4, docs-check, elaborate, yosys-elaboration, publication-census and firmware-control-mutants: in progress (`receipts/hosted_check_runs.tsv`). The manager owns hosted and act acceptance |

### What `probe_r3.py` checks

The probe imports the head's `act_ci.py` as a module. It runs only pure functions and `JobCpuRanges`, against a model daemon that I wrote independently.

- **P1: randomized lifecycles.** 300 seeds x 400 steps, 120,000 steps in all, covering:
  - create, start, die and destroy, including restarts;
  - moves that were applied and then timed out, moves that were lost and landed late, refused moves, and unreadable inspects;
  - containers removed without an event;
  - duplicated events, foreign-owner events, and stale events from an earlier stream window (`--since`).

  After every step: no two containers the daemon still has share a job range; every container on a job range holds that range in the record; and the record never maps two holders to one range. Result: 0 violations, with 2510 staging outcomes exercised.
- **P2: derivation order.** The result is the most of any selected workflow in either order: 4 for both orders.
- **P3: derivation source.** The derivation reads the tree it is handed. A planted checkout with `max-parallel: 3` gives 3, while the runner's own tree gives 1. A planted 5 is refused. P3b: `run_validation` derives from `layout.checkout` (`scripts/act_ci.py:5834`).
- **P4: layout.** Slots 0-63 at every concurrency from 1 to 4. Each refuses exactly at the last CPU it needs. The 320 ranges at full concurrency are disjoint.
- **P5: width.** Every range is 4 wide, so `nproc` is 4.

## Findings

### F1: MINOR (Tests): the derivation arm cannot fail for its claim "the most of any selected workflow"

**Where:** `scripts/act_ci.py:7121-7133` (`selftest_job_concurrency`), for the code at `scripts/act_ci.py:2092`.

**Authority:**

- AGENTS.md section 6, `Tests`: "Each new test can fail for the defect it claims to detect."
- Issue #730 acceptance 2: the number of ranges comes from the replayed workflows' concurrency.
- Acceptance 1 and 2, with the PR body's Derivation and Layout rows: a run that derives more than 4 is a Refusal.

**Evidence:**

- The arm is labelled "a replay's concurrency is its workflows' CONCURRENT_JOB_LIMIT widest jobs together (4, then 4+2, then 4+2+1), the most of any selected workflow".
- It derives only `("docs", "rtl-full")`, so the widest workflow is always last.
- Mutant Q24 replaces `most = max(most, sum(...))` with `most = sum(...)`, so the last selected workflow wins. It passes all 497 arms (`receipts/mutants-r3-own.log`).
- Probe P2 separates the two cases: the head gives 4 for `(docs, rtl-full)` and for `(rtl-full, docs)`, while Q24 gives 1 for the second (`receipts/probe-r3-sanity-last.log`).
- The code is correct today.

**Impact:** a regression that sizes a run's ranges from its last selected workflow would pass every offline gate. The workflows are read from the PR's own checkout, so a candidate can change any workflow's width.

- A too-wide `max-parallel` in any selected workflow except the last would escape the Refusal that acceptance 1 and 2 require. Its extra legs would share the staging range, with only a warning.
- An under-derived count would leave legs on staging, again with warnings only.

**Required outcome:** the arm fails whenever the result is not the most over the selected workflows, whatever their order. For example, also derive the reversed order, or put a wide workflow in front of a narrow one.

**Verification:** re-run `scripts/mutants_r3.py`. Q24 must be KILLED, and the unmutated self-test must still pass.

**Lenses:** Tests only. The code conforms; P2 and P3 pass at head.

### SUGGESTIONS (optional; no lens impact)

- **S1 (Tests): behaviour no arm claims, and so no arm pins.** Each of these is correct by reading:
  - **Q06:** a failure closing the event pipe is recorded as a cleanup failure (`:5566-5570`).
  - **Q11:** a container with no free range is marked `staging` (`:5413`). This only changes whether a later destroy counts it as `<g>` or `<s>` in the summary. The warning is printed either way.
  - **Q13:** a moved container later read off its range is warned (`:5399`).
  - **Q28:** the event stream's stderr goes to `DEVNULL` (`:5664`), so there is no unread pipe.
  - **Q29:** `run_validation` derives from the materialized checkout, not the runner's tree (`:5834`, probe P3b). The self-test's checkout carries the shipping workflows, so a mirror would pass.

  A planted checkout whose workflows differ from the runner's would pin Q29 cheaply.
- **S2 (Robustness), R632-2-S2 retained.** A first INT, TERM or HUP can land after the generator enters its `finally` (`:5680`) and before `stop_job_cpu_range_monitor` masks signals. If it does, containment and the join are skipped. The PR body lists this as a known limitation, and `replay_slot` and `run_act_process` share the pattern. The authoritative sentence "On every exit the event stream's process group is walked down…" (`docs/testing/CI_WORKFLOWS.md:1807`) states no exception. If the window stays open until its own Issue, the doc could carry the same caveat as the PR body.
- **S3 (Robustness, diagnostics), R632-2-S3 retained.** A join that raises at once is still reported as "survived its bounded shutdown", with a hold line (`:5506-5525`).

No RESIDUE finding is recorded this round.

### Prior public findings, resolved or retained at this head

| Finding | Status at 5c6f489a | Evidence |
| --- | --- | --- |
| R633-1-F1: `die` freed a restartable container's range | RESOLVED | `observe` frees only on `destroy` or an inspect proving the container gone (`:5298-5480`). The adapted R633-1 F1 probe passes. K01 is killed, and P1 has 0 violations |
| R633-1-F2: an uncertain update freed its target | RESOLVED | The target is reserved before the update, and only `No such container` frees it. The adapted F2 probe passes. K02, K03, K07 and K08 are killed, and P1 covers the applied, lost and unreadable cases |
| R633-1-F3: slot 0 fell back silently | RESOLVED | `job_cpu_ranges` refuses on every slot (`:4672`) and runs before `replay_slot` (`:5834-5846`). The F3 probe passes, K15 is killed, and P4 holds the boundary |
| R633-1-F4: a reap failure skipped the join | RESOLVED | `stop_job_cpu_range_monitor` (`:5528-5590`). The F4 probe passes, and K09, K10, K11 and K14 are killed |
| R632-1-F1: no arm failed without the reader join | RESOLVED | `selftest_job_cpu_monitor_busy` (`:7823`). K10 is killed, and R633-2's no-join mutant shows the reader alive at boundary exit |
| R632-1-F2: verdict invariance was not pinned at run level | RESOLVED | `selftest_cpu_range_warnings` (`:6502`). K23 and K24 are killed, and R633-2's WARNING probe keeps PASS and FAILED (3) |
| R632-1-R1 and R2 (RESIDUE) | APPLIED | The mixed-runner-version sentence is at `docs/testing/CI_WORKFLOWS.md:2146-2157`. The PR body's Layout row states the refusal on every slot |
| R633-2-F1: a cleanup failure replaced an interrupt already unwinding | RESOLVED | `primary` is recorded (`:5678`) and handed to stop, which prints each cleanup failure and returns (`:5576-5589`). The R633-2 probe's signal arm exits 143 with the diagnostic and the reap line. My Q01-Q05 (primary dropped, first failure not printed, cleanup failure raised in its place, raised failure also printed, stdout instead of stderr) are all killed |
| R632-2-F1 (a)-(d): K12, K13, K36 and K32 survived | RESOLVED | `selftest_job_cpu_monitor_shutdown` (`:7996`) and the `--since` pin. `mutants_r2.py`, unchanged: 36 of 36 killed. `probe_shutdown.py`: S1-S4 PASS |
| R632-2-S1 (suggestion) | TAKEN | K29 and K31 are killed |
| R632-2-S2 and S3 (suggestions) | RETAINED as S2 and S3 above | The author's rationale is published in the PR body |

## Lens coverage at this head

```text
[R632] PASS Conformance — scripts/act_ci.py:2043-2093, 4624-4705, 5298-5690, 5774-5786, 5834-5866, 15300-15311; .github/workflows/*.yml (unchanged in diff) — acceptance 1-3 and ruling 6131815815 checked against code and executed probes. Each concurrent container gets its own 4-wide range, disjoint within and across slots (P1, P4, the self-test's planted overlaps). Slot 0 refuses like every slot. Memory flags, --concurrent-jobs, the slot cap and the ownership label are unchanged. Derivation reads the PR's checkout through a BaseLoader (string) parse, refuses a non-literal or more-than-4 max-parallel, and follows the per-job max-parallel inside --concurrent-jobs per stage. nproc stays 4 on staging and on job ranges (P5). A container on staging changes no verdict (K23). No workflow file changed. Acceptance 3's same-head verdict clause and 4-5 are post-merge, by the ruling.
[R632] PASS RTL — git diff --name-only dc4d06cb..5c6f489a (scripts/act_ci.py, docs/testing/CI_WORKFLOWS.md: no HDL, CDC or interface file); runner architecture at scripts/act_ci.py:5298-5590 — the outcome state machine (moving, moved, gone, staging) has complete default paths. The single-writer reader thread starts with cleanup signals blocked (:324-333), and the main thread reads only after the join. Range index and width arithmetic is exact (P4). WorkflowPlan.cpu_ranges defaults to () and keeps existing callers valid. The slot slices set no AllowedCPUs (:4347-4353), so docker update is not fenced by the parent cgroup.
[R632] PASS Robustness — JobCpuRanges.observe/place/check (:5298-5480) and stop_job_cpu_range_monitor/job_cpu_range_monitor (:5528-5685) — 120,000 randomized steps (P1) cover malformed, foreign, duplicated and stale events, restarts, timed-out, lost, refused and unreadable moves, and removal without an event. Interrupts and failures during activity keep their status (R633-2 probe; Q01-Q05 killed). Join retry and hold (K12, K13). No-ranges and reader-start failures. Host CPU counts at and around every boundary (P4). S2 and S3 are suggestions only.
[R632] MINOR Tests — scripts/act_ci.py:7121-7133 — F1: the arm claiming "the most of any selected workflow" cannot fail (Q24 survives). Examined: selftest_job_concurrency, selftest_cpu_layout_disjoint, selftest_job_cpu_ranges, selftest_job_cpu_record, selftest_job_cpu_move_failures, selftest_job_cpu_monitor(_busy/_shutdown), selftest_cpu_range_warnings, selftest_dry_run_cpu_ranges, selftest_workflow_order; 497 arms PASS; 36/36 prior and 23/30 own mutants killed.
[R632] PASS Docs — docs/testing/CI_WORKFLOWS.md:1551-1558, 1724-1860, 2146-2157, 2364-2366; PR #731 body — the replica shape, reservation-until-destroy, inspect-read placement, derivation, slot blocks (20N..20N+19; slot 6 fits one-container workflows on 128 CPUs, checked arithmetically), plan and summary lines, first-failure-wins shutdown, self-test list and mixed-version rule all match the code at head. The PR body's counts (497 arms, 36/36 mutants) reproduce. S2 notes an optional caveat for :1807.
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | `scripts/act_ci.py:2043-2093, 4624-4705, 5298-5866, 15300-15311`; issue #730 acceptance 1-5; rulings 6131815815, 6132404197 and 6133149921; probes P1-P5; R633 probes | R632-3 | 5c6f489ac65f51763a6ccc41f338dde0e5fc90b5 |
| RTL | CLEAN | Diff file list (no HDL or CDC); runner architecture `:324-333, 4347-4353, 5298-5690` | R632-3 | 5c6f489ac65f51763a6ccc41f338dde0e5fc90b5 |
| Robustness | CLEAN (S2 and S3 are SUGGESTIONs) | `JobCpuRanges` and the monitor shutdown; P1 (120,000 steps); R633-2 lifecycle and monitor probes; `probe_shutdown.py`; Q01-Q10 | R632-3 | 5c6f489ac65f51763a6ccc41f338dde0e5fc90b5 |
| Tests | UNCLEAN (F1 MINOR) | Self-test arms `:6502, 7084-7279, 7396-8100, 14342-14362`; `mutants_r2.py` 36/36; `mutants_r3.py` 23/30 (Q24 open) | R632-3 | 5c6f489ac65f51763a6ccc41f338dde0e5fc90b5 |
| Docs | CLEAN | `docs/testing/CI_WORKFLOWS.md` diff (+141); PR body; docs gates rc 0 | R632-3 | 5c6f489ac65f51763a6ccc41f338dde0e5fc90b5 |

## Real limits

- **Nothing ran against a live daemon in this round, by the ruling.** No `docker events`, `docker container update`, `docker container inspect`, act, live `--interrupt-selftest`, replay or `--dry-run` was run. Everything above is offline, using the runner's own seams and an independent model daemon.
  - Docker's event ordering, labels on `destroy` and `update` events, and the effect of `--since` were judged by reading.
  - So was the kernel applying a cpuset update to processes already running.
  - act 0.2.89's concurrency rules (per-job `max-parallel` inside `--concurrent-jobs` per stage, default 4, and `--rm` removal) were judged by reading the act source locations the PR cites, not by running act.
- **One interpreter only.** The self-test ran on CPython 3.14.7 alone. The author's receipts cover 3.12.3.
- **Hosted runs were incomplete at the snapshot.** Many exact-head checks were still in progress; Physical gPTP is skipped. A skip is not an execution.
- **No manager source bank** ran at this head, and none is claimed or inferred here. The final current-dev candidate is separate.
- **No physical calibration or hardware** was run. Field skips are not hardware proof.

## Pending manager duties

- Carry F1 to the executor. The fix belongs in `selftest_job_concurrency`; verify it with `scripts/mutants_r3.py`, where Q24 must be KILLED.
- Accept the exact-head hosted gates once they complete. Validate the current-dev merge candidate (builder and native banks) at the merge turn.
- After the merge, per the ruling:
  - acceptance 4: the `rtl-full` wall clock per job and the slot memory peak, before and after;
  - acceptance 3's same-head verdict comparison;
  - optional acceptance 5;
  - the first live exercise of the monitor, including the `--interrupt-selftest` move requirement (R632-1's M18).
- There is no residue checklist item from this round.

R632-3 FINISHED
