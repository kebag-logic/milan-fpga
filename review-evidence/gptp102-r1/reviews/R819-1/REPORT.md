[R819] POSITIVE - exact head 97d83a72f4939ff938917deef33fa1ec1a5ba810

# R819-1 internal independent review: issue #102 / PR #103

- Repository: Mister-M-alt/FPGA-gPTP, PR #103 (`102-parallel-mutants` into `main`), round R819-1.
- Exact head `97d83a72f4939ff938917deef33fa1ec1a5ba810`, tree `c31eb535af8bdc540a298a80bc425112f055dc01`; source base `1616fc8f062fbf58c35ad31674b5b233207bbdb8`.
- Delta: `docs/TEST_DEVELOPER.md` (+10), `tb/mutation_jobs_test.py` (new, 119 lines), `tb/verilator/engine/Makefile` (+13/-3), `tb/verilator/engine/mutants.py` (+118/-37). No `hdl/`, `syn/`, `bench/` or generated artifact changes.
- Reviewer: internal role, cleared context, own detached clone. No source edits, commits, pushes or GitHub writes.

## Verdict

POSITIVE. Every acceptance item of #102 is met at the exact head, and I verified each one independently with executable evidence. One RESIDUE (prose only) and one SUGGESTION are recorded. Neither blocks the verdict.

## Reconstructed scope (issue #102 body; no maintainer or manager scope comments beyond TAKEN / REVIEW READY)

| # | Acceptance item | Result at this head | Evidence |
|---|---|---|---|
| 1 | Measure every `tb` sub-make and every mutant driver under `make all` at `main`; name the dominant step | Met | Author receipt `before/walls.json` (base `1616fc8f`, affinity 80-95): engine `mutants.py` 18575.7 s of 19211.5 s (96.7 %). I recomputed every PR §1/§6 figure (shares, 7.84x, 6.42x, -4:30:19, 89.8 %) from the receipts. |
| 2 | `--jobs N`; default from `os.sched_getaffinity`, small cap (8); `--jobs 1` keeps serial order | Met | `tb/verilator/engine/mutants.py:977-1012,1022-1027`. Probe P4: default 1/3/8 under 1/3/16 CPUs; `--jobs 1` runs one task at a time in list order; `0`, `-1`, `abc`, `1.5` rejected with rc 2 before any build. |
| 3 | Same mutants, same verdict each, same tally, list-order output; a test compares `--jobs 1` and `--jobs 4` byte for byte | Met | Test `tb/mutation_jobs_test.py`, target `tb/verilator/engine/Makefile:65-66`. Author `eq/make.log`: rc 0, 8/8 PASS, both 77458 bytes, sha256 `9fb353df…74b2`. My full arm at `--jobs 8` (campaign A): byte-identical to author's base-serial and head receipts. My subset (B/C): base serial == head `--jobs 1` == head `--jobs 4`, across every verdict branch. Mutant list and helpers unchanged (P5). |
| 4 | Each mutant stages in its own temporary directory; no two concurrent mutants share a build or run directory | Met | `mutants.py:948-959` (`mkdtemp` per mutant; `src_`, `run_`, `obj_` under it). Mid-run snapshot `A_isolation_snapshot1.txt`: 7 in-flight mutants, each in its own `mutant-*` tree. Generator mutants execute the clean build's executable read-only (pre-existing cost design, `mutants.py:23-25`). The harness writes no file (`run_clean` holds only its images). |
| 5 | Same change for any other driver over 10 min serially | Met (none qualifies) | `before/walls.json`: parser 215.3 s, gaskets 33.1 s, tsngen 32.7 s. |
| 6 | `make all` wall time before and after, same CPUs | Met | `before`/`after` `summary.json`: both affinity 80-95, consecutive, rc 0; 19211.54 s to 2992.85 s. |
| Out of scope | No mutant or check removed, merged or weakened | Respected | P5: 159 = 159 `MUTATIONS` entries identical; `RTL_SOURCES`, `GENARGS`, `P1_*`, `VFLAGS`, `PARSER_EDITS`, `GENERATOR`, `stage`, `generate_image`, `build`, `run_harness`, `_named_failure`, `verdict` source-identical. `named_verdict`/`run_mutant` changed only `print` to `say`, with identical message text. |

## Findings

### R819-1-F1 - RESIDUE - Docs

- Where: `docs/TEST_DEVELOPER.md:60` "The engine arm runs up to eight mutants at once."
- Authority/evidence: `mutants.py:1022-1027`. Eight is only the default cap. An explicit `--jobs 12` runs twelve at once (no cap applies to an explicit value; P4).
- Impact: prose only. The sentence states a default as an absolute bound. The next line ("Its `--jobs` option sets that number.") partly corrects it. No figure, test, code, verdict or clause claim changes.
- Required outcome (exact fix): replace line 60 with `By default, up to eight engine mutants run at once.`
- Verification: P6 (`receipts/P6_residue_fix_docs_gate.log`). Two longer phrasings fail the docs gate's word limit (12 and 11 words). This 10-word line passes `scripts/check_docs.py` (rc 0) and its selftest (attempt 3). Every attempt was applied only in a disposable copy, then restored.

### R819-1-S1 - SUGGESTION - Tests, Docs

- Where: `tb/verilator/engine/Makefile:60-66`, `tb/mutation_jobs_test.py:19-21`, `docs/TEST_DEVELOPER.md:49`.
- Observation: the list-order and `--jobs` equivalence property is guarded only by `mutants-jobs-test`. That target takes about 5.5 h (author `eq` receipt: 19741 s) and `make all` leaves it out, for reasons the Makefile and test docstring state. A future scheduler regression (for example, completion-order yielding) would still pass `make all`: the arm's rc and tally are unchanged by ordering.
- Suggestion: add a cheap in-gate guard, such as a unit check of `in_list_order` with out-of-order completion, or the driver comparison on a fixed small subset. Also state the target's runtime, and that `make` omits it, in the test guide row. Not required by #102, which asks for the test (present and executed). Does not affect the verdict.

No BLOCKER, MAJOR or MINOR findings.

## Independent executable evidence (this round)

Toolchain: scoped Verilator `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator`, verified `Verilator 5.050 2026-07-01 rev v5.050`. Its `VERILATOR_ROOT` overlay is the same one named in the author's `summary.json`; it is first on `PATH` via a symlink. Python 3.14.9. All runs used extracted copies of the exact head and base under the never-published scratch directory, a private `TMPDIR` each, and `taskset` inside 16 CPUs. Peak concurrency was at most 16 driver jobs. Unit `memory.peak` was 6.15 GB, under the 12 GB cap.

| ID | What | Result | Receipts |
|---|---|---|---|
| A | Full engine arm at head, `--jobs 8` (159 mutants + control) | rc 0, `160 checks: 160 PASS, 0 FAIL`, 77458 bytes, sha256 `9fb353df86cecf91cd2d782904f7543f809a5e8d649ae2c068c69c8d1ccc74b2`, stderr empty. `cmp`-identical to the author's base-serial (`before/engine-arm.stdout`) and head (`after/engine-arm.stdout`) receipts. Temp tree removed. Wall 2:05:58 on a host under load average 100-200; no timing claim drawn. | `A_full_head_jobs8.*`, `A_compare.txt`, `A_isolation_snapshot1.txt`, `A_memory_samples.txt` |
| B | `tb/mutation_jobs_test.py` (unmodified) on a 9-entry subset driver copy: 4 real mutants (RTL `#100`, RTL `slew:`, two generator) + 5 planted faults (pattern missing, survivor, build failure, generator refusal, named check missed), slow entry first so completion order differs from list order | rc 0, 8/8 PASS; `--jobs 1` and `--jobs 4` both exit 1, 2540 bytes, sha256 `9175803c…7f82`, 10 verdicts; 2724 s vs 956 s | `B_subset_eq_head.*`, `B_out/` |
| C | Same subset on the base `1616fc8f` driver, serial | `cmp`-identical to B's `--jobs 1` and `--jobs 4` stdout; stderr empty in all three | `C_subset_base_serial.*` |
| M1 | Planted defect: `in_list_order` yields in completion order (`as_completed`); test checks run on head `--jobs 4` against B's recorded serial run | Caught: 5 checks FAIL (verdict lists, stdout, stderr traceback, verdict count 3/10, tally missing) | `M1_order_mutant.*` |
| M2 | Planted defect: the printer drops each mutant's last line | Caught: verdict count 1/10 FAIL. This count check alone catches it even when both halves share the defect. | `M2_drop_mutant.*` |
| P3 | Test power against 8 fake drivers (good, reordered, abort-alike, stderr diff, rc diff, wrong tally, extra verdict, extra named line) | 8/8 as expected: only `good` passes | `P3_fakes.log` |
| P4 | `in_list_order` / `default_jobs` / `--jobs` parse unit probes | 29/29 PASS. My first log has 2 FAILs: my probe wrongly expected FIFO start order with 32 workers for 20 tasks, where threads start lazily and race. Result order passed there too; the corrected probe is the second log. | `P4_scheduler_first.log`, `P4_scheduler.log` |
| P5 | Mutant list and helper identity, base vs head | All SAME | `P5_mutation_lists.log` |
| I3/I4 | SIGINT to the process group mid-run (Ctrl-C) | Head `--jobs 4`: rc 130, exit 15.1 s after SIGINT. Base serial: rc 130, 0.5 s. Both leave no process and no temp entry. An earlier attempt was void: background jobs of a non-interactive shell ignore SIGINT. Kept as `*_flawed*`. | `I3_*`, `I4_*`, `I1_*_flawed*`, `I2_*_flawed*` |
| G | Light source gates on an extracted head copy: `make contract`, `make docs`, `make diagrams-check`, `make lint`, the four selftests, `make -n` of the engine default, `mutants-jobs-test` and `tb` | All rc 0. Docs selftest 127 arms, source evidence 7, diagrams 10, ooc clock 30. `make -n` confirms `all: run mutants` is unchanged and the new target is outside `all`/`tb`. | `G_gates.*` |
| - | Clone integrity after all probes | HEAD, tree and index tree = exact head; worktree/index/modes equal HEAD; no untracked or ignored files. The repository tracks no submodule gitlinks and no `.gitmodules`, so none are required. | `clone_integrity_mid.txt`, `clone_integrity_final.txt` |

Public evidence (`kebag-logic/milan-fpga@46a1666…/review-evidence/gptp102-r1`): all 31 `MANIFEST.json` entries match their published sha256. Receipts used: `before/`, `after/` (`walls.json`, `summary.json`, `engine-arm.stdout`, `make.log`), `eq/`, `gates/`, `probe/`. The PR body equals the published `PR-BODY.md` apart from one trailing newline. Hosted CI: the repository has no workflows, and the exact head reports 0 check runs and 0 statuses. No hosted job executed, so none was skipped.

## Lens notes

- Conformance: scope is issue #102's six items plus the out-of-scope rule. All met (table above). PR §1-§6 figures recomputed from receipts.
- RTL: the delta touches no RTL or microcode. Every mutant's RTL/generator pattern and replacement is identical to base (P5). `make lint` passes with the pinned 5.050.
- Robustness: thread use is confined. Each task writes only its own `mkdtemp` tree and a per-task line list; `print` runs only on the main thread; shared inputs (`HDL` sources, clean executable) are read-only. Exceptions propagate in list order after earlier results, leaving no running task (P4). `contextlib.closing` plus `shutdown(wait=True, cancel_futures=True)` drains workers before the temp tree is removed (P4 close probe, I3). Interrupt latency is bounded (15.1 s observed). Memory at 8 jobs plus 6 more jobs stayed at 6.15 GB unit peak.
- Tests: the new test's checks are load-bearing: 8 fake-driver plants (P3) and 2 driver plants (M1, M2) are all caught. The test was executed by the author at exact head (rc 0); my independent full-arm and subset runs agree.
- Docs: new rows and four lines in `docs/TEST_DEVELOPER.md`; `make docs` passes. One RESIDUE (F1). Comment rule: the delta's comments and docstrings cite only `#102` and behaviour. No lane label, lane name, review round, reviewer ID or issue-comment ID was found (grep over all added lines).

## Prior public review findings at this head

I read these after this verdict and ledger were written. The PR has no reviews and no review comments. One public review result was posted during this round: the external review's R820-1 (issuecomment-6775284988), POSITIVE at this exact head. The other comments are manager status posts. Its two findings, as they stand at this head:

- R820-1-01 (RESIDUE, Docs, `docs/TEST_DEVELOPER.md:60,62`): RETAINED, open as RESIDUE. It is the same defect as R819-1-F1. Its stated exact fix makes `make docs` fail: in P6 attempt 4, line 60 becomes 19 words and `scripts/check_docs.py` returns rc 1 on the word limit. The 10-word replacement in R819-1-F1 passes the gate (P6 attempt 3). The manager should carry the gate-passing text to the residue checklist.
- R820-1-02 (SUGGESTION, Tests): RETAINED as SUGGESTION. It concurs with R819-1-S1.

Neither changes this verdict.

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #102 body and comments; PR #103 body; `before/after/eq/probe` receipts; `mutants.py:977-1076`; campaigns A, B, C; P4, P5 | R819-1 | 97d83a72f4939ff938917deef33fa1ec1a5ba810 |
| RTL | CLEAN | Diff stat (no `hdl/`, `syn/`, `bench/` change); P5 pattern/replacement identity of all 159 mutants; `make lint` (G) | R819-1 | 97d83a72f4939ff938917deef33fa1ec1a5ba810 |
| Robustness | CLEAN | `in_list_order`, `run_mutant`, `main` scheduling/cleanup; isolation snapshot; P4 exception/close probes; I3/I4 interrupt; unit memory peak | R819-1 | 97d83a72f4939ff938917deef33fa1ec1a5ba810 |
| Tests | CLEAN | `tb/mutation_jobs_test.py`, `Makefile:60-66`; author `eq` receipt; B, C, M1, M2, P3; S1 recorded as SUGGESTION | R819-1 | 97d83a72f4939ff938917deef33fa1ec1a5ba810 |
| Docs | CLEAN (RESIDUE F1 carried) | `docs/TEST_DEVELOPER.md:23,49,60-66`; `mutants.py` docstring; `Makefile` comments; `make docs` and selftest; P6 fix probe; comment-rule grep | R819-1 | 97d83a72f4939ff938917deef33fa1ec1a5ba810 |

## Real limits

- My full-arm run (A) used `--jobs 8` only. I did not repeat the serial 5 h full run. Full-arm serial equivalence rests on: the author's `eq` receipt (`--jobs 1` vs `--jobs 4` at this head), the author's base-serial `make all` receipt, and my A output being byte-identical to that base-serial receipt. My own serial-vs-concurrent comparisons (B, C) cover a 9-entry subset reaching every verdict branch.
- M1/M2 reuse B's recorded `--jobs 1` output rather than re-running the serial half. The planted defects do not touch the serial path, except M2, which the count check catches regardless.
- Timings: my host was under load average 100-200, so my wall times are not comparable with the PR's. I make no speed claim. The PR's before/after timings rest on the author's receipts (same affinity, consecutive runs).
- The 3.9 G memory peak in the PR body comes from the author's unit accounting, stated in the published handoff. It has no raw receipt. It is not an acceptance item.
- No hosted CI exists for this repository. No manager source bank ran at this head, and I claim none. Physical calibration was NOT RUN, and nothing here is hardware proof.

## Pending manager duties

- Carry RESIDUE R819-1-F1 (exact fix above) to the residue checklist. It is the same item as R820-1-01; use the fix text that passes the docs gate (P6).
- Build and validate the current-dev merge candidate (source base `1616fc8f`, live dev `45c0b56c1f4a8a52878815fdcb1359d18e2c5b1c`) with the builder and native banks at the merge turn, and link its receipts on the PR.
- Own hosted/act acceptance and the second independent review (R820) before merge.

R819-1 FINISHED
