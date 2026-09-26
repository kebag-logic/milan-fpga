[R245] NEGATIVE - exact head f36b40ddb5bf7fa5b12bba47d136e0b9d429403c

Round R245-3: internal, cleared-context, independent review of issue #517 / PR #524 at exact head `f36b40ddb5bf7fa5b12bba47d136e0b9d429403c`, tree `270b9c97701047659ff1ec6040126af77b7141e1`. The whole PR `5c78ce2e9d831e588e759b696ed549804327e4d8..f36b40dd` was reviewed (commits `cce997f6`, `9ceec519`, `c0b1dd5d`, `f36b40dd`). All five lenses were applied. This is a source verdict, not a merge authorization.

**Summary.** The runner, its Makefile wiring and the policy union are correct at this head, and every behavioural claim I tested holds on real processes and on real Verilated legs. R245-1 F1 (blocked stdout defeats cancellation) is **closed**. One new MINOR documentation finding remains open: the runner's contract docstring still describes a ten-leg inventory while the recipe now passes eleven, including in the rationale for killing legs with no grace period. That leaves `Docs` unclean, so under the completion rule the verdict is NEGATIVE. Conformance, RTL, Robustness and Tests are covered clean at this head. Five SUGGESTIONs are optional.

## Findings

### R245-3-D1 - MINOR - Docs - `tb/verilator/milan_dp/sim_pool.py:8`, `:44` - runner contract states a ten-leg inventory; the no-grace SIGKILL rationale does not cover the eleventh leg

- **Authority/evidence.** AGENTS section 6 `Docs`: changed contracts must be reflected in authoritative docs. The rebase assignment (issue comment 5835674224) reconciled the pool to every leg at dev `5c78ce2e`. The recipe now passes **eleven** legs (`Makefile:544-563`), and the README (`README.md:15`), `TESTING.md:289` and the test contract (`test_sim_pool.py:37`, `:859`) all say eleven. The runner's own module contract still says `used to run ten of them` (`sim_pool.py:8`). More importantly, it justifies SIGKILL without a grace period with `none of the ten legs handles a signal` (`sim_pool.py:44`). The eleventh leg, `obj_crflic` (`sim_crf_licence.cpp`, #530), entered the pool at the rebase. The reconciliation commit updated README, TESTING and the tests but left the runner byte-identical, by the author's stated choice.
- **Independent check.** I searched all five pooled harness sources and `tb/common/verilator_harness.hpp` for `signal(`, `sigaction`, `SIGTERM`, `SIGINT`, `atexit` and `at_quick_exit`. None installs a handler, so the SIGKILL behaviour is still correct for all eleven legs. The defect is documentary only.
- **Impact.** The runner's authoritative contract misstates the inventory it enforces. The safety premise behind the uncatchable kill does not name one of the legs it now applies to, so a maintainer adding a signal-handling leg, or auditing this one, is told the audit covered "ten".
- **Required outcome.** The runner docstring states the current inventory (or states no count), and its no-signal-handler premise explicitly covers every pooled leg, including `obj_crflic`.
- **Verification.** Reading the docstring against `Makefile:544-563`. `python3 tb/verilator/milan_dp/test_sim_pool.py` stays 17/17. `python3 scripts/check_baremetal_only.py --check` and `--selftest` still pass: lines 8 and 44 carry no masked token, but the masked context at `:35` must stay byte-identical.

### Suggestions (optional; do not affect coverage)

- **R245-3-S1 - SUGGESTION - Tests - `test_sim_pool.py:265`, `:437`.** The identity arm asserts that each leg's stdin is `/dev/null`, but the fixture starts the runner itself with `stdin=subprocess.DEVNULL`. A runner that passed its own stdin through would therefore also pass. Mutant `stdin-inherited` (`sim_pool.py:311` `stdin=None`) **survived** both control files. No pooled harness reads stdin (I searched all five sources), so there is no functional impact. The arm's docstring also calls `/dev/null` "the recipe's" input, but the sequential recipe gave legs make's stdin. Starting the runner on a non-null stdin (for example a pipe) would give the assertion teeth.
- **R245-3-S2 - SUGGESTION - Tests - `sim_pool.py:177-178`.** The duplicate-leg refusal ("each runs exactly once") has no control: mutant `duplicates-allowed` **survived**. The real recipe is independently guarded by the Makefile inventory arm and by my inventory comparison, so this refusal is defence in depth.
- **R245-3-S3 - SUGGESTION - Tests - `test_sim_pool.py`, `test_sim_pool_backpressure.py`.** No gate executes these controls. They are not in the suite recipe, `scripts/run_all_suites.sh` preflights or any workflow, only in README commands (`README.md:43-48`). Their Makefile-inventory and exclusivity arms guard a recipe that dev changed again after the base (`1658ded`), so a later edit that pools a new `sim_nxn` leg without `--exclusive`, or adds a leg outside the pool, would pass every gate. Four of the 32 killed mutants were detected only as a hang (the documented behaviour), which a person has to notice. Repository precedent is mixed: `scripts/test_suite_cancellation.py` and `gptp_shadow/test_mutant_lifecycle.py` are gated, but `test_render_phase_observation.py` (#445) is not. The issue freezes workflow and shared-contract edits out of scope, and running the controls inside the suite would add non-leg tally lines, which acceptance 4 forbids. The honest route is therefore a follow-up issue to gate host-orchestration controls, not a change in this lane.
- **R245-3-S4 - SUGGESTION - RTL (scheduling/latency) - `Makefile:544-563`.** `obj_aclk` takes about 450 s, while the other ten ordinary legs take about 88 s together (sequential warm run). Because start order follows recipe order, aclk starts about 40 s into the pool, so the pool saves at most about 45 s. Starting aclk first, with replay order unchanged, would bound the ordinary phase near aclk alone. This needs a public decision, because the settled scope ties execution to recipe order.
- **R245-3-S5 - SUGGESTION - RTL (module contract) - `Makefile:596-597`.** `clean` lists every suite object directory but not the new `obj_legs/`. The directory is git-ignored (`.gitignore:98`), and the runner deletes stale captures at start, so this is housekeeping only.

## R245-1 findings: disposition at this head

| R245-1 item | Disposition at `f36b40dd` | Evidence |
|---|---|---|
| **F1 MAJOR** (all five lenses): blocked output replay prevents cancellation cleanup | **CLOSED** | The runner now replays through a disk transcript with non-blocking writes and a byte cursor (`sim_pool.py:236-282`). Capacity waits service INT/TERM/HUP (`:251-255`, `:274`). Cleanup happens in `finally` before any final delivery (`:405-411`). After an interrupt, the last delivery never waits (`:468-474`). Shared descriptor flags are restored (`:281-282`). My probe `scripts/probe_blocked_cancel.py` passes 3/3 at head (exit by the same signal in 3-5 ms, zero marked survivors, pipe still unread). The same probe **fails 3/3** against the R245-1 runner blob `761ec858` (no exit in 5 s, four processes alive), which reproduces F1. On **real Verilated legs through the actual Makefile** with stdout genuinely blocked (20,525 transcript bytes on disk, 82-86 delivered), SIGTERM, SIGINT and SIGHUP each end make by the same signal within 5 ms. The live `obj_notify` leg is killed and attributed, the nine unstarted legs are named, nothing survives and the render phase does not run. The shipped regression through the real recipe (`test_sim_pool_backpressure.py`, `make-*` variants) passes 28/28. It kills all four targeted mutants: blocking write, signals ignored in capacity wait, final drain waits, flags not restored. README `:34-40` now discloses the output contract. |
| Original 21 policy-checker findings (T/R classes on 20 lines) | Resolved; retained resolved | The PR-side mask and self-test hunks are line-identical to the corrected source `ff7dac32`, except the one arm-registration line (see the policy union row below). All 20 fixture literals exist verbatim at head. `--check` exits 0 and `--selftest` passes 700 arms. |
| A176 shared-header decision and inaccurate `sim_nxn.cpp` comment | Retained resolved | Five-leg exclusive group verified (below). The comment correction at `sim_nxn.cpp:399-400` is the only C++ change. |
| #523 residue | Retained under its own issue | Not invoked to excuse anything in this runner. |

## Verification of the assignment items

1. **R245-1 findings.** See the table above.
2. **Policy union (`scripts/check_baremetal_only.py`).** `git diff 5c78ce2e..f36b40dd` removes exactly one line: the arm-group registration list. It is re-added with the same entries plus `_arms_sim_pool_host_masks`, so no dev-side mask (#504, #523, #532) is dropped. The PR-side added lines are identical to the `483a133e..ff7dac32` hunk apart from that line (`scratch`-derived comparison, reproducible with the command in Reproduction). The dev base self-test runs 441 arms; the head runs 700. `--check` passes: 0 findings, exit 0. `--selftest` passes: 700 arms, exit 0. All 20 fixture literals are present at head (`receipts/baremetal_fixture_presence.txt`).
3. **Inventory (`Makefile`).** `scripts/inventory_compare.py` compares `make -n run` at base `5c78ce2e` (sequential recipe) with head, for the default, `SIM_JOBS=1` and `NOTIFY_MDIR`/`CRFLIC_MDIR` override variants. In each, the eleven ordinary executables appear in the same order with the same banners and no argument, with no stray direct ordinary leg and no duplicate. The exclusive set is exactly the five legs built from `sim_nxn.cpp` (`obj_notify`, `obj_nxn`, `obj_nxndv`, `obj_nxn8`, `obj_nxn4c`), and I confirmed that from the Makefile build lines. All 25 non-pool command lines before the pool (builds, gPTP prerequisites, generators) and all 5 after it (render-law and GM-step controls) are byte-identical. Result: `INVENTORY MATCH` (`receipts/inventory_compare.txt`). The #508 GET_STREAM_INFO checks stay in `obj_notify`, the #443 render CSR checks in `obj_aclk` and #530 in `obj_crflic`. The focused `notify`, `gsi-mutants`, `crflic*` and `render-csr-controls` targets are untouched; the only Makefile hunks are `SIM_JOBS` and the pool line. `TESTING.md:289-301` and `README.md:15-41` list the same inventory. A runtime audit of the six pooled harness sources found no file write except `sim_nxn.cpp` (builder `system()` calls at `:411` and `:422`, the private `mkdtemp` image directory, and `MILAN_COUNTER_FRAME_OUT` at `:3640`), and no RTL `$fopen`, `$fwrite`, `$writemem` or `$dumpfile` in `hdl/`, `third_party/verilog-axis/rtl` or the processor HDL. Grouping only the `sim_nxn` legs is therefore complete.
4. **Pool semantics.** The shipped controls pass: `test_sim_pool.py` 17/17 and `test_sim_pool_backpressure.py` 28/28. `scripts/mutate_pool.py` built **35 mutants, one per claim**, each an exact single substitution in a disposable tree that is restored and hash-checked after each mutant. **32 were killed.** Of the 3 survivors, `stdin-inherited` and `duplicates-allowed` are S1 and S2. `exit-no-group-kill` is behaviourally equivalent: removing the per-leg group kill in `reap_exited` still leaves nothing alive, because the leg's orphaned group members are adopted by the subreaper and killed by `reap_adopted` in the same call, before the next launch. Claims covered by killed mutants:
   - two-child bound, including a third slot and a ceiling of 3;
   - independence from `MAKEFLAGS`;
   - exclusion, group order and independent overlap;
   - fail-fast, masked failure and missing executable;
   - failing leg named;
   - interrupt kills groups, with the subreaper and adopted-descendant reaping;
   - exit by the same signal;
   - inherited ignore kept;
   - child signal mask;
   - recipe-order replay;
   - frame-dump presence, including empty;
   - the four backpressure claims;
   - unstarted legs named and killed legs attributed;
   - Makefile inventory, exclusivity marks, default of 2, error propagation, order, and a double run after the pool.

   On real legs, the per-leg captures and ordered `replay.log` are **byte-identical** across pooled cold, sequential warm and pooled warm runs (12/12, `receipts/capture_compare_all.txt`). Cancellation works on real legs with regular-file stdout (SIGTERM, two live legs) and with blocked stdout (INT/TERM/HUP), as reported under F1. With `MILAN_COUNTER_FRAME_OUT` set, the pool at `--jobs=2` over the ten non-aclk real legs ran one at a time with its note. The final dump is byte-identical to direct sequential execution (174 B, same SHA-256), and all ten per-leg outputs match (`receipts/frame-dump-real/summary.txt`). `SIM_JOBS=1` reproduces the sequential inventory and order (`make -n` and the real run: sampled peak 1).
5. **Wall clock.** The reproduced pooled **cold** run took **1389.421 s**. It used 6 CPUs (`taskset 0-5`), `VERILATOR_JOBS=6` and Verilator 5.050 on a shared host at load about 10, and left 2210.6 s of the unchanged 3600 s budget. It recorded exit 0 and 10074 checks / 0 failures / 16 tallies (the author's 1370.953 s pooled cold is the same order). Same-host warm pair: sequential **1226.770 s**, pooled **1182.429 s**, saving **44.341 s (3.61%)**; the author reports 59.996 s (4.88%). The ordinary phase took 540 s sequential and 498 s pooled; aclk alone takes about 452 s. Sampled peak was two ordinary legs and one exclusive writer (pooled) and 1/0 (sequential). GNU time's single-process peak RSS was 382 MB cold and 360 MB warm. Tracked generated-header hashes were unchanged in every run. The cold figure has no same-host sequential-cold partner. It is one sample on a loaded shared host and is not a hosted prediction.
6. **Gates.** `ci_events.py --check` passes (1647 contract items) and `--selftest` passes (2188 arms). No workflow changed. `docs_check.py` passes with git (0 findings, 165 pages) and without git in an extracted archive (0 findings, one declared git-only skip); `--selftest` passes. `check_feature_status.py` passes without git. Also exit 0: `check_py_idiom`, `measure_test_evidence --check`, `measure_fail_fast --check`, `measure_naming --check`, `check_hygiene --check`, `check_todo_ownership`, `check_doc_style`, `check_rtl_source_lists`, `check_cpp_idiom`, `check_archive`, `measure_control_flow --selftest`, `suite_tally --selftest`, and the phase-observation controls (24/24). The same holds, with the pinned Markdown renderer in a private venv, for `check_em_dash --base 5c78ce2e` (0 findings over 60 added lines) and `gen_toc --selftest`, `--verify-anchors` and `--check`. No `.budget` file changed. I did not rerun the full default sweep (not permitted). The author's published chunked sweep at this head shows 5/5 chunk exits 0, 55 suites, 2,121,993 checks, 0 failures and 4 declared skips; chunk 4/5 is `milan_dp` alone with 10,074 checks. That is author evidence at `2f5dfa97:review-evidence/517-r1/author-r4/`, not reviewer reproduction.
7. **Merge.** `git merge-tree --write-tree` of `f36b40dd` with dev `1299b461` is clean (tree `3052b62a`, auto-merge of `TESTING.md`). With live dev `1658ded2` it is also clean (tree `3c26bfef`, auto-merges of `TESTING.md`, milan_dp `Makefile` and `README.md`). Dev's Makefile change adds `crflic_probes.vlt` to the crflic build and adds no leg. Dev's `sim_crf_licence.cpp` changes add no file write or signal handler. In the materialized merged tree, `test_sim_pool.py` passes 17/17 and the inventory comparison against live dev's sequential recipe gives `INVENTORY MATCH`. The manager still owns the final current-dev candidate build.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts (at the exact head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | **CLEAN** | Issue body and decisions 5780545051, 5781783857, 5835674224 against acceptance 1-4: `make -n` inventory base vs head (`receipts/inventory_compare.txt`); real per-leg capture identity; tally 10074/0 in all three real runs; frame-dump real probe; `SIM_JOBS` bound at `Makefile:28`, `sim_pool.py:149-179`; render/GM-step phases after the pool. | R245-3 | `f36b40ddb5bf7fa5b12bba47d136e0b9d429403c` |
| RTL | **CLEAN** (S4, S5 optional) | Host scheduling architecture `sim_pool.py:285-412` (bounded eligibility loop `:385-395`, SIGCHLD/sigwait service, subreaper `:86-117`, group kill `:219-226`); runtime write-set audit of `sim_main.cpp`, `sim_nxn.cpp`, `sim_crf_licence.cpp`, `sim_prune.cpp`, `sim_aclk.cpp`, `verilator_harness.hpp`, and RTL file-output search; build recipes byte-identical (`make -n`); no HDL, firmware, pin, clock, reset or CDC change in `git diff --stat`. | R245-3 | `f36b40ddb5bf7fa5b12bba47d136e0b9d429403c` |
| Robustness | **CLEAN** | Failure, crash, missing executable, invalid `--jobs` and inherited `MAKEFLAGS` (shipped arms plus mutants); INT/TERM/HUP with new-session descendants (fake legs); INT/TERM/HUP on real legs with blocked stdout and SIGTERM with file stdout (`receipts/real-cancel-*`); frame-dump set; ignored-signal inheritance; merged-tree behaviour. | R245-3 | `f36b40ddb5bf7fa5b12bba47d136e0b9d429403c` |
| Tests | **CLEAN** (S1, S2, S3 optional) | `test_sim_pool.py` 17 arms and `test_sim_pool_backpressure.py` 28 controls, run and read in full; 35-mutant campaign (`receipts/mutants/`), 32 killed, survivors analysed; phase observation 24/24; tally selftest; policy selftest 700 arms. | R245-3 | `f36b40ddb5bf7fa5b12bba47d136e0b9d429403c` |
| Docs | **UNCLEAN** (R245-3-D1 MINOR open) | `sim_pool.py:4-60` docstring; `README.md:1-48,74`; `TESTING.md:289-301`; `sim_nxn.cpp:399-400`; `CI_WORKFLOWS.md` milan_dp budget rows (`:158-173`, unchanged, still accurate); docs gates in both modes. | R245-3 | `f36b40ddb5bf7fa5b12bba47d136e0b9d429403c` |

Clean-lens lines:

```text
[R245] PASS Conformance - tb/verilator/milan_dp/Makefile:544-563 + receipts/inventory_compare.txt - 11 legs, order, banners, argv, exclusivity and all non-pool commands match the base sequential recipe; real per-leg captures and 10074/0 tally identical across modes
[R245] PASS RTL - tb/verilator/milan_dp/sim_pool.py:86-117,219-226,285-412 + harness write-set audit - bounded two-slot scheduler, ordered exclusive group, subreaper/group cleanup and signal service are sound; no production RTL/interface change
[R245] PASS Robustness - receipts/real-cancel-*/result.json, receipts/probe_blocked_cancel_head.txt, receipts/frame-dump-real/summary.txt - failure, crash, missing, bound, INT/TERM/HUP with blocked output and descendants, frame-dump serialization all hold on real legs
[R245] PASS Tests - tb/verilator/milan_dp/test_sim_pool.py, test_sim_pool_backpressure.py + receipts/mutants/SUMMARY.txt - 17/17 and 28/28; 32 of 35 claim mutants killed; survivors are S1/S2 and one equivalent mutant
```

## Real limits

- The cold timing has no same-host sequential-cold partner. The host was shared with other lanes (load about 10). All figures are single samples and not hosted predictions. The first cold run's concurrency sampler was host-wide, and after about 868 s it recorded another lane's milan_dp processes. Its pool-phase window (410-455 s) is unambiguous, and the warm runs used a sampler filtered by working directory.
- Long runs could not fit one foreground call, so each was detached with `setsid` and then waited on in the foreground (`tail --pid`) until it exited. Nothing was left running.
- The assigned Verilator path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist on this host. I used a wrapper with identical content pointing at the same pinned overlay as the other pinned-tool wrappers there. It reports `Verilator 5.050 2026-07-01 rev v5.050`, and `receipts/verilator_identity.txt` records the binary hashes. The system `/usr/bin/verilator` (5.052) was not used.
- The frame-dump real probe omitted `obj_aclk` (about 450 s; it writes no frame file) and drove the runner directly with the recipe's argv, not through `make`. Make's environment pass-through is not separately exercised on real legs; the fake-leg Makefile controls cover it.
- I did not rerun the full default sweep, parent/PP/gPTP/Yosys/builder banks, the trusted act replica or hosted gates (not permitted). Default-sweep figures are author evidence.
- Physical calibration was NOT RUN. Field and freshness skips are not hardware proof.

## Pending manager duties

Remaining duties:

- trusted local replica (act) at the ready head;
- exact-head hosted `verilator-suites` and `yosys-portability` (both **skipped** at this head because the PR is a draft; the executed jobs are `rtl-fast`, `elaborate`, `yosys-elaboration`, `verilator-lint`, `docs-check`, `docs-check-no-git`, `bdd-conformance`, `wire-accountability`, `full-ci-gate` and `changes`, all success; `receipts/hosted_check_runs.txt`);
- hosted dedicated-worker timing against the 1999 s baseline;
- the external independent review;
- the final current-dev candidate at the merge turn (live dev `1658ded2`, merge-tree clean here);
- authorized merge and post-merge containment;
- a follow-up issue for S3, if accepted.

## Integrity

The review clone matches the start state exactly after all probes: HEAD, tree, stage-0 index records, worktree blob hashes, modes, zero untracked or modified files, and gitlinks `third_party/verilog-axis` `48ff7a7e`, `protocol-processor` `990f9652`, `gptp-processor` `e5dcea6e` and `external` `efeb541a` (uninitialized, unchanged). See `receipts/integrity_before.txt` and `receipts/integrity_after.txt`. An ignored `scripts/__pycache__/` created by this review was removed. The mutant tree was verified restored to head bytes (`receipts/integrity_mutant_tree_after.txt`). All builds, probes and mutants ran in disposable copies under `scratch/`. Parallelism stayed at or below 8 jobs: 6 for builds on CPUs 0-5, and 2 for tests and probes on CPUs 6-7. There were no source edits, commits, pushes, GitHub writes, author contact, sub-agents, Docker/act, privilege use or hardware. The only network actions were read-only: `gh api` reads and `git fetch` of dev and the evidence commit into the isolated clone.

## Reproduction

The scripts live under `scripts/` in this packet. `TREE` is a disposable copy of the head checkout with submodules; `TOOLBIN` holds a `verilator` wrapper resolving to 5.050.

```sh
python3 scripts/check_baremetal_only.py --check; python3 scripts/check_baremetal_only.py --selftest
python3 tb/verilator/milan_dp/test_sim_pool.py; python3 tb/verilator/milan_dp/test_sim_pool_backpressure.py
python3 $PACKET/scripts/inventory_compare.py <base-5c78ce2e-tree> <head-tree>
python3 $PACKET/scripts/mutate_pool.py <disposable-head-tree> <outdir> [MUTANT ...]
python3 $PACKET/scripts/probe_blocked_cancel.py <sim_pool.py> <outdir>
$PACKET/scripts/run_milan_dp.sh <tree> <SIM_JOBS> <VERILATOR_JOBS> <cpuset> <outdir> <toolbin>
python3 $PACKET/scripts/probe_real_cancel.py <built-tree> <toolbin> SIGTERM|SIGINT|SIGHUP <outdir> blocked|file
$PACKET/scripts/probe_frame_dump.sh <built-tree> <outdir>
git diff --no-color 483a133e ff7dac32 -- scripts/check_baremetal_only.py | grep -E '^[+-][^+-]'   # compare with 5c78ce2e..f36b40dd
git merge-tree --write-tree --name-only --messages f36b40dd <dev>
```
