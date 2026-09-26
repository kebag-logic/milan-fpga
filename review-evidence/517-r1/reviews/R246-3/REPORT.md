[R246] POSITIVE - exact head de4862cb74ba476f2dd10f095049c062fccfc920

# R246-3: composition acceptance, issue #517 / PR #524

- Role: cleared-context external reviewer, composition round R246-3.
- Candidate: `de4862cb74ba476f2dd10f095049c062fccfc920`, tree `05202d8256ac3cba5b04766301b3750b39d125f2`.
- Parents: `ccfed0e7d5cdd64687af30646536603bbb7ea236` (C_567: #567 pin `0922e434` on the #532 fix `7e4dcd0e` on live dev `7eb3b0d4`) and PR #524 source head `1d694677c8f376ec44e3b59b1d7fa7abccda106b` (rebased on `5c78ce2e`).
- Scope: composition acceptance only. The composed tree must add no defect beyond the reviewed source.
- Verdict basis: no BLOCKER, MAJOR or MINOR finding is open under any lens. One SUGGESTION (S1) is recorded. It is optional and affects no lens.

## 1. What the composition changes

Receipt: `receipts/composition-delta.txt`.

`git diff ccfed0e7..de4862cb` touches the same seven files as the source diff `5c78ce2e..1d694677`. The two diffs are identical line for line, apart from index and hunk headers, except one unchanged README context line. That line is the `obj_crflic` table row that #551 rewrote on dev.

`scripts/check_baremetal_only.py`, `sim_pool.py`, `test_sim_pool.py` and `test_sim_pool_backpressure.py` are byte-identical to the source-head blobs. Only `Makefile`, `README.md` and `docs/testing/TESTING.md` differ from the source blobs, because they are merges.

Files this PR changes that predecessors in the candidate also changed (`git log 5c78ce2e..ccfed0e7 -- <file>`):

| file | predecessor commits since the PR base | textual result | semantic check |
|---|---|---|---|
| `tb/verilator/milan_dp/Makefile` | #551 (`4eca4540`, merged by `220cb5a3`): `crflic_probes.vlt` added to `CRFLIC_BUILD`; `crflic-mutants` comment | clean; the PR hunk's context is unchanged. The delta `5c78ce2e..1d694677` equals the delta `ccfed0e7..de4862cb` | expanded recipe comparison, section 2 |
| `tb/verilator/milan_dp/README.md` | #551, #545/#563, #400/#403/#566, #567 (`1912c047`, `9143e21a`) | clean | section 5 |
| `docs/testing/TESTING.md` | #545/#563, #559/#564 | clean | section 5 |
| `scripts/check_baremetal_only.py` | none since `5c78ce2e` | the file equals the source blob | the #504 (PR #521, `4876423d`) and #523 (PR #526, `015edd9a`) changes are ancestors of `5c78ce2e`. The named text conflict was already resolved in the reviewed source rebase. `--check` and `--selftest` pass on the candidate, section 6 |

Predecessor changes to sources the pooled legs execute, also since `5c78ce2e`: `sim_nxn.cpp` (+96, #403 output-offset census), `sim_crf_licence.cpp` (+179, #551), `sim_main.cpp` (comments), `sw/builder/endstation_builder.py` (#400/#403; the `sim_nxn` legs invoke it), `hdl/milan/milan_datapath.sv` and other RTL, and the `protocol-processor` gitlink `0922e434`. No predecessor adds an ordinary simulation leg to `run`. Section 3 covers these changes.

## 2. Decisive question: pooled default inventory equals the composed sequential inventory

Receipts: `receipts/make-n-run.ccfed0e7.txt` and `receipts/make-n-run.de4862cb.txt`, from `make -n run VERILATOR_JOBS=8` with the pinned tool first on PATH.

- The two expansions are identical on lines 1-35. That covers the generators, the `gptp`, `gptp-lat` and `gmstep` prerequisites with the `gmstep` leg run, all 14 elaborations including #551's `crflic_probes.vlt` build, and the separator echo. They are also identical on the tail: `render_mutants.py`, then `gmstep_mutants.py`.
- The only difference is the ordinary-leg block. In `ccfed0e7` it is 11 bare executable lines plus `echo` banners. In the candidate it is one `exec python3 sim_pool.py --jobs="2"` line that carries the same 11 executables, in the same order, with the same banners and no arguments: `obj_dir`, `obj_notify`, `obj_crflic`, `obj_nxn`, `obj_nxndv`, `obj_nxn8`, `obj_nxn4c`, `obj_nolpf`, `obj_prune`, `obj_ax1x1`, `obj_aclk`.
- #551: `--unwarmed-refusal` is now unconditional inside `sim_crf_licence.cpp:1225`. The default leg correctly takes no argument in both recipes. It is pooled exactly once.
- #545: its slew controls in `gmstep_mutants.py` are `acceptance=False`. The default `python3 gmstep_mutants.py` after the pool still plants only the three #387 acceptance controls. `slew-mutants` belongs to `tb/verilator/mmcm_servo`, not to this recipe. No #545 leg belongs in the pool.
- #400/#403: no new leg. They extend the existing `sim_nxn` legs.
- Nothing was dropped or run twice. Each executable appears once on the runner line and nowhere else in the expansion.

## 3. Executed evidence on the candidate (pinned Verilator 5.050)

Tool identity: the configured wrapper path was absent on this host. I used a scoped wrapper under the packet scratch directory. It points at the same container overlay the manager's evidence records (`.../overlay/9517af57.../diff/usr`). `verilator --version` prints `Verilator 5.050 2026-07-01 rev v5.050`, and `verilator_bin` sha256 is `44898b22af4178b45214a0820a04eeac8632ae721ff005e69ef1cf69121bbfdd`. `VERILATOR_JOBS=8`, `TMPDIR` is under packet scratch, and runs are in the foreground.

A foreground call has a 10-minute limit, so the expanded default recipe ran as consecutive chunks of its own `make -n` lines (`run_chunk.sh`). The chunks are `A` (lines 1-8), `B` (9-15), `C` (16-21), `D` (22-28), `E` (29-35), `pool` (36-55), `render` (56-57) and `gmstepm` (58-59). Every chunk exited 0 (`receipts/timings.txt`, `receipts/chunk-*.log`, `receipts/pool-jobs2.log`).

| comparison | pooled `--jobs=2` (the default line as expanded) | sequential `--jobs=1` |
|---|---|---|
| exit | 0 | 0 (run as legs 1-9, then legs 10-11) |
| per-leg captures `obj_legs/NN-*.log` | 11 | 11; **all 11 byte-identical** to pooled |
| ordered transcript `obj_legs/replay.log` | 930,026 B | concatenation of the two parts **byte-identical** to pooled |
| `sim_pool:` lines on a passing run | 0 | 0 |
| full-suite `suite_tally.py` (all chunks) | 11206 checks, 0 failures, 16 tallies | 11206 checks, 0 failures, 16 tallies |
| `suite_tally.py --verdict` | 0 | 0 |
| wall time of the ordinary set (loaded shared host, load average 20-35 on 16 CPUs; context only) | 542.88 s | 620.02 s |

Per-leg check counts, identical in both modes: `obj_dir` 234, `obj_notify` 381, `obj_crflic` 415, `obj_nxn` 1844, `obj_nxndv` 1846, `obj_nxn8` 3524, `obj_nxn4c` 1844, `obj_nolpf` 234, `obj_prune` 33, `obj_ax1x1` 231, `obj_aclk` 190. All have 0 failures.

`render_mutants.py` passed with 6 checks, and the default `gmstep_mutants.py` passed with 4 checks. Receipts: `receipts/pool-jobs2-obj_legs/`, `receipts/seq-jobs1-part{1,2}-obj_legs/`, `receipts/tally/`.

`obj_aclk` dominates the ordinary set at about 440 s. It is the last leg in recipe order, so the pool cannot overlap it with a later leg. That is a property of the preserved order, not of the composition.

### Per-leg write sets (new or changed legs)

Receipt: `receipts/write-audit/`. `audit_writes.py` runs each leg under `strace -f --seccomp-bpf -y` on the creating, modifying and removing path syscalls. Relative names are resolved against their directory fd, or against the traced cwd.

Tool correction, recorded for transparency: my first parser accepted only a bare `AT_FDCWD`. Under `-y`, strace prints `AT_FDCWD</cwd>`, so that version missed `openat` creations. A positive control exposed this. The corrected tool detects all three planted writes (`receipts/write-audit/positive-control.txt`): two scripts writing one shared path, reported as shared, and a cwd-relative write into the suite directory, reported as outside scratch. Every leg was then re-traced. An independent `grep` over the raw traces also finds 0 successful write-class calls outside `milan_nxn_*` for every leg. The results below come from the corrected tool.

- `obj_notify`, `obj_nxn`, `obj_nxndv`, `obj_nxn8` and `obj_nxn4c` each write 18 paths, all inside their own `mkdtemp` `milan_nxn_XXXXXX` directory. That is the directory, `generator.log`, `image.bin`, `image.json`, `builder/`, `builder/<cfg>/`, `builder/<cfg>/gen/`, and 11 builder files including the private `gen/adp_shape_defaults.svh`. The #400/#403 builder change did not add a file or a path outside the scratch directory.
- `obj_dir`, `obj_crflic` (with #551's new arm), `obj_nolpf`, `obj_prune`, `obj_ax1x1` and `obj_aclk` write 0 paths.
- No leg writes a path outside its private scratch. **No exact path is written by two legs.** No `--exclusive` mark is needed, which matches the recipe.
- `.pyc` caches: no bytecode file is newer than the `gmstep` prerequisite's image. That prerequisite warms `sw/builder` and `avdecc` before the pool, so the concurrent legs write none.
- Each traced leg's output is byte-identical to its pooled capture.
- `MILAN_COUNTER_FRAME_OUT` is still read only at `sim_nxn.cpp:3640`. The predecessors added no other environment-selected output.

### Cancellation with composed legs

Receipt: `receipts/probe-cancel.txt`, script `probe_cancel.sh`. SIGTERM reached the pool 4 s after it started `obj_nxn` (while its builder child ran) and `obj_crflic`. Result: 0 survivors with the suite as cwd, both partial captures retained and attributed, and the unstarted `obj_notify` named. No composed leg installs a signal handler (`grep` over the five harnesses and `tb/common/verilator_harness.hpp`).

Blocked stdout with real composed legs: `receipts/probe-blocked-cancel-SIGTERM.txt` and `-SIGINT.txt`, script `probe_blocked_cancel.py`.

- Setup: the pool ran `obj_nxn` and `obj_aclk` with stdout on a pipe nobody reads. The signal was sent after `obj_nxn`'s 157 KB capture had been replayed to the transcript, so replay to the pipe was blocked while `obj_aclk` still ran.
- SIGTERM: the runner ended by the signal in 0.01 s, `obj_aclk` was reported killed, and 0 processes survived.
- SIGINT: the same result.

## 4. Tests on the candidate

- `test_sim_pool.py`: 17/17 pass. `test_sim_pool_backpressure.py`: 28/28 pass. `test_render_phase_observation.py`: 24/24 pass. Receipt: `receipts/gates.txt`.
- `test_sim_pool_backpressure.py` repeats (`receipts/repeat-backpressure.txt`, script `repeat_backpressure.sh`): 5 runs with SIGINT at its default and 5 with SIGINT inherited ignored. All 10 runs gave 28/28 and exit 0.
- Inventory-arm fault probes, restored byte-exact after each one (`receipts/probe-inventory.txt`):
  - dropping `obj_crflic` from the runner line FAILS the arm;
  - swapping `obj_nxn` and `obj_nxndv` FAILS it;
  - a default of `SIM_JOBS ?= 3` FAILS it;
  - running `obj_crflic` also as a bare line after the runner PASSES it (see S1);
  - adding a new bare leg after the runner PASSES it (see S1).
- `measure_test_evidence.py --check` and `--selftest` pass. Ratchet counts are identical at `ccfed0e7` and at the candidate: 75 suites without a mutation arm, 10 unseeded draw sites, 0 unexplained DUT-source readers, 3 wall-clock suites. `check_py_idiom`, `measure_fail_fast` and `check_hygiene` counts are identical too, apart from +3 scanned files (`receipts/ratchet-compare.txt`).

## 5. Documentation on the candidate

- `docs/testing/TESTING.md:293-310` lists the composed inventory exactly. That covers the eleven legs in recipe order, `SIM_JOBS=1`, the five `sim_nxn` writers with 11 builder files, frame-dump serialization, `gptp`/`gptp-lat`/`gmstep` before the pool, and the render-law and default GM-step controls after it. All of this matches sections 2 and 3.
- `tb/verilator/milan_dp/README.md:4` says "fourteen elaborations", and the expansion contains 14 `verilator` invocations.
- `README.md:15-62` lists the same pooled inventory and write sets.
- `README.md:76-79` keeps the #551 `obj_crflic` row from dev and adds a correct `obj_gptplat` row.
- The `render-csr-controls`, `gsi-mutants`, `notify`, `crflic-mutants` and `gmstep-mutants` targets named in the documentation exist.
- Predecessor documentation text says "the normal licence leg remains part of the default sweep" (#551) and "the sweep carries the three controls named by acceptance" (#545). Both stay true under the pool.
- The dated per-leg count table (`README.md:960-980`) is an explicitly historical record that this PR does not touch.
- `docs/testing/CI_WORKFLOWS.md` (changed by #545/#559) keeps the `milan_dp` 3600 s budget. The PR does not touch it, and the pool only shortens the suite.

## 6. Gates on the candidate

Receipts: `receipts/gates.txt`, `receipts/md-gates.txt`, `receipts/docs-check-no-git.txt`. All pass:

- `docs_check.py` in git mode: 0 findings over 166 md + 887 files.
- `docs_check.py` in no-git mode, on a `git archive` of the candidate: 0 findings. `check_feature_status` also passes in that mode.
- `check_em_dash.py --base ccfed0e7`: 0 findings over 70 added lines in 2 pages. `--selftest` passes.
- `gen_toc.py`: `--selftest`, `--verify-anchors` (176 fragments) and `--check` (108 pages).
- `check_doc_style`, `check_doc_paths`.
- `check_baremetal_only.py --check`: 0 findings over 885 files. `--selftest`: 700 arms.
- `measure_test_evidence` `--check`/`--selftest`, `check_py_idiom`, `check_hygiene --check`, `measure_fail_fast --check`, `measure_naming --check`, `check_todo_ownership`.
- `ci_events.py --check` (1655 items) and `--selftest` (2197 arms).
- `check_archive`, `check_solution_docs`, `DOC_MAP.gen.py --check`, `check_sweep_shape --self-test`, `check_feature_status`.

The renderer gates used an interpreter whose environment is named for, and carries, the pins in `tools/markdown/requirements.txt` (sha256 prefix `40cdefe08ebd`; `cmarkgfm==2025.10.22`, `html5lib==1.1`, and the rest). The default host interpreter lacks `html5lib`, and those gates refuse on it by design.

## 7. Findings

### S1 - SUGGESTION - Tests - `tb/verilator/milan_dp/test_sim_pool.py:858-894` - the inventory arm cannot see an ordinary leg outside the runner line

- Authority/evidence: `receipts/probe-inventory.txt`. With `obj_crflic` also run as a bare recipe line after `sim_pool.py` (a double run), or with a new bare leg added after it, `arm_the_makefile_hands_the_runner_the_recipes_ordinary_legs` passes. It pins only the runner line's words and the build/render ordering.
- Impact: none at this candidate. Section 2 shows directly that no executable runs outside the runner line. A later dev merge that adds an ordinary leg beside the pool, or re-adds a pooled one, would still pass this arm unnoticed.
- Optional outcome: assert that no executable line between the last build and `render_mutants.py` appears other than the runner. Alternatively, keep the manager's direct `make -n` comparison at each merge candidate. That comparison is listed under pending duties.
- Verification: the `crflic-also-sequential` and `new-leg-outside-pool` probes fail the arm.

No BLOCKER, MAJOR or MINOR finding.

## 8. Reviewer-owned ledger

| lens | result | examined artifacts (at `de4862cb`) | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #517 acceptance 1 and 4 against the composed tree: `receipts/make-n-run.*.txt` (identical 11-leg inventory, arguments and banners; the #551 argument-free crflic leg; the #545 default controls), `receipts/composition-delta.txt`, per-leg byte identity and `suite_tally` 11206/0 in both modes, full default recipe exit 0 | R246-3 | `de4862cb74ba476f2dd10f095049c062fccfc920` |
| RTL | CLEAN | the PR diff contains no RTL. In scope for the composition: the 14 elaborations of the composed RTL (#400/#403 `milan_datapath.sv`, pin `0922e434`) built and ran under pinned 5.050 (`receipts/chunk-A..E.log`); build recipes identical between `ccfed0e7` and the candidate; `print-srcs`/`print-pp-srcs`/`print-dp-vflags` untouched; runner bound fixed at 2 and independent of `-j` (inventory arm, `-j8` variant) | R246-3 | `de4862cb74ba476f2dd10f095049c062fccfc920` |
| Robustness | CLEAN | `receipts/write-audit/` (positive-controlled; disjoint write sets for all 11 composed legs, nothing outside private scratch, no shared path), `receipts/probe-cancel.txt` (SIGTERM with composed legs: 0 survivors, attributed partials, unstarted leg named), `receipts/probe-blocked-cancel-{SIGTERM,SIGINT}.txt` (blocked stdout: 0.01 s, 0 survivors), frame-dump variable read only at `sim_nxn.cpp:3640`, no leg signal handlers | R246-3 | `de4862cb74ba476f2dd10f095049c062fccfc920` |
| Tests | CLEAN (S1 is a SUGGESTION) | `test_sim_pool.py` 17/17, `test_sim_pool_backpressure.py` 28/28 plus 10 repeats under both SIGINT dispositions, `test_render_phase_observation.py` 24/24 (`receipts/gates.txt`, `receipts/repeat-backpressure.txt`), inventory-arm probes (`receipts/probe-inventory.txt`), ratchet counts equal to `ccfed0e7` (`receipts/ratchet-compare.txt`), pooled against sequential tallies (`receipts/tally/`) | R246-3 | `de4862cb74ba476f2dd10f095049c062fccfc920` |
| Docs | CLEAN | `docs/testing/TESTING.md:293-310`, `tb/verilator/milan_dp/README.md:4,15-62,76-79` against the executed inventory and write audit; predecessor sweep statements; `CI_WORKFLOWS.md` budget; `docs_check` in both modes, `check_em_dash --base ccfed0e7`, `gen_toc --check/--verify-anchors`, `check_doc_paths`, `check_doc_style` (`receipts/gates.txt`, `receipts/md-gates.txt`, `receipts/docs-check-no-git.txt`) | R246-3 | `de4862cb74ba476f2dd10f095049c062fccfc920` |

The composition touches the scope of every lens: shared files, legs changed by predecessors, and doc tables. So I applied every lens myself at this head, and none rests only on the source reviews. The source POSITIVE reviews at `1d694677` still cover the source-only content that the composition leaves byte-identical: `sim_pool.py`, both test files and `check_baremetal_only.py`. Section 11 names them.

## 9. Real limits

- The ordinary set and the full recipe ran as consecutive foreground chunks of the exact `make -n run` expansion, not as one `make run` process. The sequential mode ran as two `--jobs=1` invocations (legs 1-9, then 10-11). Their transcripts concatenate byte-identically to the pooled one. Make's own error propagation across chunks was not exercised; each chunk ran under `sh -e`.
- The configured pinned-tool path was absent. I used a wrapper to the same recorded overlay, with version and sha256 as stated in section 3. The host was shared and heavily loaded, so the timings are context, not a benchmark.
- The write audit traces path syscalls with `strace --seccomp-bpf`. It does not see writes through pre-opened descriptors that are not path-named. None is expected, since the legs read `/dev/null` and write stdout into the capture. Its first parser version had a defect, found by its positive control and corrected before any conclusion was drawn (section 3).
- Tracked-state integrity: before the runs and after all probes, the index hash, tracked-content hash, file modes (865 regular, 46 executable, 4 gitlinks), gitlinks and submodule worktrees are identical and clean (`receipts/integrity-after.txt`, `receipts/index-before.sha256`, `receipts/tracked-content-before.sha256`).
- Receipts have host-specific absolute paths replaced by `$PACKET`, `$CLONE`, `$TOOLS`, `$VALIDATION_STORAGE`, `$DATA` and `$WORKSPACE_HOME`. Raw `strace` files are kept in the packet but not listed for publication. `writes.json` and the leg outputs are listed.
- No hosted, act, full-parent, PP, gPTP, Yosys, builder or BDD bank ran, and no physical calibration or hardware ran. Field skips are not hardware proof.
- The candidate commit exists only locally; the checks API reports no such SHA.
- Hosted results at source head `1d694677` (draft):
  - succeeded: `rtl-fast`, `docs-check`, `docs-check-no-git`, `elaborate`, `verilator-lint`, `yosys-elaboration`, `bdd-conformance`, `wire-accountability`, `full-ci-gate`;
  - skipped, not executed: `verilator-suites`, `yosys-portability`, the Verilator and Yosys shard matrices, and physical gPTP.

## 10. Pending manager duties

- Build the final current-dev candidate at the merge turn. Repeat the `make -n run` comparison against that candidate's sequential parent: exactly the 11 legs, none outside the runner line (S1). Repeat the per-leg write audit if dev adds or changes a leg or the builder.
- Exact-head hosted `verilator-suites` and `yosys-portability` after the PR is marked ready. Also the trusted act replica, candidate-merge validation and post-merge containment.
- Publication, PR ready-state and issue state are the manager's.

## 11. Prior public review findings on this PR

I read these only after sections 1-10 (verdict, findings and ledger) were written. Sources: the PR #524 review comments, R245-1 through R245-4 and R246-1 and R246-2. The two source POSITIVE reviews are **R245-4** (internal, `[R245] POSITIVE - exact head 1d694677`, PR comment 5845511559) and **R246-2** (external, `[R246] POSITIVE - exact head 1d694677`, PR comment 5845676358).

| prior finding | severity / lenses | state at `de4862cb` | evidence at this head |
|---|---|---|---|
| R245-1 F1: stdout backpressure prevents INT/TERM cancellation from terminating and reaping simulations | MAJOR, all five | **Resolved** | `sim_pool.py` is byte-identical to `1d694677` (`receipts/composition-delta.txt`). With real composed legs and a blocked pipe, SIGTERM and SIGINT end the runner in 0.01 s with 0 survivors (`receipts/probe-blocked-cancel-*.txt`). `test_sim_pool_backpressure.py` passes 28/28 in 11 runs |
| R246-1 F1 (retained by R245-3 as its F1): the stated shared tracked-header write does not happen | MAJOR, Conformance/RTL/Docs | **Resolved** | the pool line has no `--exclusive` mark. The positive-controlled trace shows every `sim_nxn` leg writing only its private `mkdtemp` directory, including the private `gen/adp_shape_defaults.svh`, with the #400/#403 builder composed in. There are no repository writes and no shared path (`receipts/write-audit/`). `sim_nxn.cpp` still says the builder "touches nothing tracked". `README.md:24-32` and `TESTING.md:298-303` state that write set |
| R246-1 F2 (retained by R245-3 as its F2): the backpressure verdict depends on the inherited SIGINT disposition and on a torn-ledger read | MINOR, Tests | **Resolved** | the test file is byte-identical to `1d694677`. At this head it gave 10/10 repeats at 28/28: 5 with SIGINT at its default and 5 with SIGINT inherited ignored (`receipts/repeat-backpressure.txt`) |
| R245-3-D1: the runner contract states a ten-leg inventory, and the no-grace SIGKILL rationale omits the eleventh leg | MINOR, Docs | **Resolved** | `sim_pool.py:8` reads "used to run eleven of them", and `:48` reads "none of the eleven legs, including obj_crflic, handles a signal" |
| R246-1 S1 and R245-3-S3: the pool tests run in no workflow, sweep preflight or target | SUGGESTION | retained (optional) | still true at this head. It relates to S1 above: the inventory arm protects the handoff only when someone runs it, and it cannot see legs outside the runner line |
| R246-1 S2 and R245-3-S1/S2: surviving mutants (stdin, duplicate refusal, late interrupt, stale-capture removal); hard-coded `28`; the "outer command guard" docstring | SUGGESTION | retained (optional) | the source files are byte-identical; the composition does not change them |
| R246-1 S3 and R245-3-S5: `clean` does not remove `obj_legs/` | SUGGESTION | retained (optional) | the `clean` recipe still omits `obj_legs` |
| R246-1 S4: while stdout is blocked, no new leg starts | SUGGESTION | retained (optional) | unchanged. Cancellation during that state is verified above |
| R245-3-S4: `obj_aclk` (about 440-450 s) dominates the pool from its recipe position | SUGGESTION | retained (optional) | consistent with this candidate's timings (section 3) |
| R246-1 S5: `reap_adopted` needs `/proc/<pid>/task/<tid>/children`, and only subreaper support is checked before launch | SUGGESTION | retained (optional) | unchanged; not re-probed |
| R245-4-S1: the unit-arm ledger read races an appending leg (`test_sim_pool.py:555`) | SUGGESTION | retained (optional) | unchanged; 17/17 in this round's runs |

No prior BLOCKER, MAJOR or MINOR finding remains open at this head. None of the prior findings changes this round's verdict or ledger.

R246-3 FINISHED
