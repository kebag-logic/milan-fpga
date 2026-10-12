[R626] NEGATIVE - exact head 61296ea1fbbb456bd9bc4d7ed93af37d0dfaf6d3

Round R626-2 is the internal cleared-context review of issue #727 / PR #728: a full review at the exact head plus the round-2 delta `a57d384d..61296ea1`.

- Head `61296ea1fbbb456bd9bc4d7ed93af37d0dfaf6d3`, tree `8fd4dbd4f35e3892f7df8f2e404302e3658d443d`, source base `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`.
- Diff: `scripts/suite_shards.py` (+580/-92) and `docs/testing/CI_WORKFLOWS.md` (+33/-19). Six commits, each one line with no trailers (`receipts/commit-format.txt`).
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs.

The verdict is NEGATIVE for one open MINOR, F1 (Docs, Robustness), which is new in this round.

All round-2 work checks out:

- R626-1/F1 = R627-1-F1 is resolved. The new arm computes `minutes * 36` without `bound_seconds` or `HEADROOM_PERCENT`. R626-1's unmodified `mutate.py` gives rc 1 for `headroom-75-percent`, `headroom-100-percent` and `bound-formula-div10`, and in each the only failure is that arm reporting ESCAPED. `tree-head` gives rc 0.
- The zero-duration and six-worker plants are refused, and each escapes under its mutant.
- The R1 wording is applied.
- The assignment is byte-identical to round 1.

F1 is a gap that neither earlier round reached. Prior reviews checked the serial `--list`; this round checked the full serial sweep. When a default suite has no recorded duration, the mandatory serial local sweep now stops at its preflight. The gate's own error message then points to a refresh procedure that cannot produce that figure. Neither fact is in the repository's documentation.

## Context reconstructed

- AGENTS.md, CONTRIBUTING.md and docs/README.md.
- Issue #727: body (acceptance 1-4), lane assignment 6121794007, TAKEN 6121909841, REVIEW READY 6122246247, the round-2 decision 6126048117 and REVIEW READY 6126250528.
- PR #728 body at the head.
- Authorities:
  - `.github/workflows/rtl.yml`: job `verilator-shards` at :147-157, the ownership step at :208-222 and the physical job's self-test at :364.
  - `scripts/run_all_suites.sh`: selection at :168-189, preflight at :291-295, `main` at :447-454.
  - `scripts/suite_tally.py:388-417`, the aggregate's inventory check.
  - `docs/testing/{CI_WORKFLOWS,TESTING,RUNNING_TESTS}.md`.
- `git diff c6bd08c6..61296ea1` and `git diff a57d384d..61296ea1`, with their history.
- Public evidence at `b98797c2:review-evidence/727-r1`:
  - `reviews/R626-1/scripts/mutate.py`. Its sha256 `571bd0aa...fcfc031` equals its `MANIFEST.sha256` entry. It was run unmodified.
  - The R626-1 and R627-1 findings, read only after this round's independent verdict was recorded (`receipts/verdict-before-prior.txt`).
- Hosted logs: dev run 38217650945 (event `schedule`, dev `c6bd08c6`, all five Verilator jobs `success`) and run 38208503834 (#696 head `26e2748f`, worker 1/5 job 114677344710). These were fetched by the docstring's own commands. Their sha256 values are in `receipts/hosted-log-sha256.txt`.

## Findings

### F1 - MINOR - Docs, Robustness - adding a default suite: the gate's remedy cannot cure it, and the serial sweep's new precondition is undocumented

Artifacts: `scripts/suite_shards.py:192-194` (message "refresh it as the module docstring says"), `:27-48` (refresh procedure), `:649-662` (head arms); `scripts/run_all_suites.sh:291-295`, `:447-453`; `docs/testing/TESTING.md:513`; `docs/testing/CI_WORKFLOWS.md:191-198`; PR body lines 36 and 151.

**Authority and evidence.**
- AGENTS.md section 5 says to "update authoritative documentation when behavior or architecture changes". The Docs lens says "Changed contracts are reflected in authoritative docs". The Robustness lens covers configuration-dependent behavior.
- At base, a planted unmeasured suite passes `suite_shards.py --selftest` (rc 0, `receipts/base-vs-head-planted-suite.txt`). At the head the same plant fails it (rc 1).
- The serial sweep runs that self-test as a preflight (`run_all_suites.sh:291`, after `select_suites` and before any suite runs). So on a full-tree copy of the head with one planted suite, `scripts/run_all_suites.sh <out>` exits 2 after 41 s with `ABORTING: scripts/suite_shards.py fails its own self-test` (`receipts/serial-sweep-planted-suite.log`).
- `TESTING.md:513` still describes this as "the mandatory serial local sweep" with no new precondition. The PR body says both "The serial `0/1` sweep needs no table and is unchanged" (line 36) and that the local preflight now needs a duration (line 151). The PR body is not durable documentation.
- The gate's message says to "refresh it as the module docstring says". That procedure measures an rtl-full dev run, which cannot contain a suite that is not yet on dev. Following it verbatim, with `maap` kept at 1375 as the docstring requires, leaves the failure in place: `FAIL head: zz_unmeasured ...`, rc 1 (`receipts/refresh-does-not-cure-new-suite.txt`).
- The PR's own hosted run cannot measure the new suite either. Each worker's ownership step runs `--selftest` under `set -euo pipefail` (`rtl.yml:213-214`) before any suite runs.
- The docstring's pull-request exception (`:46-48`) covers a figure that has already been measured. Nothing says where the first figure comes from.

**Impact.**
- Every future change that adds or renames a default Verilator suite first hits an abort of the mandatory serial local sweep and of every hosted worker. The gate then names a remedy that does not work.
- The author must invent a provisional figure with no stated source, and that figure feeds the 60 % prediction.
- The fail-closed behaviour itself is correct and required by acceptance 1. The defect is the undocumented contract change and the wrong remedy for the gate's main failure case.

**Required outcome.**
- The selector's docstring states what a change that adds a default suite records. It names the source of the first figure, and says how that figure is replaced from the change's own hosted run with `--measure`, as the pull-request exception already allows. The gate's message must point to a remedy that cures it.
- The authoritative testing documentation states that the selector's self-test, and therefore the serial sweep's preflight and every hosted worker, refuse to start until `SUITE_SECONDS` names every default suite.
- The design is not prescribed. If the maintainer instead rules that the serial preflight should not depend on the table, that is an equally valid outcome, published as a decision.

**Verification.**
- In a disposable copy with a planted suite, follow the documented new-suite steps verbatim. `--selftest` then exits 0 and the serial sweep passes its preflight.
- The doc gates (`docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py`, `check_doc_paths.py`) exit 0.

**Why not Conformance.** Acceptance 4 asks how the table is refreshed from a hosted run, and the procedure does that for the inventory it measures (verified below). Acceptance 1's fail-closed case behaves as required.

### S1 - SUGGESTION - Tests - `scripts/suite_shards.py:488-504`, `:234-235` - the determinism arm cannot detect a split that differs between processes

- `split_selftest` compares two selections made in one process. A tie-break on `hash(suite)` passes the self-test (rc 0; probe case `tie-by-hash`, and R626-1's case `nondeterministic-tie`).
- Under that mutant, five worker processes with different hash seeds give a union of 50-54 distinct suites, with 7-8 run twice (`receipts/tie-by-hash-crossprocess.txt`).
- The head's tie-break is lexical. Its lists are identical under `PYTHONHASHSEED` 0, 1, 2, 12345 and random, and under CPython 3.12.13 and 3.14.7.
- The hosted aggregate fails closed on a MISSING or DUPLICATE suite log (`suite_tally.py:390-416`).
- Option: one arm that runs `--shard I/N` in subprocesses under two hash seeds and compares them.

### S2 - SUGGESTION - Tests, Robustness - `scripts/suite_shards.py:541-545`, `:652-655` - forcing `in_checkout()` to False drops every head arm and still reports PASS

This is retained from R626-1/S1 and reproduced here: R626-1's `head-arms-skipped` gives rc 0 at this head.

### R1 - RESIDUE - Docs - `.github/workflows/rtl.yml:136-137` - comment still says "four hashed workers"

This is retained from R626-1/R2. The round-2 decision keeps `rtl.yml` byte-unchanged (acceptance 2) and routes the comment to #495. The defect is still in the tree.

Exact fix: "four workers balanced by measured hosted time (#727)".

### R2 - RESIDUE - Docs - PR #728 body, line 36 - "The serial `0/1` sweep needs no table and is unchanged."

The selection needs no table and is unchanged. The sweep's preflight, however, now requires one (F1, and the PR body's own line 151).

Exact fix: "The serial `0/1` selection needs no table and is unchanged; the sweep's preflight runs `--selftest`, which needs every suite in the table."

## Prior public findings at this head

| Prior ID | Disposition | Evidence |
|---|---|---|
| R626-1/F1 = R627-1-F1 (MINOR, Tests) | RESOLVED | `:604-611` builds `expected = {m: m * 36}` from the applied bounds, and never calls `bound_seconds` or reads `HEADROOM_PERCENT` there. At the head it prints `{116: 4176, 117: 4212, 120: 4320}`. R626-1 `mutate.py`: `headroom-75-percent`, `headroom-100-percent` and `bound-formula-div10` each give rc 1, and the new arm is ESCAPED as the only failure (5400, 7200 and 43200 s at 120). `tree-head` gives rc 0. The reviewer's own subtler mutants `headroom-61` (4392 s) and `bound-plus-one` (4321 s) are also caught (`receipts/r626-1-mutate-at-61296ea1.out`, `receipts/probe_727.txt`). |
| R626-1/R1 = R627-1-R1 (RESIDUE) | RESOLVED | `CI_WORKFLOWS.md:191-194` reads "All figures come from one dev run, except `maap`, which keeps #696's figure from its pull-request run until a dev run measures that change." That matches `suite_shards.py:86-89` and `:46-48`. |
| R627-1-R2 (RESIDUE, PR body) | RESOLVED | PR body line 149 reads "Overheads assume warm Verilator and Yosys caches; worker 1's overhead includes the tsn-gen build." |
| R626-1/R2 (RESIDUE) | RETAINED as R1 above | `rtl.yml:136` still says "four hashed workers". Routing it to #495 does not change the tree. |
| R626-1/S1 (SUGGESTION) | RETAINED as S2 above | `head-arms-skipped` gives rc 0 at this head. |
| R626-1/S2 (SUGGESTION) | RESOLVED | The zero-duration arm `:585-588` and the six-worker arm `:613-620` were added. `table-zero-duration-allowed` and `worker-count-mirrored-5` each give rc 1 with their arm ESCAPED as the only failure. |

## Per-lens results

[R626] PASS Conformance - `scripts/suite_shards.py:90-158` at 61296ea1. Receipts: `measure-38217650945.txt`, `independent-38217650945.json`, `independent-38208503834.json`, `independent-split.txt`, `lists/`, `selftest-head-py314.txt`, `gates/selector_selftest_py312.log`, `round1-vs-round2-lists.txt`; `git diff --quiet c6bd08c6 HEAD -- .github` (rc 0). Checked against #727 acceptance 1, 2 and 4, assignment steps 1-5 and round-2 decision items 1-4:

1. **The refresh procedure runs as written.** The docstring's `gh` commands were run verbatim on run 38217650945, then `--measure` (rc 0). The result reproduces all 61 dev figures and `WORKER_OVERHEAD_SECONDS = (83, 115, 80, 93, 80)` exactly. `maap` measures 185 s on dev, and the docstring keeps it at 1375.
2. **An independent parser agrees.** `scripts/independent_measure.py` uses Decimal timestamps and does not import the selector. It gives the same 62 ceilings and the same five overheads. Every window is a PASS.
3. **`maap` follows the assignment's window rule.** In run 38208503834, worker 1/5, the window from 06:40:57.0569333Z (`lat_history_ring`) to 07:03:51.2344068Z (`maap`) is 1374.1774735 s, which rounds up to 1375. The issue quotes about 1,380 s. With 1380 planted, the self-test still passes and the worst worker is 4210 s.
4. **The split is reproduced independently.** A separate longest-first, least-loaded implementation (`scripts/independent_split.py`) gives the same owners. Predicted times are 4204, 4205, 4203, 4205 and 2877 s against 4320 s, which is 60 % of `rtl.yml`'s `timeout-minutes: 120`.
5. **The split is deterministic, disjoint and complete.**
   - The five lists are identical across hash seeds 0, 1, 2, 12345 and random, and on CPython 3.12.13 and 3.14.7.
   - They hold 15, 16, 14, 16 and 1 suites. Their union equals the 62-suite serial inventory, with no suite twice.
   - Shard 4/5 is exactly `milan_dp`, `tsn_fuzz` is in 1/5 and `chmap_capture` is in 3/5.
6. **Round-1 behaviour is unchanged where it should be.** The serial 0/1 selection and `--physical-gptp` output are byte-identical to the base selector's. All five lists are byte-identical to `a57d384d`'s. `table_problems`, `balance`, `select_suites`, `verilator_job_limits`, `bound_seconds`, `headroom_problems`, `measure_log`, `measure_main` and `main` are textually unchanged since round 1. `rtl.yml` is byte-unchanged and the worker count is still five.

[R626] PASS RTL - `git diff --name-only c6bd08c6 HEAD` (only the two files) and caller contracts at `scripts/run_all_suites.sh:168-189,291-295`, `scripts/suite_tally.py:388-417`, `.github/workflows/rtl.yml:208-222,364`, `scripts/test_suite_cancellation.py:87-89`. No HDL, testbench, workflow or gitlink changed, so clock, reset, CDC, width and FSM concerns do not apply. The selector's CLI and its argparse refusal exit 2 are preserved. The gates that import or wrap the selector exit 0: `measure_test_evidence.py --check`, `suite_tally.py --selftest`, `test_suite_cancellation.py`, and `ci_events.py --check` and `--selftest` (1821 items, 2530 arms). On the hosted rtl-full run 38262957309 at this exact head, the step "Prove specialized suite ownership" reached completed/success on all five Verilator workers (`receipts/hosted-rtl-full-38262957309-snapshot.txt`, 2026-10-12T14:30Z).

[R626] UNCLEAN Robustness - F1 is open (`receipts/serial-sweep-planted-suite.log`, `receipts/refresh-does-not-cure-new-suite.txt`, `receipts/base-vs-head-planted-suite.txt`). Beyond F1, the tree plantings fail closed as designed (`receipts/probe_727.txt`, `receipts/r626-1-mutate-at-61296ea1.out`):

| Planting | Result |
|---|---|
| Unmeasured suite | Refused |
| Removed suite | Refused |
| `gptp_plane` +500 s | Four workers over |
| `timeout-minutes` 116 | Refused |
| `timeout-minutes` 117 | PASS |
| Six workers | Refused |
| Missing `rtl.yml` | Refused |
| Duplicate job `timeout-minutes` | Refused |
| `timeout-minutes` as an expression | Refused |
| Step-level `timeout-minutes` | Ignored |

- A sharded selection of an unmeasured suite exits 2, naming the suite.
- `--measure` handles the cancelled #696 log correctly: it keeps the windows of suites that completed and gives no overhead (rc 0).
- Worker 1's 19 shared suites take 0.991x as long in the #696 run as in the dev run (`receipts/runner-variance.txt`).

[R626] PASS Tests - `scripts/suite_shards.py:411-693` at 61296ea1, `receipts/probe_727.txt`/`.json` (28 reviewer cases, 0 drift), `receipts/r626-1-mutate-at-61296ea1.out` (29 cases, rc 0), `receipts/gates_summary.txt`. Every assigned control is `[ok]` at the head and ESCAPED under its mutant:

| Mutant | Arm that reports ESCAPED |
|---|---|
| Missing duration made free | Both arms |
| Stale-entry check deleted | Stale arm |
| Timeout mirrored as 120 | 116-minute arm and the 36 s arm |
| `HEADROOM_PERCENT` 61, 75 or 100; bound +1; bound /10 | 36 s arm |
| `>=` at the bound | At-bound arm |
| Mean-only check | Three arms |
| Overhead dropped | +1 s arm |
| Zero duration allowed | Zero arm |
| Worker count mirrored | Six-worker arm |

The following mutants also fail the self-test: pins dropped, a pin moved, the dedicated set dropped, `--measure` timed from job start, `--measure` rounding down, and `--measure` accepting a TIMEOUT. The 36 s arm is independent of the formula it checks. The existing regressions pass: selector self-test on 3.12.13 and 3.14.7, `ci_events`, cancellation, tally, test-evidence and idiom gates, `git diff --check`. S1 and S2 are optional.

[R626] UNCLEAN Docs - F1 is open. Beyond F1:

- `CI_WORKFLOWS.md:183-211,322-328` and the docstring `:1-48` match the code: longest-first balancing to the least-loaded worker, the pins, the dedicated `milan_dp`, 60 % of `rtl.yml`'s `timeout-minutes`, the `maap` provenance, and the 104-minute and 120-minute history.
- The cited pages `RUNNING_TESTS.md:93`, `TESTING.md:515-521` and `milan_dp/README.md:442` stay accurate.
- No other doc cites hash ownership. R1 and R2 are RESIDUE.
- The doc gates exit 0 with the pinned renderer: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base c6bd08c6` (0 findings over 33 added lines) and `--selftest`, `check_doc_paths.py`.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Tables re-derived from both hosted runs (selector and independent parser); docstring refresh run verbatim; independent split; five lists, union and inventory; serial, physical and round-1 byte comparisons; `rtl.yml` unchanged | R626-2 | 61296ea1fbbb456bd9bc4d7ed93af37d0dfaf6d3 |
| RTL | CLEAN | Complete diff (two files); caller contracts in run_all_suites.sh, suite_tally.py, rtl.yml and test_suite_cancellation.py; integration gates; hosted ownership step at this head | R626-2 | 61296ea1fbbb456bd9bc4d7ed93af37d0dfaf6d3 |
| Robustness | UNCLEAN (F1) | 10 tree plantings; refusal exits; full serial sweep with a planted suite; refresh with a planted suite; cancelled-log measure; runner variance | R626-2 | 61296ea1fbbb456bd9bc4d7ed93af37d0dfaf6d3 |
| Tests | CLEAN (S1, S2 optional) | `--selftest` arms; 28 reviewer cases plus 29 R626-1 cases; hash-tie cross-process probe; selector, ci_events, tally, cancellation and test-evidence gates | R626-2 | 61296ea1fbbb456bd9bc4d7ed93af37d0dfaf6d3 |
| Docs | UNCLEAN (F1; R1 and R2 are RESIDUE) | CI_WORKFLOWS.md diff; selector docstring; TESTING.md and RUNNING_TESTS.md serial-sweep text; PR body; doc gates | R626-2 | 61296ea1fbbb456bd9bc4d7ed93af37d0dfaf6d3 |

## Real limits

- No manager source bank runs at this head, and none is claimed or inferred. The execution evidence here is the reviewer's own focused receipts. Source-head execution evidence is otherwise the executor's published gate record.
- **Not run:**
  - any Verilator suite, the full serial sweep to completion (only its preflight abort was exercised), `syn/yosys/run.sh`, act or `act_ci`, Vivado, and hardware;
  - the pinned Verilator 5.050, which no check here needed.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- Mutation and planting cases used minimal disposable trees under `scratch/`: the inventory directories with stub Makefiles, plus `rtl.yml` and the selector, which are the only inputs the self-test reads. The serial-sweep probe used a full copy of the clone.
- Three doc gates first exited 2 because the pinned renderer was absent. They were re-run with it installed into a disposable environment under `scratch/`; nothing shared was installed.
- Hosted state at 2026-10-12T14:30Z: rtl-full run 38262957309 at this head had `full-ci-gate` and the four Yosys shards at success, Physical gPTP skipped (not executed), and all five Verilator workers in progress. Round-1 run 38258772791 was cancelled, so it carries no acceptance-3 evidence.
- The table is one sample. The balanced workers have 115-117 s spare (2.7 %) against 72 min.
- Clone integrity after the probes:
  - 1295 tracked blobs match HEAD in bytes and mode, and the 1300 index entries equal the HEAD tree.
  - The gitlinks for verilog-axis `48ff7a7e`, protocol-processor `2ad2f845` and gptp-processor `7dda9c3b` match and are clean.
  - A `scripts/__pycache__/` created by this review's gate runs was removed, leaving no untracked or ignored files (`receipts/integrity.txt`).

## Pending manager duties

- **Acceptance 3.** Every Verilator worker of the PR's ready-state rtl-full run must take at most 4320 s. Record predicted against measured on the PR.
- **F1.** It needs a source and doc correction, or a published maintainer decision, followed by re-review. Any change to `scripts/suite_shards.py` un-covers every lens whose scope includes it.
- **Residue checklist.** Carry R1 (the `rtl.yml` comment, routed to #495) and R2 (the PR body line).
- **Decision on S1.** The executor has published it for a decision.
- **Merge turn.** The act replica, the current-dev merge candidate (builder and native banks, the serial sweep and Yosys), merge authorization, post-merge containment, and closing the issue.

R626-2 FINISHED
