[R632] NEGATIVE - exact head eb5666349fc20ed3b5437a4357ef097c1231e557

Round R632-1, internal cleared-context review of PR #731 (issue #730).
Head `eb5666349fc20ed3b5437a4357ef097c1231e557`, tree `301ea3a9a3ff9a1e4a4eee40edfd70925982d0cb`.
Source base `dc4d06cb`, live dev `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`.
Diff `dc4d06cb..eb566634`: `scripts/act_ci.py` (+1038/-66) and `docs/testing/CI_WORKFLOWS.md` (+82/-8). No workflow, RTL, firmware or test-bench file is touched.

The verdict is NEGATIVE because of two open MINOR findings, both under `Tests` and one also under `Docs`. The self-test cannot fail for two properties that the PR, the docs and this round's assignment rely on:

- the event-stream reader is joined before Docker teardown;
- a monitor problem is printed and never changes a verdict.

The code at this head does both. Probes P4.5 and P5 show it, and this round found no defect in the shipped runner logic. The gap is in the evidence that would catch a regression.

## Reconstruction

The task was rebuilt from public sources only, in this order:

1. AGENTS.md and CONTRIBUTING.md (act-first replication, the review lenses).
2. Issue #730: the body's acceptance 1-5, the assignment (comment 6131408752), the disk note, the ruling (comment 6131815815: no replays in the lane, measurement after the merge, `--dry-run` and `--selftest` evidence) and the executor's TAKEN and REVIEW READY comments.
3. `docs/testing/CI_WORKFLOWS.md`: "Act-first local replication" and "Parallel replay slots".
4. The diff and its two commits.
5. The public evidence tree at `b5cf83a0/review-evidence/730-r1`. Every file's sha256 matches its MANIFEST.json entry.
6. Exact-head hosted check runs.

PR #731 had no prior review findings to resolve. Its only comments are the two review-start notices.

## Executed evidence (this round, exact head; receipts listed in MANIFEST.sha256)

| Command | Result |
| --- | --- |
| `python3 scripts/act_ci.py --selftest` | rc 0, `selftest: PASS`, 477 `ok`, 0 FAIL (CPython 3.14.7, PyYAML 6.0.3; the author recorded 3.12.3). The same result holds in a `git archive` extraction. |
| `ci_events.py --check` / `--selftest` | rc 0 / rc 0 (2016 contract items OK) |
| `act_slot_proof.sh --selftest` | rc 0 (44 cases) |
| `check_py_idiom.py` / `--selftest` | rc 0 / rc 0 (0 over-long lines, 0 globals) |
| `check_baremetal_only.py --check` / `--selftest` | rc 0 / rc 0 |
| `check_em_dash.py --base dc4d06cb` | rc 0, 0 findings over 82 added lines (run with the pinned Markdown renderer environment) |
| `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `gen_toc.py --verify-anchors`, `check_doc_paths.py` | all rc 0 |
| `git diff --check dc4d06cb HEAD` | rc 0 |
| `scripts/probes.py` (reviewer probes; Docker, sudo and act are all stood in) | rc 0; see the probe IDs below |
| `scripts/mutants.py` (24 planted defects, 16 jobs, run three times) | 18 killed, 5 defects survived, and 1 control (a non-defect) survived. The classification was identical in all three runs. |

No Docker command, daemon, act binary, replay or `act_ci.py` against a live PR was run.

## Findings

### F1: MINOR (Tests, Docs): the self-test cannot fail when the monitor's reader join is missing

- **Location:**
  - `scripts/act_ci.py:7165-7198` (`selftest_job_cpu_monitor`, the arm "after its body the monitor walks the stream's group down the containment ladder once, joins its reader with every line applied, and closes the pipe");
  - `scripts/act_ci.py:5443-5449` (the join under test);
  - `docs/testing/CI_WORKFLOWS.md:1809-1810` ("For the job ranges it pins: ... its containment and join after a body that returns or raises").
- **Authority:** AGENTS.md section 6 `Tests`: "Each new test can fail for the defect it claims to detect." The assignment asks this round to judge that the events stream "is contained and joined on every exit path".
- **Evidence:** mutant `M13_reader_not_joined` replaces `if reader is not None and reader.ident is not None:` with `if False:`. That removes the join and its survival check. The mutant passes the self-test with 477/477 `ok` in all three runs (`receipts/mutants*.txt`). The arm's fake stream is an `io.StringIO` holding two lines, so the reader thread drains it before the assertions run, whether or not anything joins it.
- **Impact:** a regression that lets Docker teardown start while a `docker container update` is still in flight would ship green. The doc's "pins ... join" is not true of the current self-test.
- **Required outcome:** an arm in which the reader is still busy when the body returns, for example a move stand-in that blocks until released, or a stream that yields a line only after the body. Removing or reordering the join must then fail that arm.
- **Verification:** re-run `scripts/mutants.py`. `M13_reader_not_joined` must be KILLED and the unmutated self-test must still pass.

### F2: MINOR (Tests): "printed as a warning and never changes a verdict" is not pinned at the run level

- **Location:**
  - `scripts/act_ci.py:5535-5546` (`report_job_cpu_ranges`) and `5621-5632` (the monitor in `execute_workflows`);
  - `scripts/act_ci.py:6074-6090` (`cpu_range_monitor_stand_in`, which always yields a clean record);
  - `docs/testing/CI_WORKFLOWS.md:1783-1785`.
- **Authority:**
  - acceptance 3 ("The replay's verdict on the same PR head is unchanged");
  - the assignment ("a container that stays on the staging range cannot change a verdict");
  - AGENTS.md section 6 `Tests`.
  - The post-merge acceptance-4 reading in the PR body depends on two lines this code prints: `act-ci: <wf>: CPU ranges: <n> created, <m> moved ...` and the absence of `act-ci: WARNING: <wf>: CPU ranges:`.
- **Evidence:** three mutants pass 477/477 in all three runs:
  - `M16_problems_fail_the_workflow` (`execute_workflows` returns `RC_FAILED` when the record has problems);
  - `M17_problems_never_printed` (no WARNING line is printed);
  - `M23_report_skipped` (neither the summary nor any warning is printed).

  Problems are checked only on the `JobCpuRanges` record (`selftest_job_cpu_record`, and the "reported as a problem, not a verdict" arm at line 7216, which reads `record.problems`). No arm drives `execute_workflows` with a record that has problems.
- **Impact:**
  - A change that turns a missed move into a `FAILED` verdict, which is a fidelity regression against acceptance 3, would pass every gate.
  - So would a change that silences the lines the manager's post-merge measurement reads.
- **Required outcome:** through the existing `workflow_control_fakes` / `run_workflow_control` harness, add an arm whose monitor stand-in yields a record with moves and planted problems. The arm asserts:
  - (a) the workflow's verdict follows act's result alone (PASS with rc 0, and `FAILED (<rc>)` with nonzero);
  - (b) the summary line and one `WARNING ... CPU ranges:` line per problem are printed.
- **Verification:** M16, M17 and M23 are KILLED.

### R1: RESIDUE (Docs): mixed runner versions are not mentioned in the authoritative doc

- **Location:** `docs/testing/CI_WORKFLOWS.md:2098-2105` (Resource bounds, first bullet). The PR body's "Known limitations" states this hazard; the doc does not.
- **Evidence:** probe P2b. A pre-#730 runner's slots 1-4 (`4N..4N+3`) meet this runner's slot-0 job ranges `4-19`. The cost is CPU contention only: `nproc` is still 4, so no verdict changes.
- **Exact fix:** append to that bullet: "A replay started by a runner from before #730 still puts slot N on `4N` to `4N+3`, which meets these blocks, so run every concurrent slot from one runner version."

### R2: RESIDUE (Docs): the PR body's slot-0 fallback threshold is too broad

- **Location:** PR #731 body, "Description" table, Layout row: "Slot 0 on a host under 20 CPUs keeps its legs on `0-3`, as before".
- **Evidence:** `job_cpu_ranges(0, 1)` returns `("4-7",)` on a host with 8 to 19 CPUs (self-test arm "one container still gets 4-7"). The fallback depends on the ranges the run derives, as the doc already says correctly at `CI_WORKFLOWS.md:1770-1772`.
- **Exact fix:** "Slot 0 on a host without the CPUs for the ranges a run derives (20 for `rtl-full`, 8 for a workflow deriving one container) keeps its legs on `0-3`, as before, and prints that."

### SUGGESTIONS (Robustness; optional, no lens impact)

- **S1 (restart after `die`).** Probe P3.1: `die` frees a range while the stopped container keeps that cpuset. A restarted container would then share it with the next leg, and is counted as "started on the staging range". This is not reachable under act 0.2.89 with `--rm` and no restart policy. Freeing on `destroy`, or re-placing on `start` of a known container, would close it. Control mutant `C24_free_on_destroy_only_control` shows that freeing on `destroy` alone still passes the self-test.
- **S2 (timed-out move).** Probe P3.2: if a move's CLI times out but the daemon applied the move, the range is treated as free, and the next container can be placed on it. A WARNING is printed. Marking such a range as unknown rather than free would avoid the double placement.
- **S3 (containment raises).** Probe P4.4: if `terminate_group` itself raises, the reader is not joined and the pipe is not closed. This needs the leader-reap step to fail after the group was proven gone, so it is practically unreachable. A `try/finally` around the join would make "joined on every exit path" unconditional.
- **S4 (container gone before its move).** Probe P3.4: a container already gone at its move counts in `created` but not `moved`, with no WARNING. The PR body's post-merge reading, "expect `m == n` and no WARNING", could then be misread. Printing a note for that case would close the gap.

## Resolved or confirmed by this round

- **Disjointness.** Probe P2 checked 389 admitted (host CPUs, slot, concurrency) layouts across 17 host sizes, slots 0-63 and concurrency 1-4, independently of the self-test's own helper. It found:
  - no range outside `20N..20N+19`;
  - no CPU beyond the host;
  - every job range 4 wide;
  - no shared CPU within a slot or between any two slots;
  - no fallback on an isolated slot.

  A 128-CPU host admits slots 0-5 at concurrency 4 and slots 0-6 at concurrency 1, as the doc states. Mutants M01, M02, M03, M07 and M21 (spacing, overlap with staging, guard removed, too-wide accepted, 3-wide range) are all killed.
- **Derivation reads the replayed workflows.** In `run_validation` (`scripts/act_ci.py:5682-5683`), the derivation reads `layout.checkout` after `validate_workflow_sandbox` and before `replay_slot` is entered. Mutants M04, M05, M06 and M22 are killed. Probe P1b shows:
  - a literal `max-parallel` is honoured;
  - a `max-parallel` above 4 is refused at the range step;
  - an expression or an empty value is refused;
  - two wide jobs follow the `CONCURRENT_JOB_LIMIT` sum.

  Shipping workflows derive `rtl-full` 4 (`verilator-shards` and `yosys-shards`) and `docs`, `elaborate` and `rtl-fast` 1. The act 0.2.89 binary's strings contain `GetMaxParallel`, `MaxParallelString`, "Failed to parse 'max-parallel' option" and "PlanExecutor concurrency". The sandbox refuses `services`, `container` and reusable-workflow jobs, so only job containers carry the label.
- **Event handling.** For the five-shard job, a freed range is reused by the next leg (P3.6). Stale `die`/`destroy` lines are ignored (P3.5). A duplicate `create` moves once (P3.3). The label filter, the owner check, the free-on-`die` and the lowest-free choice are pinned (mutants M08, M09, M10 and M11 killed).
- **Exit paths.**
  - KeyboardInterrupt, TerminationRequest and a reader that cannot start each still walk the stream's group and close the pipe (P4.1-P4.3).
  - The containment walk on a raised body is pinned (M12 killed), as are the ended-early report (M19) and act running inside the monitor (M14).
  - An in-flight move finishes before the monitor exits (P4.5).
  - The monitor is stopped before `cleanup_owned_containers` (`scripts/act_ci.py:5621-5637`).
  - The reader thread starts with cleanup signals blocked, so its `docker container update` takes the worker branch of `run_tracked_process_group_command` (`5098-5170`). That branch makes no `signal.signal` call.
  - Leases, the ownership label, `--memory`/`--memory-swap`, `--concurrent-jobs 1`, the 24G slice cap and the existing Refusals are unchanged. The slice sets only `MemoryMax`, so a move out of the staging range is permitted.
- **Verdict.** `report_job_cpu_ranges` returns nothing, and the verdict comes from act's result alone (P5 and code reading). Only the interrupt self-test turns a missed move into a Refusal, and it does so deliberately.
- **Dry run.** The slot-0 and slot-3 lines in the public receipt `dryrun-offline.txt` match the self-test arms that pass here. The executor published that a live `--dry-run` is not daemon-free (a conflict with ruling item 2) instead of resolving it privately.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Issue #730 acceptance 1-3 against `scripts/act_ci.py:2041-2091` (derivation), `4622-4723` (layout, refusals, fallback) and `5682-5683` (order before slot entry); the diff stat (no workflow, step or job change); probes P1, P1b, P2 and P2.128; ruling 6131815815 (acceptance 3's verdict clause, 4 and 5 deferred after the merge; the PR says `Relates to #730`, not `Closes`) | R632-1 | eb5666349fc20ed3b5437a4357ef097c1231e557 |
| RTL | CLEAN | No HDL in the diff (`git diff --stat dc4d06cb..eb566634`: two files, neither RTL), so the RTL-specific angles do not apply. The architecture and interface angles were applied to the runner: the single-writer reader thread, the record read only after the join (`5427-5457`, `5621-5632`, `14390-14400`), the reuse of the `ProcessSeams` and `terminate_act_process_group` ladder, the worker-thread signal path in `run_tracked_process_group_command` (`5098-5170`), and the slot daemon's `--cgroup-parent` and slice properties (`4133`, `4350`) | R632-1 | eb5666349fc20ed3b5437a4357ef097c1231e557 |
| Robustness | CLEAN (S1-S4 are SUGGESTIONS) | `JobCpuRanges.parse/place/observe` (`5306-5415`) under malformed, foreign, duplicate, stale, out-of-order, restart and timeout inputs (P3.1-P3.6); monitor exits under return, raise, KeyboardInterrupt, TerminationRequest, thread-start failure and containment failure (P4.1-P4.5); host-size boundaries 1-1280 (P2); unreadable, expression, empty, 0 and over-4 `max-parallel` (P1b) | R632-1 | eb5666349fc20ed3b5437a4357ef097c1231e557 |
| Tests | UNCLEAN (F1, F2) | `selftest_job_concurrency`, `selftest_cpu_layout_disjoint`, `selftest_job_cpu_ranges`, `selftest_job_cpu_record`, `selftest_job_cpu_monitor`, `selftest_dry_run_cpu_ranges`, the updated `selftest_workflow_order`, slot and guard arms (`6846-7230`, `12092-12160`, `13291-13460`); 24-mutant campaign run three times (`receipts/mutants*.txt`); full gate set (`receipts/gates.rc`) | R632-1 | eb5666349fc20ed3b5437a4357ef097c1231e557 |
| Docs | UNCLEAN (F1; R1 and R2 are RESIDUE) | `docs/testing/CI_WORKFLOWS.md` hunks at 1551-1557, 1723-1812, 2095-2105 and 2312, checked against the code; a repository-wide search for the stale `4N` layout (none left); docs gates rc 0; the PR body and the issue's REVIEW READY | R632-1 | eb5666349fc20ed3b5437a4357ef097c1231e557 |

## Real limits of this round

- **Nothing ran live.** No `docker events` or `docker container update` was run against a daemon, by this round or (per the PR) by the lane. These remain unexercised against a live daemon:
  - act's real event order (`die` before the next `create` under `--rm`);
  - the label being present on `update`/`destroy` events;
  - `cpuset` moves under the systemd cgroup driver and the slot slice.

  The live `--interrupt-selftest` requirement (mutant M18) is pinned only by that live gate, which this round did not run.
- **Upstream act source was not read.** The act 0.2.89 semantics (max-parallel default, per-stage `--concurrent-jobs`, `--rm` removal before the next leg) were checked against the binary's strings and the PR's citations only.
- **No measurement was taken.** Acceptance 3's "verdict unchanged on the same head" clause, acceptance 4 (wall clock, slot memory peak) and acceptance 5 are not shown at this head. That follows the ruling.
- **Some properties rest on probes, not the self-test.** P4.5 and P5 show the join and the verdict invariance, but those probes are this round's, not the self-test's. F1 and F2 ask for the self-test to pin them.
- **Slot 0 has no host-wide lock.** Two concurrent slot-0 replays would share job ranges, as they already shared `0-3` before #730. This round did not treat that as a slot overlap.
- **No source bank ran.** No manager source bank or candidate-merge build ran at this head, and none is claimed. Physical calibration was NOT RUN; skipped fields are not hardware proof.
- **Hosted checks were incomplete at read time.** At the exact head, 8 contexts had completed with success and 1 was skipped (Physical gPTP, nightly/manual). Another 15 were queued or in progress, including several Verilator and Yosys shards, `elaborate` and `docs-check` (`receipts/hosted_check_runs.tsv`). This round makes no hosted verdict.

## Pending manager duties

- Carry R1 and R2 to the residue checklist.
- Hosted and act acceptance at the exact head after F1 and F2 are fixed: the `rtl-fast` verdict, plus exact-head `verilator-suites` and `yosys-portability` once ready.
- The current-dev candidate merge validation (builder and native banks) at the merge turn.
- The post-merge acceptance-4 measurement per the ruling: before = the slot-0 replays of #721 at `42678ae2` and #715 at `c7d0ad63`; after = the first replay on the merged runner. Read the plan line, the `CPU ranges:` summary (expect `m == n`, `k == 4`, no WARNING; see S4), the verdict, and the slot memory peak on an isolated slot. Acceptance 5 comes after that.
- A re-review of the corrected head by this lane. The `Tests` and `Docs` coverage must be re-banked at that head. Any change to `scripts/act_ci.py` also un-covers `Conformance`, `RTL` and `Robustness` for the changed artifacts.
- The external review (R633) is independent and still required.

## Clone integrity after probes

The clone at `$REVIEWS/r632-1-730` was never modified. Probes and mutants ran on a `git archive` extraction under `scratch/`. After the round:

- `HEAD` is `eb5666349fc20ed3b5437a4357ef097c1231e557` and the tree is `301ea3a9a3ff9a1e4a4eee40edfd70925982d0cb`;
- `git status --porcelain` is empty;
- the `git ls-files -s` digest is unchanged (`receipts/index_before.sha256` equals `receipts/index_after.sha256`);
- the five submodule gitlinks are unchanged (`receipts/gitlinks_head.txt`).

R632-1 FINISHED
