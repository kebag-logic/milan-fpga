[R820] POSITIVE - exact head 97d83a72f4939ff938917deef33fa1ec1a5ba810

# R820-1 external independent review: issue #102 / PR #103

- Repository: Mister-M-alt/FPGA-gPTP, PR #103 (`102-parallel-mutants` into `main`)
- Exact head: `97d83a72f4939ff938917deef33fa1ec1a5ba810`, tree `c31eb535af8bdc540a298a80bc425112f055dc01`
- Source base: `1616fc8f062fbf58c35ad31674b5b233207bbdb8`. Reviewed delta: `git diff 1616fc8f..97d83a72`
  (4 files: `tb/verilator/engine/mutants.py`, `tb/verilator/engine/Makefile`, `tb/mutation_jobs_test.py`,
  `docs/TEST_DEVELOPER.md`; 2 commits, ab89c60 and 97d83a7)
- Role: external independent reviewer, cleared context, own detached clone. No source edit, commit, push or
  GitHub write was made. No other reviewer's report was read.
- Verdict: **POSITIVE**. No open BLOCKER, MAJOR or MINOR. One RESIDUE (docs wording) and one SUGGESTION.

## 1. Scope, from the issue's frozen acceptance

There is no AGENTS.md or CONTRIBUTING.md at this head. The guidance read was `README.md` and `docs/README.md`
(truth order: RTL, then executable tests, then guides). The scope is issue #102's body. Its comments are only a
TAKEN notice and a REVIEW READY notice, and neither changes scope. The PR comments are review-start notices.

| # | Issue #102 acceptance | Where it is met | Evidence |
|---|---|---|---|
| 1 | Measure every `tb` sub-make and mutant driver under `make all` at main; name the dominant step | PR body section 1; `before/walls.json` | Public receipts at main 1616fc8 (rc 0, 19211.54 s, CPUs 80-95). Engine driver: 18575.7 s, 96.7 %. PR arithmetic rechecked (sections 3.1 and 3.4) |
| 2 | `--jobs N`; default from `os.sched_getaffinity`, small cap such as 8; `--jobs 1` keeps the serial order | `mutants.py:977-983` `default_jobs()`, `:986-1004` `in_list_order()`, `:1007-1012` `jobs_arg()`, `:1023-1026` | Probe 5: affinity 1, 3, 16 gives default 1, 3, 8. `--jobs 0/-1/2.5/x` are rejected (rc 2). `--jobs 1` runs inline on one thread (probe 2: threads 1) |
| 3 | Same mutants, same caught or missed answer, same tally, output in list order; a test compares `--jobs 1` and `--jobs 4` verdict lists byte for byte | `mutants.py:1041-1072`; `tb/mutation_jobs_test.py:90-104`; target `Makefile:65` | Author exact-head receipt `eq/make.log`: 8 PASS, both runs 160 verdicts, 77458 bytes, sha256 `9fb353df…`. Before/after `make all` logs are identical after normalisation (all four arms). The mutant list and constants match base exactly. The test fails on 5 of 5 planted output faults (probe 1) |
| 4 | Every mutant stages in its own temporary directory; no two concurrent mutants share a build or run directory | `mutants.py:948-950, 957` (`tempfile.mkdtemp(prefix="mutant-", dir=work)`) | Probe 2: 159 per-mutant dirs at `--jobs` 1/4/8/16, 160 unique run dirs, 71 unique build dirs, one run per dir. Generator mutants still run the read-only clean executable (`:956-957`) as before #102. The harness opens no file (no `ofstream`/`fopen` in `sim_main.cpp`, no `$fopen`/`$dumpfile`/`$writemem` in `hdl/`) |
| 5 | Same change for any other driver over 10 min serially | PR body section 5 | Public walls: parser 215.3 s, gaskets 33.1 s, tsngen 32.7 s. Every tracked `mutants.py` driver sits in `make all` (top `Makefile` target `tb`, run serially). Unchanged code is correct |
| 6 | `make all` wall time before and after on the same CPUs | PR body section 6; `before`/`after` `summary.json` | Both runs on CPUs 80-95 with rc 0: 19211.54 s, then 2992.85 s. After head 97d83a7, before head 1616fc8 |
| OOS | No mutant or check removed, merged or weakened | `receipts/arm_constants.log` | `MUTATIONS` (159), `RTL_SOURCES`, `GENARGS`, `P1_*`, `VFLAGS`, `PARSER_EDITS`, `GENERATOR` and `verdict` are identical, base vs head. Diff hunks touch only plumbing (`say=` threading, directory, pool) |

## 2. Findings

### R820-1-01 - RESIDUE - Docs

- **Where:** `docs/TEST_DEVELOPER.md:60` and `:62`: "The engine arm runs up to eight mutants at once." /
  "Its `--jobs` option sets that number."
- **Authority/evidence:** `mutants.py:1007-1012` accepts any `--jobs` of at least 1. Eight is only the default's
  cap (`JOBS_CAP`, `:116`). Probe 2 ran `--jobs 16` with 16 workers (17 threads). The Makefile comment
  (`Makefile:54-56`) correctly says the cap applies to the default.
- **Impact:** wording only. A reader may take eight as a hard limit. No measurement, figure, verdict, test, code,
  generated artifact or conformance claim changes.
- **Required outcome (exact fix):** replace line 60 with "By default the engine arm runs as many mutants at once as
  it may use CPUs, at most eight." and line 62 with "Its `--jobs` option sets any other number."
- **Verification:** `make docs` rc 0 after the edit.

### R820-1-02 - SUGGESTION - Tests

- **Where:** `tb/verilator/engine/Makefile:60-66` (the `mutants-jobs-test` target, left out of `all`).
- **Evidence:** the only check that list order survives concurrency is the roughly 5.5 h comparison. No automated
  gate runs it, and `make all` runs only the concurrent arm. The issue does not require it in a gate, and the
  author records the exclusion and its reason, so this is not a defect.
- **Suggestion:** add a seconds-long check to `make all` that runs the real `main()`/`in_list_order()` with fake
  build and harness calls and random delays. Probe 1 in this packet is one such shape: it catches completion-order
  printing and worker-thread printing in about 6 s. A later regression to completion-order output would then fail
  every merge candidate.
- **Verification:** under the new check, plant `as_completed` in `in_list_order` and see it fail.

### Prior public review findings at this head

None exist. PR #103 has 0 reviews and 0 review comments, and its issue-thread comments are review-start notices
only. Nothing is retained or needs resolving.

## 3. Lens results (each applied independently)

### 3.1 Conformance - CLEAN
Each of the six acceptance items and the out-of-scope rule maps to code and receipts (table in section 1). The
receipts are public at kebag-logic/milan-fpga@46a1666, `review-evidence/gptp102-r1`. All 31 files listed in its
MANIFEST.json match their published sha256 values (`receipts/evidence_check.txt`). The receipts show:
- `before/engine-arm.stdout` and `after/engine-arm.stdout` are byte-identical (sha256 `9fb353df…`, 160 `[PASS]`).
- Both whole `make all` logs (902 lines) are identical once per-line timestamps, the two clone paths and the
  build-time summary line are normalised (`receipts/make_log_before_after.txt`). So the ucpu, parser, engine
  suites, gaskets, tsngen and bench tallies are unchanged as well.

The PR body figures were recomputed from `walls.json`: 96.7 %, 98.4 %, 7.84x, 6.42x, -4:30:19 and 89.8 % all
match. The PR body equals the published `PR-BODY.md` apart from one trailing newline.

### 3.2 RTL - CLEAN
The delta touches no `hdl/` or `syn/` file. The RTL the arm mutates and builds is the same at base and head, as
are the build flags and generator arguments (`receipts/arm_constants.log`). `make lint` with Verilator 5.050
(wrapper identity checked: `Verilator 5.050 2026-07-01 rev v5.050`) gives rc 0 on an exact-head extraction.
`make contract` gives rc 0. No RTL behaviour or synthesis claim is made or affected.

### 3.3 Robustness - CLEAN
- **Thread safety:** workers never print; each collects lines through `say=lines.append` (`:1044-1048`), and only
  the main thread prints (`:1066-1072`). The shared state is read-only: the HDL sources and the clean executable.
  `mkdtemp` and `subprocess.run` are safe to call from threads.
- **Exception in a task** (probe 3, OSError planted at mutant 5): `--jobs 1` and `--jobs 4` give identical stdout
  (11 lines), the same traceback and rc 1. No temporary directory is left behind.
- **SIGINT** (probe 4, with the default handler restored the way an interactive Ctrl-C would see it): rc 130 for
  both. `--jobs 1` exits in 0.05 s; `--jobs 4` exits in 1.7 s, after waiting for running tasks as
  `in_list_order`'s `finally` documents. No leftovers. Closing the generator (`contextlib.closing`, `:1054`) keeps
  the temporary directory alive until every running task ends, so a running task never had its directory removed
  (the fake harness checks this, `RuntimeError` arm, never raised).
- **Arguments:** invalid `--jobs` values are rejected with rc 2 and a clear message. The `default_jobs` fallback
  covers platforms without an affinity call (`:979-982`).
- **Resources:** the author's 8-job run peaked at 3.9 G. The pre-existing behaviour on SIGTERM (no cleanup handler)
  is unchanged from base and outside #102.

### 3.4 Tests - CLEAN
The new test (`tb/mutation_jobs_test.py`) was probed against the real driver with only the toolchain faked
(build, image, harness), over the full 159-mutant list (`receipts/stub_summary.txt`, probe 1):

| Planted fault | Test result | Checks that failed |
|---|---|---|
| none (head) | PASS 8/8 | - |
| results yielded in completion order (`as_completed`) | FAIL | verdict lists, stdout |
| workers print their own lines (`say=print`) | FAIL | verdict lists, stdout |
| concurrent path drops the last task | FAIL | verdict lists, stdout, `--jobs 4` count and tally |
| both modes abort after the control (equal output) | FAIL | count and tally for both runs |
| both modes skip the last mutant (equal output) | FAIL | count and tally for both runs |
| all mutants in one directory (pre-#102 layout) | PASS | none expected: tags are unique (159/159), so no collision |

The "two equal aborts" guard (`:97-104`) is therefore load-bearing. The fake-toolchain head output at `--jobs`
1/4/8/16 and the base driver's serial output are byte-identical (sha256 `8c7ac124…`, 160 checks). The test's
exact-head real-toolchain run (author receipt `eq`) passed 8/8 with 160 verdicts in each mode. `py_compile` is
clean for both changed Python files.

### 3.5 Docs - CLEAN (one RESIDUE recorded)
- `docs/TEST_DEVELOPER.md` adds the new file and target to its tables and four lines on `--jobs`. "One job keeps
  the serial order" and "Verdicts always print in mutant list order" are accurate (probes 1 and 2). "Up to eight"
  needs qualifying: R820-1-01, RESIDUE.
- The Makefile comments (`:50-56`, `:60-64`) and the module and function docstrings (`mutants.py:27-32`,
  `:926-934`, `:986-993`; `mutation_jobs_test.py:4-22`) match the code.
- No stale "serial" or wall-time claim remains in the current guides.
- `make docs` (`check_docs`, its selftest, `check_source_evidence` and its selftest, diagrams check and its selftest)
  and `make diagrams-check` give rc 0. `syn/ooc/check_ooc_clock.py --selftest` gives rc 0.
- **Comment rule:** the added lines carry issue IDs (`#102`) only. No bench lane label, lane name, review round,
  reviewer ID or issue-comment ID appears in the delta (grep of all `+` lines, no match). No RESIDUE under the rule.

## 4. Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #102 body and comments; PR #103 body and comments; public receipts gptp102-r1 (before, after, eq, probe, gates, manifest); `mutants.py`; `Makefile`; arm constants base vs head | R820-1 | 97d83a72f4939ff938917deef33fa1ec1a5ba810 |
| RTL | CLEAN | diff stat (no `hdl/`/`syn/`); `RTL_SOURCES`/`VFLAGS`/`MUTATIONS` identity; `make lint`; `make contract` | R820-1 | 97d83a72f4939ff938917deef33fa1ec1a5ba810 |
| Robustness | CLEAN | `in_list_order`, `main`, `run_mutant`, `default_jobs`, `jobs_arg`; probes 3 (exception), 4 (SIGINT), 5 (arguments, affinity) | R820-1 | 97d83a72f4939ff938917deef33fa1ec1a5ba810 |
| Tests | CLEAN | `tb/mutation_jobs_test.py`; 7-fault matrix (probe 1); full-list equivalence at `--jobs` 1/4/8/16 and base (probe 2); author exact-head `eq` receipt | R820-1 | 97d83a72f4939ff938917deef33fa1ec1a5ba810 |
| Docs | CLEAN (R820-1-01 RESIDUE) | `docs/TEST_DEVELOPER.md`; Makefile comments; docstrings; comment-rule grep; `make docs`; `make diagrams-check` | R820-1 | 97d83a72f4939ff938917deef33fa1ec1a5ba810 |

## 5. Real limits

- **No real-toolchain rerun of the engine arm.** The host's load average was about 170-190 while this review ran,
  and each foreground command is limited to 10 minutes. A control-plus-one-mutant real run was capped at 560 s and
  did not reach a verdict: both arms returned rc 124 (`receipts/real1/`). The cap was hit; this is not a verdict.
  So real-toolchain equivalence rests on the author's public exact-head receipts (`eq`, `after`) and the base
  receipt (`before`). My own executed equivalence evidence uses the real driver logic with the toolchain faked.
- An earlier batch of my own probes was invalidated by my own cleanup, which removed its temporary directories
  while it ran. Those receipts were discarded, not published, and nothing is concluded from them.
- No wall-time measurement of my own. The before/after figures are the author's, taken on CPUs 80-95 of a host the
  author describes as fully booked.
- No hosted check exists at this head: 0 check runs; combined status `pending` with 0 contexts. Nothing hosted was
  executed or skipped to inspect. Hosted/act acceptance belongs to the manager.
- No manager source bank runs at this exact head, and none is claimed or inferred. Physical calibration was NOT
  RUN; nothing here is hardware proof.
- The PR has no `hdl/` change, so `make ooc` synthesis was not run (and is not part of `make all`).

## 6. Pending manager duties

- Build and validate the current-dev merge candidate (source base 1616fc8f, live dev 45c0b56c1f4a8a52878815fdcb1359d18e2c5b1c)
  with the builder and native banks at the merge turn, and link the receipts on the PR.
- Own hosted/act acceptance for this change.
- Carry R820-1-01 (RESIDUE, exact fix above) to the residue checklist.
- Decide on R820-1-02 (SUGGESTION): whether to add a fast automated ordering check to `make all`.
- Merge still needs the second independent positive review and the full completion bar.

## 7. Clone restoration

The clone was never edited. The only artifacts were three ignored `__pycache__` directories from a read-only import
check, and they were removed. Verified (`receipts/clone_restore.txt`):
- HEAD `97d83a72…`, tree `c31eb535…`; `git status --porcelain --ignored` is empty.
- Worktree == index == HEAD.
- Index vs tree (mode, sha, path) shows 0 differences; worktree blob re-hash shows 0 mismatches and 0 mode
  mismatches.
- Submodule gitlinks: none at this head, and none at base, so none are required.

## 8. Packet contents

- `scripts/`: `make_variants.py` (disposable driver variants), `stub_probes.sh`, `summarize_stub.py`,
  `real1_probes.sh`, `job.sh`, `compare_arm_constants.py`, `compare_make_logs.sh`.
- `receipts/`: `stub/` (raw), `stub_summary.txt`, `gates/`, `real1/`, `arm_constants.log`, `evidence_check.txt`,
  `make_log_before_after.txt`, `clone_restore.txt`.
- Scripts take every tree and receipt path as an argument.
- Disposable trees (exact-head extractions, variants, downloaded public evidence, temporary build directories) live
  under `scratch/` and are not published.

R820-1 FINISHED
