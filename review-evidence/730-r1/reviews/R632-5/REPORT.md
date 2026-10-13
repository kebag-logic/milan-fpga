[R632] POSITIVE - exact head ede700b00ef4d79566a6f108b11ce9bd4ad6beaa

R632-5, internal cleared-context independent review of issue #730 / PR #731. This is a full-PR review, with the Round 5 delta (`31e53e82..ede700b0`) examined in depth. All five lenses were applied. Each is CLEAN at this head. No BLOCKER, MAJOR or MINOR finding is open. Two RESIDUE items and four SUGGESTIONs are recorded.

This is a source-review verdict, not merge authorization.

- Tree: `1efdeba1e3477de15b8f04c5615c6d58e2756e46`. Source base: `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`.
- Changed: `scripts/act_ci.py` and `docs/testing/CI_WORKFLOWS.md` only. No workflow, HDL, firmware, testbench or gitlink changed (`receipts/scope.txt`).
- No manager source bank ran at this head, and none is claimed or inferred here.

## Reconstruction

Read in this order:

1. AGENTS.md and CONTRIBUTING.md (workflow, verification bar, code-quality and documentation rules), then docs/README.md.
2. Issue #730: its frozen acceptance 1-5.
3. The public decisions on the issue:
   - assignment 6131408752;
   - no-replay ruling 6131815815;
   - Round 2 decision 6132404197;
   - Round 3 decision 6133149921;
   - Round 4 decision 6133645896;
   - Round 5 decision 6134111240.
4. `docs/testing/CI_WORKFLOWS.md`: act-first replication, slot resource bounds, the self-test pin list.
5. The full diff `dc4d06cb..ede700b0` (10 commits) and the Round 5 delta.
6. The public executable evidence on commits `783701eb` and `677b2f0a`.

Prior public review findings were read only after this round's own verdict and ledger had been written (`receipts/own-pass-before-prior-findings.txt`).

Acceptance 4 and optional acceptance 5 are post-merge manager duties under the ruling. So is acceptance 3's same-head verdict comparison.

## Findings

### R632-5-R1 | RESIDUE | Docs | `docs/testing/CI_WORKFLOWS.md:1824`

- **Evidence:** "The signal diagnostic accompanies that earlier failure."
  - Elsewhere on the page, "diagnostic" means the interrupt line `act-ci: interrupted by SIG... after cleanup`. That line is not printed in this case.
  - The line actually printed is `act-ci: CPU-range monitor cleanup was interrupted (TerminationRequest: SIG...); the failure already propagating is kept`. The self-test arm at `scripts/act_ci.py:8385-8397` pins that line.
- **Impact:** wording only. Behaviour, tests and verdicts are correct.
- **Exact fix:** replace the sentence with: "The signal is printed beside that earlier failure as `act-ci: CPU-range monitor cleanup was interrupted (...); the failure already propagating is kept`."

### R632-5-R2 | RESIDUE | Docs | `docs/testing/CI_WORKFLOWS.md:1828`

- **Evidence:** "Then the first failure wins." This follows a paragraph that already states the precedence rule, so "Then" reads as a later step.
- **Exact fix:** "Throughout, the first failure wins."

### R632-5-S1 | SUGGESTION | Tests | `scripts/act_ci.py:12390`, `:12443`

Two of this round's own control mutants are killed by ending the self-test, not by a named FAIL arm:

- **V07** (act's boundary does not restore the hold): the self-test exits 129 on a stray SIGHUP.
- **V08** (the live interrupt probe does not reopen the signals): a Refusal escapes the arm.

The gate still fails (rc != 0). Containing each case inside its arm would name the regression.

### R632-5-S2 | SUGGESTION | Tests, Docs | PR #731 body, Round 5 list

- "198 executed line steps ... 396 injections" is the count on CPython 3.12.3.
- On CPython 3.14.7 the same arm reports 185 steps (`receipts/selftest-head.log:112`).
- The arm prints its own count, so stating that the number depends on the interpreter would avoid a false mismatch.

### R632-5-S3 | SUGGESTION | Tests | `selftest_dry_run_cpu_ranges` (`:14736`)

- Retains R632-4-S1 (R632-3-S1). `mutants_r3.py` still leaves six survivors: Q06, Q11, Q13, Q28, Q29, and Q15, which is equivalent.
- Q29 (derivation from the runner's own tree, not the checkout) is pinned only by the earlier probes, not by the standing self-test.
- Optional.

### R632-5-S4 | SUGGESTION | Robustness | `join_job_cpu_reader` (`:5549`)

- Retains R632-4-S3 (R632-2-S3): a join that raises at once is still reported as "survived its bounded shutdown".
- The hold itself is accurate.
- Optional.

## Executed evidence (this round, exact head)

Every candidate import and self-test ran inside `scripts/sandbox.sh`: unprivileged, no network, no Docker socket, read-only system. Probe and mutant trees are copies made from `git archive` of the head. At most 16 jobs ran at once. No Docker, act, replay, privileged command or host self-test was run.

| Check | Result | Receipt |
|---|---|---|
| `act_ci.py --selftest` (CPython 3.14.7, PyYAML 6.0.3) | rc 0, 507 ok, 0 FAIL, 26 s | `receipts/selftest-head.log`, `.rc` |
| R633-4 `probe_cleanup_entry.py`, unchanged (sha256 `2bcf4697...`) | rc 0. All six cases `invariant: true`: body and cleanup-entry delivery for INT/TERM/HUP. Contained, reader ended, pipe closed before teardown. Exits 130/143/129 with the interrupt diagnostic | `receipts/probe_cleanup_entry-at-head.log` |
| R632-2 `mutants_r2.py`, unchanged (sha256 `c78da783...`) | 36/36 killed, no bad anchors. K12 (3 arms), K13 (4), K32 (1), K36 (1) KILLED | `receipts/mutants_r2-at-head.log` |
| R632-3 `mutants_r3.py`, unchanged (sha256 `2ef94964...`) | 24/30 killed, Q24 KILLED (fails exactly the order arm). Survivors Q06, Q11, Q13, Q15, Q28, Q29, as before | `receipts/mutants_r3-at-head.log` |
| `probe_shutdown.py` S1-S4 | PASS | `receipts/probe_shutdown-at-head.log` |
| `probe_r3.py` P1-P5 (300 seeds, 120,000 lifecycle steps) | PASS | `receipts/probe_r3-at-head.log` |
| `probe_r2.py` | P1-P3b, P7-P10 PASS (800 fuzzed interleavings, no shared job range). P4 FAIL by design, see below | `receipts/probe_r2-at-head.log` |
| R633-1 probe as adapted in Round 2; R633-2 compat, lifecycle and monitor probes | PASS, contract violations 0; signal preservation 143 | `receipts/r632-2-r633-1-probe-adapted-at-head.log`, `receipts/r633-2-*-at-head.log` |
| R633-1 `probe_cpu_ranges.py`, unchanged | rc 1: `JobCpuRanges.__init__() missing ... 'read_cpus'`. A harness incompatibility from Round 2's constructor; its adapted form passes | `receipts/r633-1-probe_cpu_ranges-at-head.log` |
| Own `probe_r632_5.py masks` | PASS. Details below the table | `receipts/probe_r632_5-masks.log` |
| Own sweep: a first signal at each of 235 traced steps from monitor entry to monitor exit | 470 injections, main thread and whole process, 0 failures. Each exits 128 + signal with its diagnostic; stream contained, reader ended and pipe closed at monitor exit; no mask or pending signal left | `receipts/probe_r632_5-steps.json`, `receipts/probe_r632_5-sweep-*.log` |
| The same sweep on a control without the outer hold (`act_ci.py:5729` removed) | 18 failures, from the cleanup entry `:5742` through `stop_job_cpu_range_monitor:5605`: stream not contained, reader alive. The sweep can fail | `receipts/probe_r632_5-sweep-control-no-outer-mask.*` |
| Own Round 5 mutants V01-V12 | 12/12 killed. Covers: outer hold removed; held signal swallowed; held signal replacing a body failure; early release; release never taken; act or live-probe window not opened or not closed; reader started unmasked; either beside-diagnostic dropped | `receipts/mutants_r632_5-at-head.log` |
| Gates: `ci_events.py --check` (2016 items) and `--selftest` (2828 arms); `act_slot_proof.sh --selftest` (44); `check_py_idiom.py` and `--selftest` (54); `check_baremetal_only.py --check` and `--selftest` (700) | all rc 0 | `receipts/gates/` |
| Doc gates, with the pinned Markdown renderer installed by hash into packet scratch: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_doc_paths.py`, `check_em_dash.py --base dc4d06cb` (0 findings over 157 added lines), `git diff --check` | all rc 0 | `receipts/gates/` |

Details of the `masks` probe, which uses a real event-stream child, the real monitor, act boundary, `run_act_process` and containment:

- the main thread is blocked outside act's window and unblocked inside it;
- the reader thread is blocked throughout;
- neither the event-stream child nor the act child inherits a blocked INT/TERM/HUP;
- the stream is contained, the reader ended and the pipe closed at monitor exit.

The `probe_r2.py` P4 failure is expected:

- P4 asserted Round 2's rule that a reap Refusal replaces the body's failure.
- Round 3's decision 6133149921 reversed that rule: the first failure wins.
- At this head P4's trail shows containment, the reader's end and the pipe close all before exit, with the body's `RuntimeError` kept. That is the required behaviour.

Hosted contexts at the exact head, snapshot (`receipts/hosted-checks-snapshot.txt`):

- 18 completed success;
- 1 skipped (`Physical gPTP`, a scheduled-only context, not hardware proof);
- 6 still in progress: `docs-check`, `elaborate`, `publication-census` and Verilator shards 0, 1 and 4.

The manager owns hosted and act acceptance.

Clone integrity (`receipts/clone-integrity.txt`):

- HEAD and tree match the exact head;
- worktree, index and HEAD are identical;
- index modes, blobs and paths equal the HEAD tree;
- the five gitlinks are unchanged;
- no tracked byte was modified, since all probes ran on copies.

## Lens results

[R632] PASS Conformance - `scripts/act_ci.py:2090-2146, 4671-4760, 5896-5897, 5836-5846`; `.github/workflows/rtl.yml` at head. Checked against acceptance 1-3 and the decisions listed above:

- The derivation reads the materialized checkout's workflows (`:5896`) with a scalar-preserving loader. Its result:
  - the most, over the selected workflows, of the `CONCURRENT_JOB_LIMIT` widest jobs added together;
  - each job's width is act's default 4, its literal `max-parallel` (at least 1), or 1 without a matrix;
  - a non-literal `max-parallel`, or a result above `SLOT_JOB_RANGES`, refuses.
- Shipping derivation: `rtl-full` 4, the other three 1.
- Slot N owns `20N..20N+19`: staging `20N..20N+3`, then four 4-wide ranges, so `nproc` stays 4.
- A host without the derived ranges refuses on every slot, slot 0 included, before the slot is entered (`:5897`).
- Memory bound, swap, `--concurrent-jobs` and the slot cap are unchanged.
- No workflow changed.
- Round 5 decision items 1-3 are met:
  - the hold is taken at `:5729`, before the reader starts and before the yield;
  - the reader inherits the hold;
  - containment, join, dead-thread proof and pipe close all finish before `delivered_after` (`:278`) restores the incoming mask;
  - a held signal is then delivered with 128 + signal, or printed beside an earlier failure;
  - standing controls exist at `:8309`, `:12390` and `:12443`;
  - the doc states the mask at `:1813-1826`.

[R632] PASS RTL - full diff; runner architecture at `scripts/act_ci.py:5313-5351, 5355-5537, 5539-5746, 15565-15580`. No HDL, CDC or interface file is in the diff, so this lens was applied to the runner's own architecture:

- `JobCpuRanges` state transitions are complete. Release happens only on `destroy`, or on a daemon `No such container` from `update` or `inspect`.
- A range is reserved before its update. Uncertainty keeps it reserved. Placement is read by inspect.
- There is one writer thread, and the main thread reads only after the join.
- Thread and signal-mask handoffs are correct:
  - the stream child is spawned before the hold, so it stays killable by the ladder;
  - worker-thread docker CLIs take the SIGKILL-first policy;
  - act's window opens and closes around the spawn only;
  - every runtime thread start (`:366`) blocks the cleanup signals;
  - the only threads alive during a replay are main and the reader (`:5730`).
- CPU arithmetic is exact at the boundaries: 19/20 CPUs for 4 containers and 7/8 for 1 on slot 0, 39/40 on slot 1, and 320 disjoint ranges across slots 0-63.

[R632] PASS Robustness - probes listed above, at this head. Covered:

- restart, out-of-order, lagging, duplicate, foreign and malformed events;
- moves that were applied then timed out, lost, landed late, or were rejected; unreadable inspects; containers gone before their move;
- slot-0 capacity boundaries;
- reap, poll, join and start failures, and a reader held past its bounded wait;
- a first signal at every traced step from monitor entry to exit, sent to the main thread and process-wide (470 runs, 0 failures).

A container left on staging is printed as a warning and never changes a verdict (`:5749-5762`, `:6564`).

[R632] PASS Tests - `scripts/act_ci.py:6564, 7146-7360, 7477-8400, 12390-12470, 14736-14760`; `receipts/selftest-head.log` (507/0); the mutation receipts. Each new arm can fail for its claim:

- earlier campaigns keep their outcomes: 36/36 killed, and 24/30 with Q24 KILLED;
- this round's Round 5 mutants are 12/12 killed;
- the sweep's own control fails 18 times.

The planted overlaps fail the disjointness proof. The dry-run arm prints the shipping `rtl-full` ranges for slot 0 and slot 3.

[R632] PASS Docs - `docs/testing/CI_WORKFLOWS.md:1551-1558, 1724-1891, 2170-2181, 2390`; the PR #731 body at head. These describe the code as built:

- staging and move;
- reservation until `destroy` or inspect-proven absence;
- inspect-read placement;
- derivation and its refusals;
- slot-0 refusal;
- the mixed-runner-version rule;
- the monitor's mask, delivery and precedence;
- the pin list.

All doc gates are rc 0. R1 and R2 are wording only, and S2 is optional.

## Prior public findings, resolved or retained at this head

| Finding | Disposition | Evidence at this head |
|---|---|---|
| R633-1-F1 (MAJOR, all five lenses), `die` frees a range | RESOLVED | `observe` releases on `destroy` only (`:5500`). The adapted probe's F1 passes. `probe_r2` P1 gives A `4-7` and B `8-11`. K01 KILLED |
| R633-1-F2 (MAJOR, all five lenses), an uncertain update frees its target | RESOLVED | `place` reserves before `assign` (`:5462`). Adapted F2, P2 and P2b pass. K02, K03, K07, K08 KILLED |
| R633-1-F3 (MAJOR, all five lenses), the slot-0 fallback | RESOLVED | `job_cpu_ranges` refuses on every slot (`:4719`). P3a, P3b and adapted F3 pass. K15 KILLED |
| R633-1-F4 (MAJOR, all five lenses), cleanup order | RESOLVED | `stop_job_cpu_range_monitor` (`:5585`) runs every step. Adapted F4 passes. K09, K10, K11, K14 KILLED |
| R632-1-F1 (MINOR, Tests and Docs), no arm fails without the join | RESOLVED | busy-reader arms (`:7922`). K10 "reader never joined" KILLED (17 arms) |
| R632-1-F2 (MINOR, Tests), the warning-and-verdict rule is not pinned at run level | RESOLVED | `selftest_cpu_range_warnings` (`:6564`). K23 and K24 KILLED |
| R632-1-R1 and R2 (RESIDUE, Docs) | APPLIED / SUPERSEDED | `CI_WORKFLOWS.md:2178-2181`. The PR body's Layout row states the refusal on every slot |
| R633-2-F1 (MINOR, all five lenses), first failure wins | RESOLVED | `primary` is passed to `stop` (`:5743-5746`). Busy-reader arms for INT/TERM/HUP plus a failed reap. R633-2 monitor probe preserves 143 |
| R632-2-F1 (MINOR, Tests), K12, K13, K32, K36 | RESOLVED | all four KILLED by the unchanged campaign |
| R632-3-F1 (MINOR, Tests), Q24 | RESOLVED | Q24 KILLED by the unchanged campaign |
| R633-4-F1 (MAJOR, all five lenses), a first signal at the cleanup entry skips containment | RESOLVED | The unchanged probe passes all six cases. The standing control is at `:8309`. My sweep includes `:5742`; without the hold at `:5729`, the sweep fails at `:5742` and the next 8 steps |
| R632-2-S2 / R632-3-S2 / R632-4-S2 (SUGGESTION), the cleanup-entry window | ADDRESSED for this monitor by the Round 5 hold | Other cleanup entries named in those suggestions are outside this diff and were not re-examined |
| R632-2-S3 / R632-3-S3 / R632-4-S3 (SUGGESTION), join diagnostic wording | RETAINED | as R632-5-S4 |
| R632-3-S1 / R632-4-S1 (SUGGESTION), Q-series survivors | RETAINED | as R632-5-S3 |

### A concurrent external review at this head, examined after this round's own pass

R633-5-F1 (posted 2026-10-13 03:40 UTC, after this round started) reports MINOR on all five lenses:

- A first signal at `act_ci.py:5351` (act boundary's closing `finally`) replaces an integrity Refusal that is already propagating.
- The boundary's mask-restoring call is skipped.

This round re-examined the claim on its own probes. It does **not** adopt the claim as an open finding, for three reasons.

1. **The delivery point exists only under a line tracer.**
   - In uninstrumented CPython, a Python signal handler runs only at eval-breaker points: function entry, backward jumps and completed calls.
   - The bytecode of `:5351` on its exception path (`receipts/dis-boundary-finally.log`, CPython 3.14.7) contains no such point between the `finally` entry and the `pthread_sigmask` CALL.
   - So without a tracer the handler runs inside that call, after the hold is restored. The tracer adds a checkpoint that real execution does not have.
2. **The tracer-free run shows the restore is kept and the order is right** (`receipts/probe_r632_5-realrace.*`).
   - No tracer is installed. The closing integrity check fails inside one long C call, a 400 MB `str.index` that raises after about 326 ms (`receipts/probe_r632_5-realrace-timing.log`).
   - A helper thread sends SIGTERM to the main thread 20 ms into that call.
   - In 5 of 5 runs, the mask was held when the monitor's cleanup began. The stream was contained, the reader ended and the pipe closed. The run exited 143.
   - That outcome is correct first-arrival order: the signal arrived about 300 ms before the failure existed. From inside Python this case cannot be told apart from R633-5's case, because in both the signal is raised by the restoring call with the failure as its context.
   - R633-5's required outcome (keep the propagating failure at that call) would therefore demote a signal that truly came first, which is the reverse of the precedence the decisions ask for.
   - What remains is a signal arriving during the few unwind instructions between a `raise` and the restoring call. That race is inherent to any exception raised where signals are deliberately unblocked, and act's window must be unblocked.
3. **Containment holds in every case, and the decisions do not cover this one.**
   - This round's traced `precedence` mode (`receipts/probe_r632_5-precedence.log`) delivers 206 signals after the Refusal.
   - The Refusal is kept in 194 of them, at every step from `contextlib` `__exit__` through `delivered_after:299`, which is the monitor's hold.
   - It is replaced in 12. Two are at the tracer-made point `:5351`. Ten are at `contextlib` `__exit__:163-172`, after the monitor has fully exited, which is the runner's ordinary unmasked unwinding and is covered by no decision.
   - The Round 3 and Round 5 precedence decisions cover cleanup failures and held signals. Both hold.

The two reviewers disagree on this point. The manager reconciles it.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #730 acceptance 1-3 and decisions 6131408752, 6131815815, 6132404197, 6133149921, 6133645896, 6134111240; `act_ci.py:2090-2146, 4671-4760, 5313-5351, 5650-5746, 5836-5846, 5896-5897, 15565-15580, 15701-15712`; shipping workflows; dry-run arm | R632-5 | ede700b00ef4d79566a6f108b11ce9bd4ad6beaa |
| RTL | CLEAN (runner architecture; no HDL, CDC or interface file in the diff) | `JobCpuRanges` `:5355-5537`; reader, join, stop and monitor `:5539-5746`; thread starts `:362-381`; mask handoffs `:5313-5351`, `:15565-15580`; CPU arithmetic `:4671-4760`; `receipts/dis-boundary-finally.log` | R632-5 | ede700b00ef4d79566a6f108b11ce9bd4ad6beaa |
| Robustness | CLEAN (S4 SUGGESTION) | probe_r2, probe_r3, probe_shutdown, R633 probes, probe_cleanup_entry; own masks, sweep (470), precedence (206) and realrace (5) | R632-5 | ede700b00ef4d79566a6f108b11ce9bd4ad6beaa |
| Tests | CLEAN (S1, S2, S3 SUGGESTION) | self-test 507/0; `:6564, 7146-7360, 7477-8400, 12390-12470, 14736-14760`; mutants_r2 36/36; mutants_r3 24/30 (Q24 KILLED); own V01-V12 12/12; sweep control (18 failures) | R632-5 | ede700b00ef4d79566a6f108b11ce9bd4ad6beaa |
| Docs | CLEAN (R1, R2 RESIDUE; S2 SUGGESTION) | `CI_WORKFLOWS.md:1551-1558, 1724-1891, 2170-2181, 2390`; PR #731 body at head; doc gates rc 0 | R632-5 | ede700b00ef4d79566a6f108b11ce9bd4ad6beaa |

CLEAN means no BLOCKER, MAJOR or MINOR finding is open under that lens. RESIDUE and SUGGESTION do not affect coverage.

## Real limits

- No live Docker daemon, `docker events`, `docker container update`, act or replay was exercised (disk ruling). Placement, live `nproc`, wall clock, memory peak and the same-head verdict comparison are unmeasured. Physical calibration was not run, and field skips are not hardware proof.
- The signal sweeps use a line tracer to choose delivery points. The tracer-free race probe covers one closing-failure shape only.
- All runs used CPython 3.14.7 with PyYAML 6.0.3. The author's receipts use 3.12.3. The sweep's step count is interpreter-dependent: 185 here, 198 reported there.
- Hosted contexts were still running at the snapshot, and only a snapshot is recorded.
- Optional suggestions R632-2-S2 through R632-4-S2 name other cleanup entries (`replay_slot`, `run_act_process`). Those are outside this diff and were not re-examined.

## Pending manager duties

- Reconcile this POSITIVE with R633-5's NEGATIVE on R633-5-F1. See the analysis above.
- Hosted and act acceptance at the exact head, including the six contexts still in progress at the snapshot.
- Current-dev merge-candidate validation, with builder and native banks, at the merge turn. Source base `dc4d06cb`, live dev `d5858bbee328cf8d2c39a99ec14203f5d0ddd123`.
- Carry R632-5-R1 and R632-5-R2 to the residue checklist.
- Post-merge duties under the ruling:
  - acceptance 3's same-head verdict comparison;
  - acceptance 4's before/after `rtl-full` measurement: per-job wall clock, slot memory peak, the CPU-range summary, and the absence of CPU-range warnings;
  - optional acceptance 5.
- Post-merge containment. The issue stays open until those duties are done.

R632-5 FINISHED
