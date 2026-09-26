[R245] POSITIVE - exact head 1d694677c8f376ec44e3b59b1d7fa7abccda106b

# R245-4: internal independent delta review of issue #517 / PR #524

This is an internal, cleared-context delta review. It covers exact head `1d694677c8f376ec44e3b59b1d7fa7abccda106b` (tree `58032a796c39dc45e7691386030e48f1882eaed8`), one commit on `f36b40dd`, from the Round 5 executor.

- **What was reviewed:** the delta `f36b40dd..1d694677` in full, judged against the Round 5 assignment and decision (issue #517 comment 5843777653). That decision supersedes the shared-header decision 5780545051.
- **Earlier coverage:** R245-3 covered `f36b40dd` in full. Executable controls for the whole runner were re-run at this head.
- **Lenses:** all five were applied: Conformance, RTL, Robustness, Tests, Docs.
- **What this verdict is not:** it is a source verdict. It does not authorize a merge. It does not accept hosted, act or candidate evidence, which the manager owns.

## Summary

All three findings open at `f36b40dd` are **closed** at this head, and no finding of MINOR or higher is new:

- **R246-1 F1 / R245-3 retained F1 (MAJOR):** the stated shared tracked-header write does not occur. My own per-leg write probe includes positive controls. It confirms that the five `sim_nxn` legs write only disjoint private `milan_nxn_*` directories, that the other six legs write no data files, and that no leg writes the repository. All five `--exclusive` marks are gone. The exclusivity, overlap and inventory controls still reject their planted defects. The comment, runner contract, README and TESTING now state the measured write set.
- **R246-1 F2 / R245-3 retained F2 (MINOR):** the backpressure fixture now sets its own signal state, and it reads the ledger only while both writers are held. It passes 28/28 in 10 default, 10 inherited-ignored SIGINT and 5 all-ignored-and-blocked runs. The pre-fix fixture, and the head fixture with the fix removed, each fail 12/28 under an inherited ignore. The R245-1 runner fails 28/28.
- **R245-3-D1 (MINOR):** the runner contract says eleven legs. Its no-grace SIGKILL rationale names `obj_crflic`.

One new SUGGESTION is optional and does not affect coverage.

**Independence record.** I did the independent pass over the delta, the write probe, the mutants, the signal repeats, the A/B timing and the merge check before reading any prior public review finding on this PR. I then read R245-3 (5843776016) and R246-1 (5839627765) to dispose of their findings. I have not read any other reviewer's report for this round. I read no author material other than the public evidence tree `80f64016` and the public PR and issue text.

## Prior public findings: disposition at this head

| Finding | Disposition | Evidence at `1d694677` |
|---|---|---|
| **R246-1 F1 = R245-3 retained F1**, MAJOR (Conformance, RTL, Docs): the shared tracked-header write that justified the five-leg exclusive group does not happen | **CLOSED** | (a) `probe_writes.py` traces all eleven legs, built with pinned 5.050 (`model-hashes.txt`). Each `sim_nxn` leg writes exactly 14 files under its own `mkdtemp` directory. The six other legs write nothing. Repository writes: 0. Pairwise shared written paths: none (`probe/analysis-legs.json`). The tree timestamp audit over the legs shows no worktree change (`probe/tree-diff-legs*.txt`; see Limits for the `.git/modules` hard-link ctime noise). (b) Positive controls fire: a same-byte tracked rewrite and a real root-mode builder rewrite of `configs/generated/endstation_arty_4x4/gen/adp_shape_defaults.svh` are both caught by the trace and the timestamp audit. A planted pair of writers of one private path is reported as shared (`probe/results/pc*.json`, `probe/tree-diff-positive-controls.txt`, `probe/analysis-legs-with-pc.json`). (c) `Makefile:544-565` has no `--exclusive`. (d) `sim_nxn.cpp` is byte-identical to base `5c78ce2e`, so the "touches nothing tracked" comment at `:399-400` is restored. (e) Planted defects are still rejected: R1 no-exclusion, M1 one mark restored, M2 crflic dropped and M3 default of one worker are each killed by assertion; R2 no-independent-overlap by guard hang (`tests/mutants-*.jsonl`). |
| **R246-1 F2 = R245-3 retained F2**, MINOR (Tests): the backpressure verdict depends on the inherited SIGINT disposition and reads the ledger while it is being written | **CLOSED** | (a) `test_sim_pool_backpressure.py:191-200` sets INT/TERM/HUP to SIG_DFL with an empty mask before exec, mirroring `test_sim_pool.py:255-260`. (b) The only ledger read is `:205`. It happens after both held legs have announced; each writes its start record before announcing. At that point L1 and L2 are held, the descendant is held, no third leg can start, and the recipe prerequisites are inert and have finished. The PID is carried to `:228`. No read follows a release. (c) Repeats (`tests/bp-head-*.jsonl`): default 10/10, inherited-ignored SIGINT 10/10, INT/TERM/HUP ignored and blocked 5/5. Every run was 28/28 with exit 0. Unit 17/17, including 2/2 under ignored and blocked signals. (d) Load-bearing: T0, the `f36b40dd` fixture, and T1, the head fixture without `preexec_fn`, each give **16 PASS / 12 FAIL** under an inherited-ignored SIGINT. (e) Still failing: the R245-1 runner blob `761ec858` (28/28 FAIL), blocking stdout (24 FAIL), flags not restored (24 FAIL) and final drain waits (18 FAIL). Cause (a) was never reproduced on this host, so its closure rests on construction (b) plus clean repeats, not on a before/after flake count. |
| **R245-3-D1**, MINOR (Docs): the runner contract says ten legs | **CLOSED** | `sim_pool.py:8` says "eleven". `:48-49` reads "none of the eleven legs, including obj_crflic, handles a signal". Independent check: `sim_main.cpp`, `sim_nxn.cpp`, `sim_crf_licence.cpp`, `sim_prune.cpp`, `sim_aclk.cpp` and `tb/common/verilator_harness.hpp` contain no `signal(`, `sigaction`, `SIGTERM`, `SIGINT`, `SIGHUP`, `atexit`, `at_quick_exit`, `sigwait` or `signalfd`, at head or in the merged tree. The runner's executable AST is identical to `f36b40dd` once docstrings are removed (`runner-ast-compare.txt`). |
| R245-1 F1, MAJOR (all lenses): blocked replay prevents cancellation | Remains **CLOSED** | Runner code is unchanged (AST identical). The blob `761ec858` fails 28/28 against the head fixture. With the marks removed, a new cancellation probe runs two `sim_nxn` legs at once with live `endstation_builder.py` descendants. It passes for SIGTERM, SIGINT and SIGHUP: the runner ends by the signal, no marked process survives, both legs are attributed and `obj_nxn8` is named as unstarted (`cancel/*.json`). |
| R245-3 S1-S5; R246-1 S1-S5 (SUGGESTION) | Optional, routed to #495 by the decision | Unchanged by this delta. S4 (start `obj_aclk` first) is now the only scheduling lever left, as the timing below shows. |

## New findings

### R245-4-S1 - SUGGESTION - Tests - `tb/verilator/milan_dp/test_sim_pool.py:555` - unit-arm ledger read races an appending leg

- **Evidence:**
  - Inside the exclusivity arm's loop, `case.events("contention")` parses the whole ledger right after `release(f"I{k}")` and the next announcement.
  - The released leg is appending its `released` and `end` records at that moment. This is the read-while-append shape of R246-1 F2 cause (a), in the sibling file the delta did not touch.
  - Not reproduced: 48/48 consecutive unit runs passed, 12 in each of 4 parallel lanes (`tests/unit-repeat/`).
- **Impact:** at worst a `JSONDecodeError`. That fails closed and never passes a defect.
- **Suggested outcome:** under #495, read the contention events after `finish()`, or parse the ledger tolerantly.
- **Verification:** the repeat harness `bp_repeat.py` on `test_sim_pool.py`.

## Verification of the assignment items

1. **Write sets and exclusivity.**
   - **Setup:** eleven models built from the head's own `make -n run` lines with pinned Verilator 5.050 (`build_models.sh`, `build-*.log`, `model-hashes.txt`). The pre-pool Python steps of `run` (`gen_divergent_shape.py`, and gmstep-build's builder and image-generator lines) were replayed first, so the interpreter cache was in the state `run` leaves before the pool.
   - **Measurement:** all eleven legs ran under `probe_writes.py`, with a shared `TMPDIR`, eight at a time for the first batch and then three. Every leg exited 0.
   - **Per-leg written paths:**

     | Leg | Written paths |
     |---|---|
     | `obj_notify` | 14, all in `milan_nxn_JOn8gv/` |
     | `obj_nxn` | 14, all in `milan_nxn_uYn961/` |
     | `obj_nxndv` | 14, all in `milan_nxn_GrcuaO/` |
     | `obj_nxn8` | 14, all in `milan_nxn_JV2civ/` |
     | `obj_nxn4c` | 14, all in `milan_nxn_1CBaF9/` |
     | `obj_dir`, `obj_crflic`, `obj_nolpf`, `obj_prune`, `obj_ax1x1`, `obj_aclk` | 0 |

   - **The 14 files:** `generator.log`, `image.bin`, `image.json`, and eleven files under `builder/<config>/`, including `gen/adp_shape_defaults.svh`. Each directory is removed on success.
   - **Result:** no repository path and no shared path. This matches the author's table.
   - **Byte identity:** the eleven per-leg captures match the author's published after-captures byte for byte: ten by git blob id, and `nxn8` by the sha256 listed in their OMITTED file (`capture-compare.txt`).
2. **Documentation of the measured write set.**
   - `sim_nxn.cpp:399-400` is restored at base bytes.
   - The runner contract is at `sim_pool.py:8-16`.
   - The Makefile comment is at `Makefile:544-545`.
   - The README is at `README.md:24-32` and TESTING at `TESTING.md:294-300`.
   - Each states the measured set, "no repository writes", "the other six legs write no data files" and that frame-dump presence still serializes. My measurements confirm every statement.
   - No stale "ten legs" or tracked-header wording remains in the pool's documents.
   - The live PR body matches.
3. **Backpressure determinism and sensitivity.** See F2 above: 28/28 repeatedly under both dispositions, plus the stricter blocked mode. The ledger read is quiescent by construction. The `761ec858` runner and the backpressure mutants fail.
4. **Eleven legs, and `obj_crflic` in the no-grace rationale.** See D1 above.
5. **Wall clock and budget.**
   - The author's cold pooled pair is 1356.114 s with the marks and 1361.378 s without (+0.388%). Both runs give 10074 checks, 0 failures and 16 tallies.
   - My concurrent A/B of the pool phase alone uses the same binaries and host load, with the head runner in private mirrors (`pool_ab.sh`, `pool-ab/summary.txt`). Head without marks: **498.52 s**. The round-4 marks restored: **501.50 s**. Both exit 0 with byte-identical replay transcripts.
   - The phase is bound by `obj_aclk`: about 454 s alone, against 1 to 27 s for each other leg (`probe/results`). Removing the marks therefore neither gains nor loses measurably, which is consistent with the author's claim of no gain.
   - The pooled runtime code is unchanged from `f36b40dd`, so the pooled-versus-sequential gain measured there stands; it is not re-measured here. The cold full suite takes about 1361 s locally, against the unchanged 3600 s `milan_dp` budget (`scripts/run_all_suites.sh:245`). No `.budget` file, script or workflow changed in the delta.
6. **Merge.**
   - `git merge-tree` of dev `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a` with the head is clean: tree `46c29c5c6819dabc599fc27331043346cc9200f0`. The merge base is `5c78ce2e`. Live `refs/heads/dev` is still `7eb3b0d4`, and `refs/pull/524/head` is `1d694677` (`merge-check.txt`).
   - Dev touches `Makefile` (crflic `.vlt` only), README, TESTING and `sim_nxn.cpp`. The `sim_nxn.cpp` change adds a timestamp grading step with no file operation, and no signal handler.
   - In the materialized merged tree, `test_sim_pool.py` passes 17/17 and the backpressure controls pass 28/28 (`tests/merge-*.log`). The pool documentation sections are unchanged by the merge.

## Per-lens results (artifacts at `1d694677`)

```text
[R245] PASS Conformance - issue #517 comment 5843777653 items 1-3 against Makefile:544-565, sim_nxn.cpp:399-400, sim_pool.py:8-16,44-50, test_sim_pool_backpressure.py:191-228, probe/analysis-legs.json, pool-ab/summary.txt, merge-check.txt - no mark without a measured shared path; decision items met; acceptance 1/3 inventory and frame-dump arms 17/17; merge with dev 7eb3b0d4 clean
[R245] PASS RTL - Makefile:544-565 pool line (make -n inventory arm, M1/M2/M3 killed), sim_pool.py executable AST identical to f36b40dd (runner-ast-compare.txt), scheduling of unmarked legs within the two-child bound (unit arms, pool-ab), harness signal-handler scan incl. obj_crflic, model hashes - no scheduling, bound or module-contract change beyond the removed marks
[R245] PASS Robustness - cancel/SIGTERM.json, cancel/SIGINT.json, cancel/SIGHUP.json (two concurrent sim_nxn legs in live builders; exit by signal; no survivor; attribution), probe/results (concurrent private scratch in one TMPDIR; no collision), tests/bp-head-ign-all-blk.jsonl, frame-dump arms - the newly allowed concurrency is safe and cancellable
[R245] PASS Tests - tests/unit-head.log 17/17, tests/bp-head-*.jsonl (25 runs, 28/28 each), tests/mutants-a.jsonl, tests/mutants-b.jsonl (11 mutants: 10 assertion kills, 1 guard hang), T0/T1 prove the F2 fix is load-bearing, tests/unit-repeat 48/48 - each changed control can fail for its defect; S1 optional
[R245] PASS Docs - sim_pool.py:8-16,48-49, README.md:24-32, TESTING.md:294-300, Makefile:544-545, sim_nxn.cpp:399-400, live PR body, gates/summary.txt (docs_check, doc_style, em_dash 0/70 added lines, toc, anchors, doc_paths, py/cpp idiom, test_evidence, baremetal, phase 24/24, diff --check all exit 0) - statements match my measured write set
```

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Decision 5843777653 items 1-3; the delta against the frozen acceptance and the superseding decision; write probe; inventory arm; merge-tree with dev `7eb3b0d4` | R245-4 (delta and executable re-run), building on R245-3 for unchanged artifacts | `1d694677c8f376ec44e3b59b1d7fa7abccda106b` |
| RTL | CLEAN | `Makefile:544-565`, `sim_pool.py` (executable AST unchanged), leg harnesses and signal scan, pool A/B scheduling | R245-4 | `1d694677c8f376ec44e3b59b1d7fa7abccda106b` |
| Robustness | CLEAN | Concurrent sim_nxn cancellation for INT, TERM and HUP; shared-TMPDIR concurrency; signal-state variants; frame-dump arms | R245-4 | `1d694677c8f376ec44e3b59b1d7fa7abccda106b` |
| Tests | CLEAN (S1 optional) | `test_sim_pool.py`, `test_sim_pool_backpressure.py`, repeats, 11 mutants, merged-tree runs | R245-4 | `1d694677c8f376ec44e3b59b1d7fa7abccda106b` |
| Docs | CLEAN | `sim_pool.py` contract, README, TESTING, Makefile comment, `sim_nxn.cpp` comment, PR body, doc gates | R245-4 | `1d694677c8f376ec44e3b59b1d7fa7abccda106b` |

Coverage of artifacts that the delta did not touch comes from R245-3 at the ancestor `f36b40dd`. Those portions of R245-3 carried no open finding: its three findings were all in delta-touched artifacts, and all three are closed above. Every lens was re-applied at this head to every artifact in the delta.

## Limits

- **Verilator path.** The directed path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist. I used a scratch wrapper around the same 5.050 installation that the other manager pinned wrappers point to: `Verilator 5.050 2026-07-01 rev v5.050`, `verilator_bin` sha256 `44898b22…bfdd` (`verilator-identity.txt`).
- **Model builds.** I built only the eleven pooled models. gptp, gptp-lat, gmstep and the mutation campaigns were not run. Instead, the pre-pool Python steps were replayed to reproduce the interpreter-cache state that `run` gives the pool. No full suite, bank, sweep, act or hosted run was performed.
- **Write-probe scope.** The probe measures the frame-dump-absent configuration and the `run` recipe's pre-pool cache state. The trace covers write-capable file syscalls, not memory-mapped writes; no leg maps a file for writing.
- **`.git/modules` ctime noise.** Eighteen submodule pack and commit-graph files under `.git/modules` changed ctime, with mtime unchanged, during the leg window. Their link counts are 5 and 16, so they are inodes shared with other clones on the host. No leg trace references `.git`. This is external hard-link activity, not a leg write.
- **Timing.** The A/B is one concurrent pair on a shared host, for the pool phase only. Cold and warm full-suite, sequential and hosted timing at this head were not measured by me.
- **Hosted checks.** At this exact head (draft PR), the executed hosted checks are `rtl-fast`, `elaborate`, `verilator-lint`, `yosys-elaboration`, `docs-check`, `docs-check-no-git`, `bdd-conformance`, `wire-accountability`, `changes` and `full-ci-gate`, all successful. `verilator-suites`, `yosys-portability`, the shards and physical gPTP were **skipped**, not passed (`hosted-checks.txt`).
- **Hardware.** Physical calibration was NOT RUN. Field skips are not hardware proof.
- **Probe artifacts.** Probe artifacts were removed after use. The clone is at exact head: tree, index and 895 tracked blobs with their modes verified, no hidden index flags, clean status including ignored files, and gitlinks `gptp-processor` `e5dcea6e`, `protocol-processor` `990f9652` and `third_party/verilog-axis` `48ff7a7e` checked out and clean. `external` is uninitialized, as it was at the start (`integrity.txt`).

## Pending manager duties

- Publish this verdict and packet.
- Trusted act replica from a clean current-`dev` runner worktree.
- Exact-head hosted `verilator-suites` and `yosys-portability` after the PR is marked ready, with the hosted `milan_dp` dedicated-worker timing compared against the attributable baseline (acceptance 5).
- The current-dev merge candidate (source base `5c78ce2e`, live dev `7eb3b0d4`) and its validation.
- Second positive review (external lane).
- Maintainer-authorized merge.
- Post-merge containment.
- Route R245-4-S1, with the carried suggestions, to #495.

## Receipts

- **Scripts:** `build_models.sh`, `probe_writes.py`, `bp_repeat.py`, `mutate.py`, `pool_ab.sh`, `probe_cancel_concurrent_nxn.py`, `integrity.sh`.
- **Raw evidence:** `probe/`, `tests/`, `gates/`, `cancel/`, `pool-ab/`, `merge-check.txt`, `capture-compare.txt`, `hosted-checks.txt`, `runner-ast-compare.txt`, `integrity.txt`.
- **Large raw files:** listed by sha256 in `OMITTED.txt`.
- **Published set:** every published file is listed in `MANIFEST.sha256`.

R245-4 FINISHED
