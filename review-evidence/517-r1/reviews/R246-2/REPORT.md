[R246] POSITIVE - exact head 1d694677c8f376ec44e3b59b1d7fa7abccda106b

# R246-2: external independent re-review of issue #517 / PR #524 (round 5)

- **Head:** `1d694677c8f376ec44e3b59b1d7fa7abccda106b`, tree `58032a796c39dc45e7691386030e48f1882eaed8`.
- **Bases:** source base dev `5c78ce2e9d831e588e759b696ed549804327e4d8`; live dev `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`.
- **Scope:** delta review of `f36b40dd..1d694677`, one commit that changes 7 files (+49/-25). R246-1 covered `f36b40dd` in full. Where the delta touches a contract, I re-read the head in full: the Makefile `run` recipe, the `sim_pool.py` docstring, README, TESTING and both test files.
- **Authorities, read in this order:**
  1. AGENTS.md and CONTRIBUTING.md.
  2. docs/README.md.
  3. The #517 body and its settled scope.
  4. Decision 5843777653, which requires exclusivity only where a written path is measured as shared, restores "touches nothing tracked", requires a deterministic backpressure test, and states eleven legs.
  5. REQUIREMENTS REQ-VER-01/02/04 and CODE_QUALITY rule 8.
  6. The diff and history.
  7. The public author evidence at `80f64016` (`review-evidence/517-r1/author-r5/`, including HANDOFF.md) and the review-ready comment 5844820638.
- **Independence:** I wrote and timestamped my verdict and provisional ledger (`receipts/independent_pass_before_prior_findings.md`, 2026-09-26T10:52:59Z) before reading R245-3's findings. I did not read any other reviewer's report on this head.
- **Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open at this head. My R246-1 F1 and F2 are closed, and so is R245-3-D1. All five lenses are covered clean at `1d694677`.

## Prior public findings: disposition at 1d694677

| Prior finding | State | Evidence at this head |
|---|---|---|
| **R246-1 F1**, MAJOR (Conformance, RTL, Docs): the stated shared tracked-header write does not happen. R245-3 retained it as its F1. | **CLOSED** | (a) `sim_nxn.cpp` is byte-identical to base again: `git diff 5c78ce2e..1d694677 -- tb/verilator/milan_dp/sim_nxn.cpp` is empty, and `:399-400` reads "touches nothing tracked". (b) All five `--exclusive` marks are removed from the pool line (`Makefile:546-565`). The comment at `:544-545` states the measured result. (c) The runner docstring (`sim_pool.py:8-16`), `README.md:24-32` and `TESTING.md:294-300` state a write set that matches my own measurement (item 1 below). (d) `builder_premise_probe.py` rerun at head: all three configs take the private branch, and no tracked header is rewritten. Its positive control (the builder run from the repository root) advances the tracked header's mtime (`receipts/builder_premise_probe.json`, `receipts/builder_premise_positive_control.txt`). |
| **R246-1 F2**, MINOR (Tests): the backpressure verdict depended on the inherited SIGINT disposition and read the ledger while it was being written. R245-3 retained it as its F2. | **CLOSED** | (a) `test_sim_pool_backpressure.py:191-200` launches the runner with INT, TERM and HUP at their defaults and an empty mask. (b) The only ledger read (`:205`) happens after both writers have announced and while both are held. Every `start` record is appended before its announcement (`test_sim_pool.py:171-187`), and no other ledger writer can run at that point: legs 3 onward cannot start while both slots are held, and the descendant is held too. (c) The test passes 28/28 in 98 of 98 runs: 25 sequential and 24 at 4-way parallel, each with SIGINT default and with SIGINT inherited-ignored (`receipts/backpressure_repeat_*`). (d) Test mutant T1, which removes the new preconditions, brings back 12 failing controls under inherited-ignored and none under default (`receipts/test_mutant_T1.txt`), so the fix is what makes the test deterministic. (e) The R245-1 runner (blob `761ec858`) fails 6/6 runs: all 24 INT/TERM controls fail with "runner did not shut down while stdout stayed blocked" (`receipts/old-runner-vs-head/summary.txt`). Mutants M15, M16 and M17 are each killed by the backpressure test (`receipts/mutants/summary.tsv`). |
| **R245-3-D1**, MINOR (Docs): the runner contract says ten legs, and the no-grace rationale omits `obj_crflic`. | **CLOSED** | `sim_pool.py:8` says "eleven". `:48-49` reads "none of the eleven legs, including obj_crflic, handles a signal". I checked this at runtime: every one of the eleven built legs shows `SigCgt` `0000000100000000` while running, which is only the libc-internal real-time signal 33, with no handler for INT, TERM or HUP (`receipts/leg_signal_handlers.txt`). The masked context still passes `check_baremetal_only.py --check` (0 findings) and `--selftest` (700 arms). |
| **R245-1 F1**, MAJOR (all lenses): blocked replay prevented cancellation | **Still CLOSED** | The runtime code of `sim_pool.py` is unchanged since `f36b40dd`: the delta touches docstring lines only. The shipped backpressure controls pass at head, and the pre-fix runner still fails them (row above). |
| R246-1 S1-S5 and R245-3-S1 to S5 (suggestions) | Unchanged, optional | Assigned to #495 by decision 5843777653, and correctly not implemented in this round. R245-3-S4 (start `obj_aclk` first) is corroborated by my own measurement (S7 below). |

## Findings

No BLOCKER, MAJOR or MINOR finding is open.

### Suggestions (optional; they do not affect coverage)

- **S6 (Docs, Robustness): `sim_pool.py:13`, `README.md:28`, `TESTING.md:297`. The statement that no repository write happens holds because `gmstep-build` warms the interpreter caches first.**
  - `run` always executes the phony `gmstep-build` before the pool (`Makefile:352-354`). Its builder and image-generator calls populate the eight `__pycache__` entries that the sim_nxn generator calls import. My pooled-phase timestamp audit therefore shows no cache or repository change (`receipts/timestamp_audit_pool_phase.txt`).
  - A sim_nxn leg run by hand on a fresh checkout, or with stale caches, writes ignored `__pycache__/*.pyc` files in `avdecc/`, `sw/litex/platforms/` and `protocol-processor/hdl/aecp/desc/`. The interpreter writes each one to a temporary file and renames it atomically. The first pass of `receipts/builder_write_strace_merged.txt` shows this, and that pass is also the realistic positive control for my tracer.
  - The write is safe under concurrency and never happens inside the pooled phase. A one-clause qualifier ("after `run`'s prerequisites") would make the sentence exact.
- **S7 (RTL scheduling): corroborates R245-3-S4.** `obj_aclk` runs about 465 s. The other ten legs take about 97 s together (`receipts/leg_durations_from_probe.txt`). The pool is therefore bounded by `obj_aclk`, which starts last in recipe order. This also explains why removing the marks gained nothing. Starting it first, with replay order unchanged, is the remaining lever (about 40 s). This is for #495 or a new Issue, not this lane.

## Assignment verification items

### 1. Per-leg write sets (my own probe and positive controls)

**Method.**
- `scripts/write_probe.py` runs each of the eleven built legs at head, from the suite directory, under `strace -f -y`. The trace covers every path-creating, write-opening, rename, unlink, mkdir and utime syscall, including those of the `sh`, builder and image-generator descendants.
- All five sim_nxn legs share one `TMPDIR`, which reproduces the real overlap condition. The frame-dump variable is absent.
- Around each batch I took a snapshot of every file and directory's mtime, ctime, size and inode across the tree and `TMPDIR` (`scripts/snap.py`).
- Each probed leg's output is byte-identical to its pooled capture (`receipts/write_probe_outputs_vs_capture.txt`), so every leg ran to completion.

**Result** (`receipts/write_probe_legs.{txt,json}`, raw traces in `receipts/write-probe-raw/`):
- `obj_notify` (config 1x1_tdm8), `obj_nxn` (arty_4x4), `obj_nxndv` (arty_4x4), `obj_nxn8` (8x8) and `obj_nxn4c` (arty_4x4) each create one distinct `milan_nxn_XXXXXX` directory.
- Each writes exactly 14 files there: `generator.log`, `image.bin`, `image.json`, and 11 files under `builder/<cfg>/`: `adp_shape_defaults.svh`, `aecp_aem_rom.svh`, `aem_overlay.json`, `build_plan.md`, `gen/adp_shape_defaults.svh`, `gptp_ucode.hex`, `lwsrp_csr_defaults.svh`, `lwsrp_table.json`, `lwsrp_table.svh`, `platform_shape.json` and `soc_params.json`. Each then removes the directory.
- `obj_dir`, `obj_crflic`, `obj_nolpf`, `obj_prune`, `obj_ax1x1` and `obj_aclk` perform no write, create or remove operation at all.
- **Shared written paths between any two legs: none.** No write lands outside the private directories, and no leg calls `chdir`.
- Both timestamp audits show only the shared `TMPDIR` directory entry changing (`receipts/timestamp_audit_probe_legs.txt`).
- This agrees row for row with the author's HANDOFF table, including each leg's config.

**Real pooled phase** (`receipts/timestamp_audit_pool_phase.txt`): across the whole tree and `TMPDIR`, the only changes are the runner's own `obj_legs/` captures, the suite directory entry that holds them, and the `TMPDIR` directory entry. No tracked, ignored or cache file changed. My sampler saw 2 sim_nxn legs alive at once, which confirms they now overlap.

**Positive controls:**
- `scripts/planted_writer.sh` runs as two "legs". Through a grandchild, each touches a tracked header, writes a shared ignored file, and creates and removes a `milan_nxn_*` directory.
- The tracer reports both repository writes and flags the shared path between the two legs (`receipts/write_probe_positive_control.json`).
- The timestamp audit reports the changed tracked header, the new file and the `TMPDIR` change (`receipts/timestamp_audit_positive_control.txt`).
- Two further controls: the repository-root builder run advances the tracked header's mtime (item F1(d) above), and the cold-cache trace records the `__pycache__` writes (S6).

**Merged candidate:**
- A disposable merge of the head with live dev `7eb3b0d4` (tree `46c29c5c`, dev gitlinks, including `gptp-processor` 5dce647a) runs the exact sim_nxn generator commands for all three configs with warm caches. Each writes the same 14 private files and nothing outside them (`receipts/builder_write_strace_merged.txt`, pass 2).
- Dev's `endstation_builder.py` changes do not alter the write set.

**Controls still reject their planted defects** (`receipts/mutants/summary.tsv`, run against the head tests):

| Mutant | Planted defect | Rejected by |
|---|---|---|
| M03 | exclusion removed | `arm_shared_group_is_exclusive_ordered_and_allows_independent_overlap` ("shared-state contention between grouped writers"), plus the skipped-group arm |
| M04 | group order reversed | the exclusivity, skipped-group and frame-dump arms |
| M28 | a leg dropped | the Makefile inventory arm |
| M29 | `--exclusive` re-planted on notify | the Makefile inventory arm |
| M34 | `--exclusive` re-planted on nxn4c | the Makefile inventory arm |
| M32 | crflic marked exclusive | the Makefile inventory arm |

At head, `test_sim_pool.py` passes 17/17.

### 2. Documentation states the measured write set

- `sim_nxn.cpp:399-400` is the base comment, byte for byte.
- `sim_pool.py:8-16`, `README.md:24-32`, `TESTING.md:294-300` and the Makefile comment each state what I measured: 14 private files in a unique directory, six legs with no data files, no repository write, disjoint sets and no marks. The one nuance is S6.
- The README's pre-existing text at `:9-12` about `TMPDIR` and a failed generator keeping its directory is still accurate.

### 3. Backpressure determinism

This item is covered by the F2 row above: 98 of 98 runs pass 28/28 under both dispositions; the R245-1 runner fails 6/6 runs; M15, M16 and M17 are killed; and T1 shows the fix is causal.

Test mutant T2 puts back the pre-fix ledger read after release. It did not reproduce the torn read (0 failures in 24 runs at 4-way parallel; `receipts/test_mutant_T2.txt`). The race was timing-dependent at `f36b40dd` (3 failures in 20 runs), so T2 is not evidence either way. Closure of cause (a) rests on the ordering argument above, which the code states at `:203-204`.

### 4. Eleven legs and the SIGKILL rationale

See the R245-3-D1 row.

### 5. Wall clock

My own cold pooled run at head used a fresh copy with no build products, pinned Verilator 5.050 (wrapper sha256 `905795b9...`, `--version` 5.050; `receipts/verilator_identity.txt`), 8 CPUs and `VERILATOR_JOBS=8` (`receipts/real-cold-pooled/`, `receipts/wallclock_summary.txt`):

| Phase | Seconds |
|---|---:|
| gptp | 101.087 |
| gptp-lat | 101.456 |
| gmstep | 37.942 |
| 14 builds + banners | 163.241 |
| ordinary pool, `--jobs=2` | 544.588 |
| `render_mutants.py` | 352.161 |
| `gmstep_mutants.py` | 139.706 |
| **Total** | **1440.181** |

- Against the unchanged 3600 s budget, the margin is 2159.8 s.
- All segments exit 0. The run produced 10074 checks, 0 failures and 16 tallies, and `suite_tally.py --verdict` exits 0.
- All eleven captures and `replay.log` are byte-identical to my R246-1 run at `f36b40dd` and to the author's after-captures. For `06-Vmilan_dp_nxn8.log` and `replay.log`, the comparison is by the sha256 in `author-r5/OMITTED.txt`.
- The host's 1-minute load average was 28-35 during the pool line, against 8-19 for R246-1's 491.6 s. These single shared-host samples do not support a speed comparison, and I claim none.
- The author's "no gain" result (1356.114 s to 1361.378 s, +0.388%) is consistent with the measured leg durations (S7): the pool is bounded by `obj_aclk`, so letting sim_nxn legs overlap cannot shorten it.
- The PR's overall gain over sequential execution was measured in R246-1 (58.8 s, 4.11%) and is not reduced by this commit.

### 6. Merge with live dev 7eb3b0d4

- `git merge-tree --write-tree 7eb3b0d4 1d694677` is clean, giving tree `46c29c5c6819dabc599fc27331043346cc9200f0`. `TESTING.md`, the Makefile and README.md auto-merge. Dev's own Makefile change adds `crflic_probes.vlt` to the crflic build, and dev's `sim_nxn.cpp` adds `#403` checks without new file writes.
- On a disposable merge checkout of that tree, with dev's gitlinks:
  - `test_sim_pool.py` passes 17/17 and `test_sim_pool_backpressure.py` passes 28/28 (`receipts/merged_tree_pool_tests.txt`).
  - The `make -n run` inventory compared with live dev: 14 legs in identical order, identical banners, builds and post-drivers, the identical interleaved sequence with pool markers removed, `SIM_JOBS=1` differing only in `--jobs`, and no exclusive legs (`receipts/inventory_livedev_vs_merged.txt`).
- This is not the manager's candidate validation.

## Gates at head

All gates below were run in a disposable copy of the exact head (`receipts/gates_rc.txt`, `receipts/gate_*.log`), and all exit 0:

| Gate | Result |
|---|---|
| `check_baremetal_only.py --check` | 0 findings across 869 files |
| `check_baremetal_only.py --selftest` | 700 arms |
| `ci_events.py --check` | 1647 items |
| `ci_events.py --selftest` | pass |
| `docs_check.py` | 0 findings |
| `check_em_dash.py --base 5c78ce2e` | 0 findings over 70 added lines; pinned renderer |
| `gen_toc.py --check` and `--verify-anchors` | pass |
| `check_hygiene.py --check` | pass |
| `check_py_idiom.py` | pass |
| `check_todo_ownership.py` | pass |
| `measure_test_evidence.py --check` | pass |
| `measure_fail_fast.py --check` | pass |
| `git diff --check 5c78ce2e HEAD` | clean |

Base-versus-head inventory: identical 14-leg sequence, and no exclusive legs (`receipts/inventory_base_vs_head.txt`).

## Per-lens results (artifacts at 1d694677)

- `[R246] PASS Conformance - #517 acceptance 1-4, settled scope, decision 5843777653 items 1-3; Makefile:544-565; receipts/write_probe_legs.json, timestamp_audit_pool_phase.txt, inventory_base_vs_head.txt, real-cold-pooled/tally.txt - exclusivity kept only where a measured written path is shared (none), accurate base comment restored, deterministic test, eleven legs stated; the inventory is identical with every leg run once; the real suite gives 10074/0/16 and its verdict exits 0.`
- `[R246] PASS RTL - Makefile:540-567 pool line and builds; sim_pool.py (runtime unchanged since f36b40dd, docstring only); diff scope (no hdl/, firmware, pin, gitlink or workflow change); receipts/real-cold-pooled/segments.jsonl concurrency; leg_durations_from_probe.txt - the scheduling constraint now rests on measured writes; the two-child bound holds; sim_nxn legs overlap as intended; the shared-state analysis is correct (S7 optional).`
- `[R246] PASS Robustness - five sim_nxn legs overlapping in one TMPDIR (distinct mkdtemp dirs, receipts/write_probe_legs.json); captures byte-identical under overlap; README:9-12 failed-generator path unchanged; 98 blocked-stdout cancellation runs under both SIGINT dispositions; frame-dump serialization arm and M04 - no new shared mutable state, no regression in failure or cancellation paths (S6 optional).`
- `[R246] PASS Tests - test_sim_pool.py:858-896 inventory arm, test_sim_pool_backpressure.py:144-233; receipts/backpressure_repeat_*, test_mutant_T1.txt, old-runner-vs-head/, mutants/summary.tsv (M03, M04, M15, M16, M17, M28, M29, M32, M34 all killed) - deterministic under both inherited dispositions; the fix is causal (T1); every planted defect is rejected by the intended arm.`
- `[R246] PASS Docs - sim_nxn.cpp:399-400 (identical to base), sim_pool.py:4-60, README.md:1-58, TESTING.md:289-303, Makefile:544-545; gate_docs_check_git.log, gate_em_dash_base.log, gate_gen_toc_*.log - the text states the measured write set, eleven legs and obj_crflic, and every claim was checked against receipts (S6 optional).`

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #517 body, settled scope and decision 5843777653; `Makefile:540-567`; `sim_nxn.cpp:399-400`; per-leg write-set receipts; inventory base/head and live-dev/merged; cold run tally | R246-2 | 1d694677c8f376ec44e3b59b1d7fa7abccda106b |
| RTL | CLEAN | `sim_pool.py` (delta docstring-only; R246-1 covered its runtime at f36b40dd, which this commit does not change); pool line and builds; concurrency samples; leg durations; diff scope with no HDL | R246-2 | 1d694677c8f376ec44e3b59b1d7fa7abccda106b |
| Robustness | CLEAN | overlapping sim_nxn write sets; captures under overlap; cancellation repeats under both dispositions; signal-handler census of the eleven legs | R246-2 | 1d694677c8f376ec44e3b59b1d7fa7abccda106b |
| Tests | CLEAN | `test_sim_pool.py` (17/17), `test_sim_pool_backpressure.py` (98 runs of 28/28); T1/T2; R245-1 runner; mutants M03, M04, M15-M17, M28, M29, M32, M34 | R246-2 | 1d694677c8f376ec44e3b59b1d7fa7abccda106b |
| Docs | CLEAN | `sim_nxn.cpp:399-400`, `sim_pool.py:4-60`, `README.md:1-58`, `TESTING.md:289-303`, Makefile comment; documentation gates | R246-2 | 1d694677c8f376ec44e3b59b1d7fa7abccda106b |

## Real limits

- As the assignment requires, I did not run the full parent, PP, gPTP, Yosys or builder banks, Docker/act, or the host `act_ci`. The 55-suite sweep figures (2121993 checks, 0 failures, 4 declared `tsn_fuzz` skips) are the author's and manager's published evidence, which I inspected but did not re-execute.
- The timing is one cold sample on a heavily loaded shared host (load average 28-35 during the pool). I made no sequential or warm rerun at this head. The sequential comparison is R246-1's, at `f36b40dd`. Per-leg durations are upper bounds taken from probe-output mtimes during parallel batches.
- The write probe ran each leg outside the runner. The pooled phase itself was audited by timestamps and directory mtimes only, which catch transient creates and deletes through the parent directory's mtime but do not name them. On the merged tree I traced the generator commands, not the full legs, because no models were built there.
- Test mutant T2 did not reproduce the original race; see item 3.
- Hosted checks at the exact head (`receipts/hosted_checks_exact_head.txt`; the PR is a draft and GitHub reports it MERGEABLE):
  - Executed with success: `rtl-fast`, `changes`, `full-ci-gate`, `docs-check`, `docs-check-no-git`, `bdd-conformance`, `elaborate`, `yosys-elaboration`, `verilator-lint`, `wire-accountability`.
  - Skipped: `verilator-suites`, `yosys-portability`, the Verilator and Yosys shards, and Physical gPTP. Skipped contexts are not evidence.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- The manager-named Verilator wrapper path does not exist on this host. I used a byte-identical copy of the same wrapper (the 55 copies on the host share its sha256) and verified its version.

## Integrity

- Every probe ran in disposable copies under the packet's `scratch/`: a full copy of the clone at head, and a scratch-local clone merged with live dev.
- The reviewed clone passes `scripts/integrity.py`: 899 tracked entries by bytes, kind and mode; the stage-0 index is equal to the tree; no hidden flags. Its index listing is unchanged, and `git status --porcelain --ignored` is empty (`receipts/integrity_before.txt`, `receipts/integrity_after.txt`).
- The gitlinks match: `gptp-processor` e5dcea6e, `protocol-processor` 990f9652 and `third_party/verilog-axis` 48ff7a7e are clean, and `external` is uninitialised, as found.
- In the clone, only git object and ref state changed: `git fetch origin dev` updated `origin/dev` and `FETCH_HEAD`, and `git merge-tree` added unreferenced objects. No tracked byte, index or `HEAD` changed.
- No probe process remains.
- Receipts are normalized to `$PACKET`, `$CLONE`, `$TREE`, `$MANAGER_TMP` and `$HOME`. Environment mappings echoed by one failing mutant assertion are redacted.

## Pending manager duties

- Publish this verdict.
- Trusted act replica.
- Ready-state exact-head hosted `verilator-suites` and `yosys-portability`, plus the dedicated-worker timing comparison.
- Full source banks at this head (recorded as passed in the manager's public evidence).
- Current-dev candidate build and validation on base `5c78ce2e` against live dev `7eb3b0d4`: this round's merge probe is not that.
- The second independent positive review, per CONTRIBUTING.
- Authorized merge and post-merge containment.
- Route S6 and S7 with the existing suggestions to #495.

R246-2 FINISHED
