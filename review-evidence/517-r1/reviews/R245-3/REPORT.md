[R245] NEGATIVE - exact head f36b40ddb5bf7fa5b12bba47d136e0b9d429403c

Round R245-3: internal, cleared-context, independent review of issue #517 / PR #524 at exact head `f36b40ddb5bf7fa5b12bba47d136e0b9d429403c`, tree `270b9c97701047659ff1ec6040126af77b7141e1`. The whole PR `5c78ce2e9d831e588e759b696ed549804327e4d8..f36b40dd` was reviewed (commits `cce997f6`, `9ceec519`, `c0b1dd5d`, `f36b40dd`). All five lenses were applied. This is a source verdict, not a merge authorization.

## Summary

The runner's scheduling, bounds, failure handling, cancellation and output replay are correct, and they behave as claimed on real Verilated legs. Leg inventory, policy-mask union and merge with live dev all check out. **R245-1 F1 is closed.**

The verdict is NEGATIVE for three open findings:

- **R246-1 F1 (MAJOR; Conformance, RTL, Docs), retained and independently verified.** The "shared tracked-header write" that the exclusive group and four documentation sites rely on does not happen when `sim_nxn` invokes the builder.
- **R246-1 F2 (MINOR; Tests), retained.** The backpressure controls' verdict depends on the caller's inherited SIGINT disposition. I reproduced this deterministically.
- **R245-3-D1 (MINOR; Docs), new.** The runner's contract still describes ten legs, including in its rationale for killing without a grace period.

Robustness is covered clean. Five SUGGESTIONs are optional.

**Independence record.** I wrote my own verdict and five-lens ledger (`REPORT.md` mtime 2026-09-26 07:59:29 +0200) before reading any other reviewer's report. That version is preserved unmodified as `receipts/report_before_reading_R246.md` (sha256 `dc820a22678338b7296177021b7e8c13d3aab02ec0bfe1d6feac6e549a2ec87d`). It was already NEGATIVE, with D1 open and Conformance, RTL, Robustness and Tests clean. My independent pass had accepted the decision's tracked-header premise from reading the code, and my benchmarks compared header bytes only. It missed R246-1 F1 and F2.

After reading R246-1, I verified both findings with my own probes and retained them. The ledger below is my current position. Only Conformance, RTL and Tests changed from the preserved version, and each change is supported by evidence produced in this round.

## Findings

### R246-1 F1 (retained) - MAJOR - Conformance, RTL, Docs - the stated shared tracked-header write does not occur

- **Artifacts:** `tb/verilator/milan_dp/sim_nxn.cpp:399-400`, `tb/verilator/milan_dp/sim_pool.py:9-12`, `tb/verilator/milan_dp/README.md:24-26`, `docs/testing/TESTING.md:294`, and the five `--exclusive` marks in `tb/verilator/milan_dp/Makefile:544-563`.
- **Authority/evidence:**
  - The shared-header decision (issue comment 5780545051) rests on the audit in 5780232053, which reads "`_write_shape_copies` unconditionally writes `configs/generated/<name>/gen/adp_shape_defaults.svh`".
  - `sim_nxn.cpp:405-410` runs the builder from `tb/verilator/milan_dp` with `../../../configs/<cfg>.yaml`.
  - `_repo_relative` (`sw/builder/endstation_builder.py:73-92`) forms `Path.cwd() / path` without normalising `..`. It returns `tb/verilator/milan_dp/../../../configs/<cfg>.yaml`, whose first part is `tb`. The tracked branch `source_parts[0] == "configs"` (`:5667-5669`) is therefore not taken, and the header is written under the private `-o` directory.
- **Reviewer probe:** `scripts/probe_builder_writes.sh` (`receipts/builder-writes/`). It runs the exact `sim_nxn` argv for all three `sim_nxn` configs (`endstation_arty_4x4`, `endstation_ax7101_8x8`, `endstation_ax7101_1x1_tdm8`) and audits the whole tree by timestamp.
  - Every config: exit 0, **no file written anywhere in the tree**, tracked header sha256 and mtime unchanged, private header present.
  - Positive control: the same builder run from the repository root with `configs/endstation_arty_4x4.yaml` rewrites `configs/generated/endstation_arty_4x4/gen/adp_shape_defaults.svh`. The probe therefore detects a real write.
- **Real-run corroboration:** my pooled cold, sequential warm and pooled warm full runs, four real cancellation probes and the frame-dump probe each ran the five `sim_nxn` legs. Afterwards every tracked generated header still carries the checkout's 06:32:26 mtime (`receipts/runA_tracked_header_mtimes_after_all_runs.txt`). Every "headers unchanged" receipt so far, including mine, compared bytes only and could not distinguish a same-byte write from no write.
- **Impact:**
  - The PR replaces a correct base comment ("touches nothing tracked") with an incorrect one, and asserts a non-existent side effect in the runner contract, README and TESTING.
  - The exclusive group, which serialises the five `sim_nxn` legs, rests on a shared-state analysis that executable evidence contradicts.
  - Serialisation is safe, but its stated reason is false, and it constrains the measured gain.
  - The frozen scope's factual premise now conflicts with the implementation's measured behaviour. AGENTS section 2 requires publishing such a conflict for a decision, not resolving it privately. CONTRIBUTING section 3: "Measure, don't assume".
- **Required outcome:**
  - The conflict is published on #517 and decided by the maintainer.
  - The code comment, runner docstring, README and TESTING state the measured write set.
  - If the group is kept, it is described as a conservative choice, not as protection against a tracked-header write.
- **Verification:**
  - Re-run `scripts/probe_builder_writes.sh`, including its positive control, and compare the wording against it.
  - If scheduling changes, the exclusivity, overlap and inventory controls still reject their planted defects.

### R246-1 F2 (retained) - MINOR - Tests - `tb/verilator/milan_dp/test_sim_pool_backpressure.py:190-193` (and `:148`, `:218`) - verdict depends on the invoking environment

- **Authority:** `docs/development/CODE_QUALITY.md:1625-1627` (rule 8: "a deterministic, self-checking test").
- **Reviewer reproduction, cause (b):**
  - The control starts the runner without normalising signal dispositions. Its sibling `test_sim_pool.py:256-260` does normalise them.
  - Run under `trap "" INT` (SIGINT inherited ignored, which is the state `cmd &` gets in any non-interactive shell), the unmodified head test reports **16 PASS, 12 FAIL**. All 12 are SIGINT controls failing with "runner did not shut down while stdout stayed blocked" (`receipts/backpressure_sigint_inherited_ignored.txt`).
  - With the default disposition it passes 28/28 (`receipts/test_sim_pool_backpressure_head.txt`).
  - The runner is right to keep an inherited ignore (`sim_pool.py:452`), so the fault is in the test's precondition.
- **Cause (a), not reproduced here:** a torn-ledger read race in the `child-exit` controls. `:148` parses the whole ledger right after `:218` releases a leg that is appending. I saw 20/20 passes in 20 consecutive runs (`receipts/backpressure_repeat20.txt`). The race is plausible by construction, because multi-page appends extend the file size page by page, but it is not reviewer-reproduced.
- **Impact:** the recorded 28/28 result depends on how the test is invoked. It fails closed, never open, but it is not reproducible evidence.
- **Required outcome:** the control establishes its own signal preconditions. It also reads the ledger only once the writer is quiescent, or parses it tolerantly.
- **Verification:** 28/28 with SIGINT default and with SIGINT inherited ignored, repeated. The R245-1 runner (blob `761ec858`) and the backpressure mutants still fail.

### R245-3-D1 - MINOR - Docs - `tb/verilator/milan_dp/sim_pool.py:8`, `:44` - runner contract states a ten-leg inventory; the no-grace SIGKILL rationale does not cover the eleventh leg

- **Authority/evidence:**
  - AGENTS section 6 `Docs`: changed contracts are reflected in authoritative docs.
  - The rebase (issue comment 5835674224) put all **eleven** legs in the pool (`Makefile:544-563`). `README.md:15`, `TESTING.md:289` and `test_sim_pool.py:37,859` say eleven.
  - The runner contract still says `used to run ten of them` (`:8`). It justifies SIGKILL without a grace period by `none of the ten legs handles a signal` (`:44`).
  - `obj_crflic` (`sim_crf_licence.cpp`, #530) entered the pool at the rebase. The reconciliation commit left the runner byte-identical.
- **Independent check:** no pooled harness (`sim_main.cpp`, `sim_nxn.cpp`, `sim_crf_licence.cpp`, `sim_prune.cpp`, `sim_aclk.cpp`, `tb/common/verilator_harness.hpp`) contains `signal(`, `sigaction`, `SIGTERM`, `SIGINT`, `atexit` or `at_quick_exit`. Behaviour is correct, and the defect is documentary.
- **Impact:** the authoritative contract misstates the inventory it enforces. Its safety premise for an uncatchable kill does not name one of the legs it now applies to.
- **Required outcome:** the docstring states the current inventory, or no count. Its no-handler premise covers every pooled leg, including `obj_crflic`.
- **Verification:** read the docstring against `Makefile:544-563`. `test_sim_pool.py` stays 17/17. `check_baremetal_only.py --check` and `--selftest` pass, with the masked context at `sim_pool.py:35` kept byte-identical.

### Suggestions (optional; do not affect coverage)

- **R245-3-S1 - Tests - `test_sim_pool.py:265`, `:437`.** The stdin assertion is vacuous, because the fixture starts the runner itself on `/dev/null`. Mutant `stdin-inherited` (`sim_pool.py:311` `stdin=None`) survived. No harness reads stdin, so there is no functional impact. The arm also calls `/dev/null` "the recipe's" input, although the sequential recipe gave legs make's stdin. R246-1 S2 (M26) concurs.
- **R245-3-S2 - Tests - `sim_pool.py:177-178`.** The duplicate-leg refusal has no control: mutant `duplicates-allowed` survived. The real recipe is guarded by the Makefile inventory arm. R246-1 S2 (M20) concurs.
- **R245-3-S3 - Tests.** No gate runs `test_sim_pool.py` or `test_sim_pool_backpressure.py`: they are not in the suite recipe, the `run_all_suites.sh` preflights or any workflow. Their inventory and exclusivity arms protect a recipe that dev changed again after the base. Four of my killed mutants were detected only as a hang. The backpressure docstring (`:12`) cites an "outer command guard" that does not exist in the repository. The issue freezes workflow edits out of scope, and running the controls inside the suite would add tally lines, so a follow-up issue is the right route. R246-1 S1 and S2 concur.
- **R245-3-S4 - RTL (scheduling) - `Makefile:544-563`.** `obj_aclk` takes about 450 s, while the other ten legs take about 88 s together. Because start order follows recipe order, aclk starts about 40 s into the pool. Starting it first, with replay order unchanged, would bound the ordinary phase near aclk alone. This needs a public decision.
- **R245-3-S5 - RTL (module contract) - `Makefile:596-597`.** `clean` omits `obj_legs/`. The directory is git-ignored, and stale captures are deleted at runner start. R246-1 S3 concurs.
- I also concur with R246-1 S4 (while stdout is blocked, no new leg starts; I observed the same on real legs, and it matches legacy backpressure) and S5 (`reap_adopted` depends on `/proc/<pid>/task/<tid>/children` without a pre-launch check; not independently probed).

## Prior public findings: disposition at this head

| Finding | Disposition | Evidence |
|---|---|---|
| **R245-1 F1 MAJOR** (all five lenses): blocked replay prevents cancellation | **CLOSED** | Non-blocking cursor replay from a disk transcript (`sim_pool.py:236-282`). Capacity waits service INT/TERM/HUP (`:251-255`, `:274`). Cleanup in `finally` precedes delivery (`:405-411`). No waiting after an interrupt (`:468-474`). Flags restored (`:281-282`). My probe `scripts/probe_blocked_cancel.py` passes 3/3 at head. The same probe **fails 3/3** on the R245-1 runner (blob `761ec858`: no exit in 5 s, four processes alive). On **real legs through the actual Makefile** with stdout blocked (20,525 transcript bytes on disk, 82-86 delivered), SIGTERM, SIGINT and SIGHUP each end make by the same signal in about 5 ms. The live leg is killed and attributed, the unstarted legs are named, nothing survives and the render phase does not run (`receipts/real-cancel-blocked-*`). The shipped real-recipe regression passes 28/28 under a default SIGINT disposition. It kills all four targeted backpressure mutants. |
| R245-1: 21 original policy findings; A176 comment item | Policy: resolved and retained. Comment item: superseded by R246-1 F1 | The policy masks are unchanged from the corrected source, and `--check` and `--selftest` pass. The corrected comment is itself contradicted by measurement (F1 above). |
| R246-1 F1 MAJOR (Conformance, RTL, Docs) | **RETAINED**, independently verified | See the finding above. |
| R246-1 F2 MINOR (Tests) | **RETAINED** on cause (b), reproduced; cause (a) not reproduced here | See the finding above. |
| R246-1 S1-S5 | Concur (optional) | See Suggestions. |

## Verification of the assignment items

1. **Prior findings.** See the table above.
2. **Policy union (`scripts/check_baremetal_only.py`).** Against base, the diff removes exactly one line: the arm-group registration, re-added with the same entries plus `_arms_sim_pool_host_masks`. No dev-side mask (#504, #523, #532) is dropped. The PR-side hunks are line-identical to `483a133e..ff7dac32` apart from that line. The self-test runs 441 arms at base and 700 at head. `--check` exits 0; `--selftest` passes 700 arms. All 20 fixture literals are present at head (`receipts/baremetal_*`).
3. **Inventory (`Makefile`).** `scripts/inventory_compare.py` compares `make -n run` at base and at head (default, `SIM_JOBS=1`, and the `NOTIFY_MDIR`/`CRFLIC_MDIR` override variants).
   - In every variant: eleven ordinary executables in the same order, with the same banners and no arguments; no stray or duplicate run; the exclusive set is exactly the five `sim_nxn.cpp` legs.
   - All 25 pre-pool and 5 post-pool command lines are byte-identical. Result: `INVENTORY MATCH`.
   - #508 stays in `obj_notify`, #443 in `obj_aclk` and #530 in `obj_crflic`. The focused targets are untouched. `TESTING.md:289-301` and `README.md:15-41` list the same inventory.
   - Write set: the only runtime writes in the pooled harnesses are `sim_nxn.cpp`'s builder and image-generator calls into the private `mkdtemp` directory and the optional `MILAN_COUNTER_FRAME_OUT`. **Measured, the builder writes nothing in the tree** (R246-1 F1). No RTL file-output task exists in the resolved HDL trees.
4. **Pool semantics.**
   - Shipped controls: 17/17 and 28/28 (with F2's caveat).
   - `scripts/mutate_pool.py`: **35 single-claim mutants, 32 killed** (`receipts/mutants/SUMMARY.txt`). The trees were restored and hash-verified after each mutant.
   - Survivors: `stdin-inherited` (S1), `duplicates-allowed` (S2), and `exit-no-group-kill`, which is equivalent because subreaper adoption plus `reap_adopted` in the same call remove the orphaned group before the next launch.
   - Claims covered by killed mutants:
     - bound, including a third slot and a ceiling of 3;
     - `MAKEFLAGS` independence;
     - exclusion, order and independent overlap;
     - fail-fast, a masked failure and a missing executable;
     - the failing leg is named;
     - interrupt group kill, subreaper and adopted reaping;
     - exit by the same signal;
     - an inherited ignore is kept;
     - the child signal mask;
     - recipe-order replay;
     - frame-dump presence, including empty;
     - the four backpressure claims;
     - unstarted and killed legs are attributed;
     - Makefile inventory, exclusivity marks, the default of 2, error propagation, order, and a double run after the pool.
   - Real legs: the per-leg captures and `replay.log` are **byte-identical** across pooled cold, sequential warm and pooled warm runs (12/12, `receipts/capture_compare_all.txt`).
   - Real-leg cancellation passes with file stdout and with blocked stdout, for INT, TERM and HUP.
   - Frame dump on real legs: with the variable set, `--jobs=2` over the ten non-aclk legs ran one at a time with its note. The final dump is byte-identical to direct sequential execution (174 B), and all per-leg outputs match (`receipts/frame-dump-real/summary.txt`).
5. **Wall clock** (pinned Verilator 5.050).

   | Run | Wall clock | Notes |
   |---|---:|---|
   | Pooled cold | **1389.421 s** | 6 CPUs, `VERILATOR_JOBS=6`, shared host at load about 10; exit 0; 10074 checks / 0 failures / 16 tallies; 2210.6 s under the unchanged 3600 s budget |
   | Sequential warm | **1226.770 s** | same host |
   | Pooled warm | **1182.429 s** | same host |

   - The warm pair saves 44.341 s (3.61%). The ordinary phase takes 540 s sequential and 498 s pooled; aclk alone takes about 452 s.
   - Author figures at this head: 1421.094 s sequential cold and 1370.953 s pooled cold; 1230.269 s sequential warm and 1170.273 s pooled warm.
   - Sampled peaks (filtered by working directory): two ordinary legs and one exclusive writer pooled; one and zero sequential.
   - Peak single-process RSS: 382 MB cold, 360 MB warm.
6. **Gates.**
   - `ci_events.py --check` passes (1647 items) and `--selftest` passes (2188 arms); no workflow changed.
   - `docs_check.py` passes with git (0 findings) and without git (0 findings, 1 declared skip); `--selftest` passes.
   - `check_feature_status.py` passes without git.
   - These exit 0: `check_py_idiom`, `measure_test_evidence --check`, `measure_fail_fast --check`, `measure_naming --check`, `check_hygiene --check`, `check_todo_ownership`, `check_doc_style`, `check_rtl_source_lists`, `check_cpp_idiom`, `check_archive`, `measure_control_flow --selftest`, `suite_tally --selftest`, and phase observation 24/24.
   - With the pinned renderer in a private venv: `check_em_dash --base 5c78ce2e` (0 of 60 added lines), and `gen_toc --selftest`, `--verify-anchors` and `--check` all pass.
   - No `.budget` file changed.
   - The full default sweep was not rerun (not permitted). The author's published evidence at this head shows 5/5 chunk exits 0, 55 suites, 2,121,993 checks, 0 failures and 4 declared skips.
7. **Merge.**
   - `git merge-tree` with dev `1299b461` is clean (tree `3052b62a`). With live dev `1658ded2` it is also clean (tree `3c26bfef`; auto-merges `TESTING.md`, milan_dp `Makefile` and `README.md`).
   - Dev adds `crflic_probes.vlt` to the crflic build and no leg. It adds no file write or signal handler in `sim_crf_licence.cpp`.
   - In the materialised merged tree, `test_sim_pool.py` passes 17/17, and the inventory against live dev's sequential recipe gives `INVENTORY MATCH`.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts (at the exact head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | **UNCLEAN** (R246-1 F1 retained) | Issue body and decisions 5780232053, 5780545051, 5781783857, 5835674224 against acceptance 1-4; `make -n` inventory base vs head; real per-leg capture identity; tally 10074/0 in three real runs; frame-dump real probe; builder write-set probe against the decision's premise | R245-3 | `f36b40ddb5bf7fa5b12bba47d136e0b9d429403c` |
| RTL | **UNCLEAN** (R246-1 F1 retained; S4, S5 optional) | Scheduler `sim_pool.py:285-412`, subreaper `:86-117`, group kill `:219-226`; harness write-set audit and `endstation_builder.py:73-92,5631-5680`; build recipes byte-identical; no HDL, firmware, pin, clock, reset or CDC change | R245-3 | `f36b40ddb5bf7fa5b12bba47d136e0b9d429403c` |
| Robustness | **CLEAN** | Failure, crash, missing executable, invalid `--jobs`, `MAKEFLAGS` (arms and mutants); INT/TERM/HUP with new-session descendants; real-leg INT/TERM/HUP with blocked stdout and TERM with file stdout (`receipts/real-cancel-*`); frame-dump set; ignored-signal inheritance; merged-tree behaviour | R245-3 | `f36b40ddb5bf7fa5b12bba47d136e0b9d429403c` |
| Tests | **UNCLEAN** (R246-1 F2 retained; S1-S3 optional) | `test_sim_pool.py` (17) and `test_sim_pool_backpressure.py` (28), read in full and run, including under an inherited SIGINT ignore and 20 repeats; 35-mutant campaign; phase observation; policy selftest | R245-3 | `f36b40ddb5bf7fa5b12bba47d136e0b9d429403c` |
| Docs | **UNCLEAN** (R245-3-D1 MINOR; R246-1 F1 MAJOR) | `sim_pool.py:4-60`; `README.md:1-48,74`; `TESTING.md:289-301`; `sim_nxn.cpp:399-400`; `CI_WORKFLOWS.md:158-173` (budget rows unchanged and still accurate); docs gates in both modes | R245-3 | `f36b40ddb5bf7fa5b12bba47d136e0b9d429403c` |

```text
[R245] PASS Robustness - receipts/real-cancel-*/result.json, receipts/probe_blocked_cancel_head.txt, receipts/frame-dump-real/summary.txt, receipts/mutants/SUMMARY.txt - failure, crash, missing, bound, INT/TERM/HUP with blocked output and descendants, and frame-dump serialisation hold on real legs and under mutation
```

## Real limits

- Timing figures are single samples on a shared, loaded host. There is no same-host sequential-cold partner. The first cold run's host-wide sampler recorded another lane's processes after about 868 s; its pool window (410-455 s) is unambiguous, and later runs filtered by working directory.
- Long runs exceeded one foreground call. Each was detached with `setsid` and waited on in the foreground with `tail --pid` until it exited; nothing was left running.
- The assigned Verilator path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host. I used an identical-content wrapper to the same pinned overlay, which reports 5.050 (hashes in `receipts/verilator_identity.txt`). The system 5.052 was not used.
- The real frame-dump probe omitted `obj_aclk` and drove the runner directly with the recipe's argv, not through make.
- R246-1 F2 cause (a) was not reproduced here. R246-1 S5 was not independently probed.
- I did not run the full sweep, parent/PP/gPTP/Yosys/builder banks, trusted act or hosted gates (not permitted). Physical calibration was NOT RUN; field skips are not hardware proof.

## Pending manager duties

- Publish R246-1 F1's scope conflict on #517 for a maintainer decision.
- Arrange corrections for F1, F2 and D1, followed by an exact-head re-review of Conformance, RTL, Tests and Docs.
- Trusted act at the ready head.
- Exact-head hosted `verilator-suites` and `yosys-portability`. Both were **skipped** at this head (draft). The executed jobs (`rtl-fast`, `elaborate`, `yosys-elaboration`, `verilator-lint`, `docs-check`, `docs-check-no-git`, `bdd-conformance`, `wire-accountability`, `full-ci-gate`, `changes`) all succeeded (`receipts/hosted_check_runs.txt`).
- Hosted dedicated-worker timing against the 1999 s baseline.
- The current-dev candidate at the merge turn (live dev `1658ded2`, merge-tree clean here).
- The second independent positive review.
- Authorized merge and containment.
- A follow-up issue for S3, if accepted.

## Integrity

- The review clone matches its start state after all probes: HEAD, tree, stage-0 index records, worktree blob hashes, modes, no untracked or modified files, and gitlinks `third_party/verilog-axis` `48ff7a7e`, `protocol-processor` `990f9652`, `gptp-processor` `e5dcea6e` and `external` `efeb541a` (uninitialised, unchanged). See `receipts/integrity_before.txt` and `integrity_after.txt`.
- An ignored `scripts/__pycache__/` created by this review was removed. The mutant tree was verified restored to head bytes.
- All builds, probes and mutants ran in disposable copies under `scratch/`, with at most 8 jobs (6 build, 2 test).
- There were no source edits, commits, pushes, GitHub writes, author contact, sub-agents, Docker/act, privilege use or hardware. The only network actions were read-only: `gh api` reads and `git fetch` of dev and the evidence commit into the isolated clone.
- Host paths and the process environment are elided from published receipts.

## Reproduction (`scripts/` in this packet)

```sh
python3 scripts/check_baremetal_only.py --check; python3 scripts/check_baremetal_only.py --selftest
python3 tb/verilator/milan_dp/test_sim_pool.py; python3 tb/verilator/milan_dp/test_sim_pool_backpressure.py
bash -c 'trap "" INT; exec python3 tb/verilator/milan_dp/test_sim_pool_backpressure.py'   # R246-1 F2 (b)
$PACKET/scripts/probe_builder_writes.sh <disposable-head-tree> <outdir>                     # R246-1 F1
python3 $PACKET/scripts/inventory_compare.py <base-5c78ce2e-tree> <head-tree>
python3 $PACKET/scripts/mutate_pool.py <disposable-head-tree> <outdir> [MUTANT ...]
python3 $PACKET/scripts/probe_blocked_cancel.py <sim_pool.py> <outdir>
$PACKET/scripts/run_milan_dp.sh <tree> <SIM_JOBS> <VERILATOR_JOBS> <cpuset> <outdir> <toolbin>
python3 $PACKET/scripts/probe_real_cancel.py <built-tree> <toolbin> SIGTERM|SIGINT|SIGHUP <outdir> blocked|file
$PACKET/scripts/probe_frame_dump.sh <built-tree> <outdir>
git merge-tree --write-tree --name-only --messages f36b40dd <dev>
```

R245-3 FINISHED
