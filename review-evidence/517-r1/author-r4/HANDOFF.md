# [A321] Rebase handoff for PR #524

Status: assigned local rebase round complete at `f36b40ddb5bf7fa5b12bba47d136e0b9d429403c`. All requested final-head commands exit 0, including both builder modes, pool/cancellation controls, four complete-suite measurements and all five default sweep chunks. The combined sweep covers all 55 selected suites exactly once: 2121993 checks, zero failures, four declared field-campaign/freshness skips. Independent review and publication remain open.

Starting head: ff7dac3257a321538a1fd1a310ab3190f646153d
Required base: 5c78ce2e9d831e588e759b696ed549804327e4d8
Remote: https://github.com/kebag-logic/milan-fpga.git

Startup checks: the origin URL matched the required HTTPS URL. `git fetch origin dev` exited 0 and `origin/dev` resolved to the required base shown above. `git rebase origin/dev` completed with the three conflict hunks recorded below. `git submodule update --init` completed; the missing pinned gPTP commit was fetched from `https://github.com/Mister-M-alt/FPGA-gPTP.git`. The final pin and tracked-byte audit is in `final-integrity.json`.

`public-pr-state.json` contains the final `gh pr view 524 --json body,headRefOid,isDraft,url` result. The published PR is still draft at `5874895eb817ed41c0f8be4eb427ad3315c29844`; the supplied local replacement body starts with `[A321]` and retains every original section and the Closes line.

## Commit sequence

The first three one-line subjects were retained; the fourth reconciles the inventory, documentation and Makefile fixtures. Every commit has an empty body and no trailers.

- `cce997f69ec27fe62af5d357e9e3670588286c8e` Bound ordinary milan_dp simulations with ordered shared-header exclusion
- `9ceec5199b70e3eeae555b9215d4621d0546022a` Bound simulation host-tool policy masks to their source contexts
- `c0b1dd5db1132d2bccbd1474ca7128b2bfb435ee` Make simulation pool cancellation independent of stdout backpressure
- `f36b40ddb5bf7fa5b12bba47d136e0b9d429403c` Reconcile pooled simulation inventory with the current default suite

`source-scope.json` verifies the runner is byte-identical to the starting correction, and the workflow files, sweep driver, mutation campaigns, HDL, firmware and required submodule pins are unchanged from the required base. The eight-file PR diff is confined to the original pool/policy work and its inventory reconciliation.

## Scope

[Assignment](https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5835674224): rebase the corrected source, retain the union of policy masks, reconcile every ordinary leg and focused target, validate the full default suite/sweep, compare complete-suite times on the same CPUs, and run CI event checks. Executor [A321]; independent reviewers [R245] and [R246]. Source remains local; no push, PR mutation, merge, additional checkout or hardware work.

## Conflict resolutions

Rebase commit 1: `tb/verilator/milan_dp/Makefile:540` (one hunk; original in `conflict-01-Makefile.txt`). Preserve dev NOTIFY_BUILD and CRFLIC_BUILD, their directory overrides and banners. Route all eleven ordinary commands through the existing pool in dev order; preserve the five exclusive sim_nxn writers. Preserve focused targets, prerequisites, render and GM-step campaign phases. Final references: `tb/verilator/milan_dp/Makefile:542` and `:543` retain both build macro invocations; `:544` introduces the pool; `:549` adds the CRF licence executable. `:480` retains all prerequisites; `:565` and `:567` retain the post-pool render and GM-step campaign sequence.

Rebase commit 2: two policy hunks (originals in `conflict-02-policy.txt`). `TERM_MASKS`: retain SDK entries and append all three simulation term entries. `selftest`: register both slot masks and simulation masks once, keeping every existing group. Runtime-mask additions merged automatically; their full union is verified in `policy-union.json`.

Policy conflict final references: `scripts/check_baremetal_only.py:293` begins the united term table; SDK entries at `:296` precede simulation entries. Runtime union starts at `:315`. `selftest:1616` registers both slot and simulation groups once. `policy-union.json` proves every dev mask and helper unchanged, all PR-added masks/helpers retained, and the exact union of registered groups.

| Saved hunk | Final location | Resolution |
| --- | --- | --- |
| Makefile hunk 1 | `tb/verilator/milan_dp/Makefile:542` | Keep both base build macros and directory overrides; pool all eleven ordinary legs in base order with five exclusive writers. |
| Policy hunk 1 | `scripts/check_baremetal_only.py:293` | Keep SDK term masks and append all three simulation term masks. |
| Policy hunk 2 | `scripts/check_baremetal_only.py:1616` | Register the base slot-mask and simulation-mask self-test groups once each. |

## Leg inventory

The starting PR has ten ordinary legs. The required base has eleven. The rebased pool runs all eleven once, with no executable arguments, in the same suite directory and replay order as the base. The first-column order below is the base and rebased order. `test_sim_pool.py` checks expanded recipes, directory overrides and phase ordering; `test_sim_pool_backpressure.py` executes the real recipe with inert build/prerequisite fixtures.

| Order | Executable | Starting PR | Base | Rebased pool | Group |
| --- | --- | --- | --- | --- | --- |
| 1 | `obj_dir/Vmilan_dp_sim` | yes | yes | yes | independent |
| 2 | `obj_notify/Vmilan_dp_notify` | yes | #508 GSI added | yes, `NOTIFY_MDIR` retained | exclusive |
| 3 | `obj_crflic/Vmilan_dp_crflic` | absent | yes | yes, `CRFLIC_MDIR` retained | independent |
| 4 | `obj_nxn/Vmilan_dp_nxn` | yes | yes | yes | exclusive |
| 5 | `obj_nxndv/Vmilan_dp_nxndv` | yes | yes | yes | exclusive |
| 6 | `obj_nxn8/Vmilan_dp_nxn8` | yes | yes | yes | exclusive |
| 7 | `obj_nxn4c/Vmilan_dp_nxn4c` | yes | yes | yes | exclusive |
| 8 | `obj_nolpf/Vmilan_dp_nolpf` | yes | yes | yes | independent |
| 9 | `obj_prune/Vmilan_dp_prune` | yes | yes | yes | independent |
| 10 | `obj_ax1x1/Vmilan_dp_ax1x1` | yes | yes | yes | independent |
| 11 | `obj_aclk/Vmilan_dp_aclk` | yes | #443 CSR checks added | yes | independent |

`sim_crf_licence.cpp` adds no filesystem writer or subprocess; its AXI writes address the simulated DUT. The five existing shared-header writers keep their exclusive relative order. Frame-output environment presence still selects whole-set serialization.

Fourteen default elaborations comprise these eleven plus `gptp`, `gptp-lat` and `gmstep`; the prerequisite recipes precede the pool. Default render-law and GM-step mutation controls follow pool success. The #508 `notify-build`, `notify`, `gsi-mutants` targets and #443 `aclk-build`, `render-csr-controls` targets remain present with unchanged bodies; their full explicit campaigns stay outside the default pool, as required by `TESTING.md:257`. No explicit campaign is silently added to or removed from the default sweep. `docs/testing/TESTING.md:288` and the suite README record the reconciled population.

## Wall-clock measurements

The unchanged budget is 3600 s (`docs/testing/CI_WORKFLOWS.md:159`). Cold means suite build artifacts were cleaned, not filesystem-cache eviction. Warm retains same-mode builds and reruns all phases. CPU affinity is 16-23 with eight build jobs and pinned version 5.050.

| Run | CPUs | Seconds | Exit | Budget margin | Evidence |
| --- | --- | --- | --- | --- | --- |
| sequential-cold | 16-23 | 1421.094 | 0 | 2178.906 s | `sequential-cold/result.json` |
| sequential-warm | 16-23 | 1230.269 | 0 | 2369.731 s | `sequential-warm/result.json` |
| pooled-cold | 16-23 | 1370.953 | 0 | 2229.047 s | `pooled-cold/result.json` |
| pooled-warm | 16-23 | 1170.273 | 0 | 2429.727 s | `pooled-warm/result.json` |

## Gates

Every invocation retains its own head, command, exit and raw log. Failed preliminary attempts remain listed.

| Gate | Command | Head | Exit | Seconds | Log |
| --- | --- | --- | --- | --- | --- |
| pool-unit | `python3 tb/verilator/milan_dp/test_sim_pool.py` | `c0b1dd5d` | 0 | 6.977 | `pool-unit.log` |
| pool-unit-final | `python3 tb/verilator/milan_dp/test_sim_pool.py` | `edf385fd` | 0 | 7.063 | `pool-unit-final.log` |
| pool-backpressure | `python3 tb/verilator/milan_dp/test_sim_pool_backpressure.py` | `edf385fd` | -2 | 78.791 | `pool-backpressure.log` |
| pool-backpressure-final | `python3 tb/verilator/milan_dp/test_sim_pool_backpressure.py` | `b6d61803` | 0 | 12.329 | `pool-backpressure-final.log` |
| baremetal | `python3 scripts/check_baremetal_only.py --check` | `b6d61803` | 0 | 14.463 | `baremetal.log` |
| baremetal-selftest | `python3 scripts/check_baremetal_only.py --selftest` | `b6d61803` | 0 | 5.119 | `baremetal-selftest.log` |
| docs-git | `python3 -B scripts/docs_check.py` | `b6d61803` | 0 | 4.132 | `docs-git.log` |
| docs-no-git | `env GIT_DIR=/nonexistent/517-no-git python3 -B scripts/docs_check.py` | `b6d61803` | 0 | 4.142 | `docs-no-git.log` |
| em-dash | `python3 scripts/check_em_dash.py --base 5c78ce2e9d831e588e759b696ed549804327e4d8` | `b6d61803` | 2 | 0.803 | `em-dash.log` |
| doc-style | `python3 scripts/check_doc_style.py` | `b6d61803` | 0 | 0.062 | `doc-style.log` |
| toc-check | `python3 scripts/gen_toc.py --check` | `b6d61803` | 2 | 0.078 | `toc-check.log` |
| toc-anchors | `python3 scripts/gen_toc.py --verify-anchors` | `b6d61803` | 2 | 0.061 | `toc-anchors.log` |
| doc-paths | `python3 scripts/check_doc_paths.py` | `b6d61803` | 0 | 0.063 | `doc-paths.log` |
| module-matrix | `python3 docs/traceability/gen_module_matrix.py --check` | `b6d61803` | 0 | 0.926 | `module-matrix.log` |
| xvlog | `python3 scripts/xvlog_gate.py --check` | `b6d61803` | 0 | 137.521 | `xvlog.log` |
| rtl-source-lists | `python3 scripts/check_rtl_source_lists.py` | `b6d61803` | 0 | 1.362 | `rtl-source-lists.log` |
| sv-idiom | `python3 scripts/check_sv_idiom.py` | `b6d61803` | 0 | 0.406 | `sv-idiom.log` |
| rtl-lint | `python3 scripts/lint_rtl.py --check` | `b6d61803` | 0 | 8.131 | `rtl-lint.log` |
| cpp-idiom | `python3 scripts/check_cpp_idiom.py` | `b6d61803` | 0 | 1.182 | `cpp-idiom.log` |
| py-idiom | `python3 scripts/check_py_idiom.py` | `b6d61803` | 1 | 3.214 | `py-idiom.log` |
| port-contracts | `python3 scripts/check_port_contracts.py` | `b6d61803` | 0 | 2.305 | `port-contracts.log` |
| naming | `python3 scripts/measure_naming.py --check` | `b6d61803` | 0 | 0.434 | `naming.log` |
| test-evidence | `python3 scripts/measure_test_evidence.py --check` | `b6d61803` | 0 | 5.350 | `test-evidence.log` |
| behave | `bash -c 'cd tests && behave --no-capture -f plain'` | `b6d61803` | 0 | 1.122 | `behave.log` |
| diff-check | `git diff --check` | `b6d61803` | 0 | 0.018 | `diff-check.log` |
| ci-events | `python3 scripts/ci_events.py --check` | `b6d61803` | 0 | 0.168 | `ci-events.log` |
| ci-events-selftest | `python3 scripts/ci_events.py --selftest` | `b6d61803` | 0 | 14.626 | `ci-events-selftest.log` |
| phase-observation | `python3 tb/verilator/milan_dp/test_render_phase_observation.py` | `b6d61803` | 0 | 0.103 | `phase-observation.log` |
| baremetal-final | `python3 scripts/check_baremetal_only.py --check` | `f36b40dd` | 0 | 14.328 | `baremetal-final.log` |
| baremetal-selftest-final | `python3 scripts/check_baremetal_only.py --selftest` | `f36b40dd` | 0 | 5.161 | `baremetal-selftest-final.log` |
| docs-git-final | `python3 -B scripts/docs_check.py` | `f36b40dd` | 0 | 4.126 | `docs-git-final.log` |
| docs-no-git-final | `env GIT_DIR=/nonexistent/517-no-git python3 -B scripts/docs_check.py` | `f36b40dd` | 0 | 4.121 | `docs-no-git-final.log` |
| em-dash-final | `python3 scripts/check_em_dash.py --base 5c78ce2e9d831e588e759b696ed549804327e4d8` | `f36b40dd` | 0 | 2.959 | `em-dash-final.log` |
| doc-style-final | `python3 scripts/check_doc_style.py` | `f36b40dd` | 0 | 0.046 | `doc-style-final.log` |
| toc-check-final | `python3 scripts/gen_toc.py --check` | `f36b40dd` | 0 | 2.430 | `toc-check-final.log` |
| toc-anchors-final | `python3 scripts/gen_toc.py --verify-anchors` | `f36b40dd` | 0 | 1.553 | `toc-anchors-final.log` |
| doc-paths-final | `python3 scripts/check_doc_paths.py` | `f36b40dd` | 0 | 0.065 | `doc-paths-final.log` |
| module-matrix-final | `python3 docs/traceability/gen_module_matrix.py --check` | `f36b40dd` | 0 | 0.951 | `module-matrix-final.log` |
| xvlog-final | `python3 scripts/xvlog_gate.py --check` | `f36b40dd` | 0 | 137.278 | `xvlog-final.log` |
| rtl-source-lists-final | `python3 scripts/check_rtl_source_lists.py` | `f36b40dd` | 0 | 1.312 | `rtl-source-lists-final.log` |
| sv-idiom-final | `python3 scripts/check_sv_idiom.py` | `f36b40dd` | 0 | 0.405 | `sv-idiom-final.log` |
| rtl-lint-final | `python3 scripts/lint_rtl.py --check` | `f36b40dd` | 0 | 7.792 | `rtl-lint-final.log` |
| cpp-idiom-final | `python3 scripts/check_cpp_idiom.py` | `f36b40dd` | 0 | 1.154 | `cpp-idiom-final.log` |
| py-idiom-final | `python3 scripts/check_py_idiom.py` | `f36b40dd` | 0 | 3.192 | `py-idiom-final.log` |
| port-contracts-final | `python3 scripts/check_port_contracts.py` | `f36b40dd` | 0 | 2.269 | `port-contracts-final.log` |
| naming-final | `python3 scripts/measure_naming.py --check` | `f36b40dd` | 0 | 0.424 | `naming-final.log` |
| test-evidence-final | `python3 scripts/measure_test_evidence.py --check` | `f36b40dd` | 0 | 5.173 | `test-evidence-final.log` |
| behave-final | `bash -c 'cd tests && behave --no-capture -f plain'` | `f36b40dd` | 0 | 1.123 | `behave-final.log` |
| diff-check-final | `git diff --check` | `f36b40dd` | 0 | 0.018 | `diff-check-final.log` |
| ci-events-final | `python3 scripts/ci_events.py --check` | `f36b40dd` | 0 | 0.170 | `ci-events-final.log` |
| pool-unit-candidate | `python3 tb/verilator/milan_dp/test_sim_pool.py` | `f36b40dd` | 0 | 7.025 | `pool-unit-candidate.log` |
| ci-events-selftest-final | `python3 scripts/ci_events.py --selftest` | `f36b40dd` | 0 | 14.554 | `ci-events-selftest-final.log` |
| phase-observation-final | `python3 tb/verilator/milan_dp/test_render_phase_observation.py` | `f36b40dd` | 0 | 0.094 | `phase-observation-final.log` |
| pool-backpressure-candidate | `python3 tb/verilator/milan_dp/test_sim_pool_backpressure.py` | `f36b40dd` | 0 | 11.426 | `pool-backpressure-candidate.log` |
| builder-sdk | `python3 $EVIDENCE/builder-sdk.py` | `f36b40dd` | 0 | 669.900 | `builder-sdk.log` |
| builder-no-compiler | `python3 $EVIDENCE/builder-no-compiler.py` | `f36b40dd` | 0 | 469.725 | `builder-no-compiler.log` |
| sequential-cold | `python3 $EVIDENCE/benchmark.py sequential-cold 1 cold` | `f36b40dd` | 0 | 1421.651 | `sequential-cold.log` |
| sequential-warm | `python3 $EVIDENCE/benchmark.py sequential-warm 1 warm` | `f36b40dd` | 0 | 1230.554 | `sequential-warm.log` |
| pooled-cold | `python3 $EVIDENCE/benchmark.py pooled-cold 2 cold` | `f36b40dd` | 0 | 1372.000 | `pooled-cold.log` |
| pooled-warm | `python3 $EVIDENCE/benchmark.py pooled-warm 2 warm` | `f36b40dd` | 0 | 1170.547 | `pooled-warm.log` |
| benchmark-comparison | `python3 $EVIDENCE/compare-benchmarks.py` | `f36b40dd` | 0 | 1.662 | `benchmark-comparison.log` |
| sweep-0 | `scripts/run_all_suites.sh $EVIDENCE/sweep-0 --shard 0/5` | `f36b40dd` | 0 | 564.104 | `sweep-0.log` |
| sweep-1 | `scripts/run_all_suites.sh $EVIDENCE/sweep-1 --shard 1/5` | `f36b40dd` | 0 | 1412.828 | `sweep-1.log` |
| sweep-2 | `scripts/run_all_suites.sh $EVIDENCE/sweep-2 --shard 2/5` | `f36b40dd` | 0 | 711.309 | `sweep-2.log` |
| benchmark-equivalence-check | `python3 $EVIDENCE/compare-benchmarks.py` | `f36b40dd` | 0 | 1.781 | `benchmark-equivalence-check.log` |
| sweep-3 | `scripts/run_all_suites.sh $EVIDENCE/sweep-3 --shard 3/5` | `f36b40dd` | 0 | 471.906 | `sweep-3.log` |
| sweep-4 | `scripts/run_all_suites.sh $EVIDENCE/sweep-4 --shard 4/5` | `f36b40dd` | 0 | 1279.530 | `sweep-4.log` |
| sweep-accounting | `python3 $EVIDENCE/aggregate-sweep.py` | `f36b40dd` | 0 | 0.811 | `sweep-accounting.log` |
| source-integrity | `python3 $EVIDENCE/verify-integrity.py` | `f36b40dd` | 0 | 0.213 | `source-integrity.log` |
| final-diff-worktree | `git diff --check` | `f36b40dd` | 0 | 0.017 | `final-diff-worktree.log` |
| final-diff-base | `git diff --check 5c78ce2e9d831e588e759b696ed549804327e4d8 HEAD` | `f36b40dd` | 0 | 0.019 | `final-diff-base.log` |

## Final state

Local candidate: `f36b40ddb5bf7fa5b12bba47d136e0b9d429403c`, based on `5c78ce2e9d831e588e759b696ed549804327e4d8`. The parent worktree and index match the committed tree; all required submodule worktrees and indexes match their exact pinned commits. `final-integrity.json` records the file counts and pins. Final whitespace checks cover both the working tree and the complete base-to-head diff. Commit subjects are one line, with no bodies or trailers.

The source is local and unpublished by this round. R245 F1 remains MAJOR under all five lenses pending independent re-review; its correction is retained and the author does not clear the finding. R246 external review, reviewer-owned lens coverage, trusted local replication, hosted gates/timing, candidate validation, authorized merge and post-merge containment remain open. The authorized final issue comment is in `REVIEW-READY.md`; this is author evidence, not a review verdict.

`PR-BODY.md` retains the full current PR body structure and Closes line, adds the rebase and measured results, and is a local replacement for the manager. No push, PR edit, merge, additional checkout, hardware action or donor edit was performed.

## Measurement interpretation

`benchmark-equivalence.json` records cold savings of 50.140 s (3.53%) and warm savings of 59.996 s (4.88%). Each full default invocation reports 10074 checks, zero failures and 16 tallies. All eleven per-leg byte streams, the complete ordered replay, executable hashes and recorded runtime-input hashes are identical across all four runs. Every tracked SystemVerilog header is unchanged before/after, and each run verifies a clean tracked worktree.

The observed ordinary/exclusive peaks are 1/1 sequential and 2/1 pooled. Summed descendant RSS peaks are 2650512/2605724 KiB for sequential cold/warm and 2645188/2613576 KiB for pooled cold/warm. These are 0.5-second samples and include shared resident pages in each process; they are neither a cgroup high-water mark nor a proof about unobserved instants. Short legs are accounted for by their eleven complete captures, not by claiming every short process was sampled. Timing includes all prerequisites, ordinary simulations and post-pool campaigns; completion is detected on a nominal 0.5-second polling interval, so subsecond timing precision is limited by sampling and scheduling.

This is one cold/warm pair per mode on a shared host, on CPUs 16-23 with eight build jobs, pinned Verilator 5.050 and identical inputs. The resource logs retain host load samples. It establishes the measured local improvement and budget margin, not hosted timing or an uncontended-host bound. No workflow timeout or budget changed.

## Validation notes

The default `tsn_fuzz` selection declares four skips because `tsn-gen` is absent: the AAF/AVTP and gPTP/802.1AS field campaigns and their two corresponding `TEST_RESULTS.md` freshness checks. These ran no checks and contribute zero to the sweep total. The repository selector, environment and skip accounting are unchanged; no additional checkout was created. The five sweep exits and aggregate tally retain this limit explicitly.

Initial rebased backpressure run was interrupted after all 14 direct controls passed and the first Makefile fixture failed before starting simulations. The new CRF recipe emits `run: .SHELLSTATUS := 0` before the prerequisite row in `make -np`; the old fixture selected that variable row. Its stderr was `No rule to make target ../../../protocol-processor/hdl/acmp/rom/gen_ltn_rom.py`. Fix: ignore target-specific assignment rows, preserve all three prerequisite leg invocations with inert build fixtures, and grade both post-pool campaign sentinels. The interrupted attempt is not a passing gate.

The first local policy AST audit incorrectly required every historical helper to equal the old PR version even when dev intentionally changed it. It refused `_arms_host_tooling_masks`; this is an audit-script scope error, not a source failure. The corrected audit confirms every dev helper and every PR-added helper separately.

Static first pass: three Markdown gates refused absent pinned renderer packages; provisioned only repository hash-locked requirements in the separate temporary validation environment. Python idiom found one 121-character inventory banner line; split the literal without changing its value. All other static commands passed; retain original failures and final reruns.

Both builder modes exit 0. The SDK mode grades the compiler instruments; the no-compiler mode explicitly stands them down. Both declare the pre-existing utilization-report calibration arm NOT RUN because its hardware build report is absent. No hardware evidence is claimed.

Validation setup: the pinned Markdown and HDL-reference requirements were installed with hash verification in a separate temporary environment outside the evidence directory. Verilator is pinned to 5.050 through an existing read-only wrapper. Builder SDK verification and executable mapping follow the supplied runner example; no SDK file is changed. No-compiler validation makes all three RV32 candidate launches unavailable while retaining real host compiler probes.

At `f36b40ddb5bf7fa5b12bba47d136e0b9d429403c`, all 24 final static/phase commands exit 0, including 700 policy controls, 344 BDD scenarios, both documentation inventory modes, real xvlog (four existing processor findings at its unchanged ratchet), and CI checks (1647 contract items; 2188 self-test arms). Pool controls: 17/17; backpressure controls: 28/28. Both builder modes subsequently passed (SDK 669.900 s; no compiler 469.725 s). All four full-suite measurements, their equivalence check and every default sweep chunk pass.

Full default sweep inventory: 55 suites, exactly partitioned into five chunks; all six inventory commands exited 0. `sweep-inventory.json` records each command and population. The scheduled physical suite is excluded by the unchanged default selector.

| Chunk | Suites | Status |
| --- | --- | --- |
| 0/5 | `aaf_latency_tap_bank`, `avtp_stream`, `cls`, `eth_tx_reset`, `gptp_txts`, `i2spb`, `ifg`, `milan_dp_render`, `ptp`, `queues`, `rx_filter` | exit 0; 564.104 s |
| 1/5 | `aaf_latency_taps`, `avtp_rxmon`, `cbs`, `cdc`, `clkvalid`, `controller_rate`, `crf_rx`, `datapath`, `gptp_plane`, `gptp_shadow`, `lat_history_ring`, `maap`, `mac_rmon`, `media_nco`, `mmcm_servo_autorepair`, `nvm_cosim`, `pair_fill`, `pcmlpf`, `pp_shadow`, `tcam_csr`, `tsn_fuzz` | exit 0; 1412.828 s |
| 2/5 | `aaf`, `aaf_audio_loop`, `aes3`, `chmap_render`, `crf_tx`, `mmcm_servo`, `ptp_sync`, `ptp_ts`, `render_setpoint`, `shaper_core` | exit 0; 711.309 s |
| 3/5 | `adp_tx`, `avtp_parser`, `chmap_capture`, `classifier`, `csr`, `link_guard`, `media_grid_align`, `nvm_backend`, `tcam`, `tdm`, `tdm_render`, `tkdiag` | exit 0; 471.906 s |
| 4/5 | `milan_dp` | exit 0; 1279.530 s |

The original comparison gate receipt reused the comparison report filename. Its raw log retained the successful result; the complete structured report is regenerated as `benchmark-equivalence.json`, separate from gate metadata. Timed runs and source files are unchanged.

## Combined sweep result

`sweep-aggregate.json` checks exact ownership against `sweep-inventory.json`: 55 default suites, no duplicate, missing or unexpected suite logs. The combined tally is 2121993 checks with zero in-suite failures and four declared skips. `sweep-accounting.log` contains the full suite-by-suite table and skip reasons. Every chunk exits 0; no suite timed out.

| Chunk | Suites | Checks | Exit | Seconds |
| --- | --- | --- | --- | --- |
| 0/5 | 11 | 401931 | 0 | 564.104 |
| 1/5 | 21 | 173056 | 0 | 1412.828 |
| 2/5 | 10 | 1522972 | 0 | 711.309 |
| 3/5 | 12 | 13960 | 0 | 471.906 |
| 4/5 | 1 | 10074 | 0 | 1279.530 |

Commands in the gate table use `$EVIDENCE` for this handoff directory. `run-gate.py` pins the validation environment and affinity and records each subprocess exit without a pipeline. The benchmark and builder helper files retain their exact invocation setup; `tool-identity.json`, `environment.json`, `source-scope.json` and `policy-union.json` provide the corresponding identities and scope checks. Preliminary failures remain in the table with their actual exits and are resolved by the later final-head runs.

Final evidence inventory: 43 successful final-head gate invocations; 71 recorded invocations including preliminary attempts. Each has an exact head, command, exit, elapsed time, receipt and raw log. The output contains only evidence documents, logs, receipts and small validation helpers; no toolchain, SDK, installed package, virtual environment, executable prefix or tree export is included.
