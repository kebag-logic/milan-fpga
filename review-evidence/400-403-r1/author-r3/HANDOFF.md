# [A316] Round 2 handoff

Status: all required commands returned zero. Local implementation is ready for independent review.

Branch: `400-403-declaration-truth`
Initial head: `2d61e7edafa63cff7d5f8fdca9840a969ee070a6`
Current head: `7463ab0889da9a95fce7c921e386d6035d69778e`
Comparison base: `864b36f5e9450ef64f75ca3f0d68c44330e447d7`
Origin confirmed: `https://github.com/kebag-logic/milan-fpga.git`

Assignment: https://github.com/kebag-logic/milan-fpga/issues/400#issuecomment-5832912970

## Root cause

`constants_header()` maintained a handwritten subset of the firmware boot constants. The production `fabric_constants()` generator already emitted the four new MAC, TCAM, AAF and MAAP constants, but the saved-state host test never consumed it. The real firmware therefore failed to compile on the first shape. `baseline-nvm.log` reproduces all four undeclared identifiers with exit 1 at the starting head.

## Changes

- `sw/firmware/nvm_hosttest/test_nvm_firmware.py:85`: import the shared boot generator.
- `sw/firmware/nvm_hosttest/test_nvm_firmware.py:166`: build the stub header from the complete derived boot dictionary instead of copied constants.
- `sw/firmware/nvm_hosttest/test_nvm_firmware.py:221`: read both per-shape generated artifacts and derive the header from them.
- `sw/builder/test_builder.py:4467`: derive the compiler census fixture's boot words from the same generator; preserve its synthetic identity sentinels.
- `sw/builder/test_builder.py:27549`: run the firmware host self-test from the full builder entry point, across every shipped shape and all four planted defects.

The authoritative generator remains `sw/litex/boot_policy.py:35`, published by `sw/litex/milan_soc.py:3950`. No production behavior, RTL, donor pin, workflow or acceptance criterion changes in Round 2. The docs workflow already runs the firmware self-test at `.github/workflows/docs.yml:230`.

## Validation method

Commands run in the foreground with captured exit codes, without output pipelines. `run_gate.py` records full argv, checkout cwd, duration and log in `gates.jsonl`. All bank commands use this checkout, overriding the JSON bank's historical cwd. The two environment assignments are taken verbatim from the read-only bank. Simulation uses eight build jobs.

Bank 48 uses the supplied compiler-mapping wrapper with only its diagnostic JSONL destination changed to this output directory. Its original record destination already exists and is read-only. Compiler argv other than the executable remains unchanged; SDK verification runs first. The SDK itself is read-only. `full-builder-sdk-argv.jsonl` records every actual invocation. The complete no-RV32 run hides only the three cross-compiler candidates, retains host builds, and records the weaker instrument verdict explicitly.

The no-git docs mode uses `GIT_DIR=/dev/null`, making Git metadata unavailable while retaining the same source tree. The gate confirms its filesystem-walk mode. No checkout, tree export or git-metadata deletion is needed.

## Manager builder bank

Every command below is prefixed by the bank's unchanged `env PATH=... VERILATOR_ROOT=...`; exact arguments are in `gates.jsonl`. Row 44 preserves the bank's original endpoint; `diff-final` additionally checks the new head. Row 48 preserves the wrapper logic with the output-only relocation above.

| # | Command | Exit | Log |
|---|---|---|---|
| 1 | `python3 avdecc/gen_aem_store.py --self-test` | 0 | [bank-01.log](bank-01.log) |
| 2 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | [bank-02.log](bank-02.log) |
| 3 | `python3 scripts/lint_rtl.py --check --self-test` | 0 | [bank-03.log](bank-03.log) |
| 4 | `python3 scripts/suite_shards.py --selftest` | 0 | [bank-04.log](bank-04.log) |
| 5 | `python3 scripts/ci_events.py --check` | 0 | [bank-05.log](bank-05.log) |
| 6 | `python3 scripts/ci_scope.py --selftest` | 0 | [bank-06.log](bank-06.log) |
| 7 | `python3 scripts/ci_events.py --selftest` | 0 | [bank-07.log](bank-07.log) |
| 8 | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | [bank-08.log](bank-08.log) |
| 9 | `python3 scripts/check_feature_status.py` | 0 | [bank-09.log](bank-09.log) |
| 10 | `python3 scripts/check_submodule_docs.py` | 0 | [bank-10.log](bank-10.log) |
| 11 | `python3 scripts/check_cpp_idiom.py` | 0 | [bank-11.log](bank-11.log) |
| 12 | `python3 scripts/check_py_idiom.py` | 0 | [bank-12.log](bank-12.log) |
| 13 | `python3 scripts/docs_check.py` | 0 | [bank-13.log](bank-13.log) |
| 14 | `python3 scripts/check_doc_style.py` | 0 | [bank-14.log](bank-14.log) |
| 15 | `python3 scripts/check_doc_style.py --selftest` | 0 | [bank-15.log](bank-15.log) |
| 16 | `python3 scripts/check_solution_docs.py` | 0 | [bank-16.log](bank-16.log) |
| 17 | `python3 scripts/check_doc_paths.py` | 0 | [bank-17.log](bank-17.log) |
| 18 | `python3 scripts/check_archive.py` | 0 | [bank-18.log](bank-18.log) |
| 19 | `python3 scripts/gen_toc.py --verify-anchors` | 0 | [bank-19.log](bank-19.log) |
| 20 | `python3 scripts/gen_toc.py --check` | 0 | [bank-20.log](bank-20.log) |
| 21 | `python3 scripts/check_hygiene.py --check` | 0 | [bank-21.log](bank-21.log) |
| 22 | `python3 scripts/check_todo_ownership.py` | 0 | [bank-22.log](bank-22.log) |
| 23 | `python3 scripts/check_sv_idiom.py` | 0 | [bank-23.log](bank-23.log) |
| 24 | `python3 scripts/check_sh_idiom.py` | 0 | [bank-24.log](bank-24.log) |
| 25 | `python3 scripts/check_rtl_source_lists.py` | 0 | [bank-25.log](bank-25.log) |
| 26 | `python3 scripts/check_soc_sources.py` | 0 | [bank-26.log](bank-26.log) |
| 27 | `python3 scripts/check_port_contracts.py` | 0 | [bank-27.log](bank-27.log) |
| 28 | `python3 scripts/check_nvm_record_space.py` | 0 | [bank-28.log](bank-28.log) |
| 29 | `python3 scripts/check_baremetal_only.py --check` | 0 | [bank-29.log](bank-29.log) |
| 30 | `python3 scripts/check_baremetal_only.py --selftest` | 0 | [bank-30.log](bank-30.log) |
| 31 | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | [bank-31.log](bank-31.log) |
| 32 | `python3 scripts/check_sweep_shape.py --self-test` | 0 | [bank-32.log](bank-32.log) |
| 33 | `python3 scripts/xvlog_gate.py --check` | 0 | [bank-33.log](bank-33.log) |
| 34 | `python3 scripts/measure_control_flow.py --selftest` | 0 | [bank-34.log](bank-34.log) |
| 35 | `python3 scripts/measure_cohesion.py --selftest` | 0 | [bank-35.log](bank-35.log) |
| 36 | `python3 scripts/check_em_dash.py --base 864b36f5e9450ef64f75ca3f0d68c44330e447d7` | 0 | [bank-36.log](bank-36.log) |
| 37 | `python3 scripts/measure_fail_fast.py --check` | 0 | [bank-37.log](bank-37.log) |
| 38 | `python3 scripts/measure_test_evidence.py --check` | 0 | [bank-38.log](bank-38.log) |
| 39 | `python3 scripts/measure_naming.py --check` | 0 | [bank-39.log](bank-39.log) |
| 40 | `python3 scripts/measure_test_evidence.py --selftest` | 0 | [bank-40.log](bank-40.log) |
| 41 | `python3 scripts/gen_toc.py --selftest` | 0 | [bank-41.log](bank-41.log) |
| 42 | `python3 scripts/check_em_dash.py --selftest` | 0 | [bank-42.log](bank-42.log) |
| 43 | `python3 scripts/docs_check.py --selftest` | 0 | [bank-43.log](bank-43.log) |
| 44 | `git diff --check 864b36f5e9450ef64f75ca3f0d68c44330e447d7 2d61e7edafa63cff7d5f8fdca9840a969ee070a6` | 0 | [bank-44.log](bank-44.log) |
| 45 | `python3 scripts/check_wire_accountability.py --self-test` | 0 | [bank-45.log](bank-45.log) |
| 46 | `python3 scripts/check_entity_shape.py --self-test` | 0 | [bank-46.log](bank-46.log) |
| 47 | `python3 scripts/check_deploy_shape.py --self-test` | 0 | [bank-47.log](bank-47.log) |
| 48 | `python3 -u $VALIDATION_STORAGE/400-403-manager-r1/full-builder-sdk.py` | 0 | [bank-48.log](bank-48.log) |

## Additional gates and chunked datapath sweep

The original `run` recipe is copied verbatim into `dp-chunks.mk`, split only at recipe-command boundaries. `dp-prereq` retains every original prerequisite, including the three directed runs. Steps 1 through 35 execute every default command in order, including both mutation campaigns. `run_rtl.py` records each command separately and stops on a nonzero exit. The four NxN builds/run legs exercise the bundle's output-indexed offsets.

| Gate | Command | Exit | Seconds | Log |
|---|---|---|---|---|
| csr | `make -C tb/verilator/csr` | 0 | 15.16 | [csr.log](csr.log) |
| pp-shadow | `make -C tb/verilator/pp_shadow` | 0 | 19.76 | [pp-shadow.log](pp-shadow.log) |
| declarations | `python3 sw/builder/test_declarations.py` | 0 | 0.52 | [declarations.log](declarations.log) |
| docs-git | `python3 -B scripts/docs_check.py` | 0 | 4.17 | [docs-git.log](docs-git.log) |
| docs-no-git | `env GIT_DIR=/dev/null python3 -B scripts/docs_check.py` | 0 | 4.12 | [docs-no-git.log](docs-no-git.log) |
| behave | `bash -c 'cd tests && behave --no-capture -f plain'` | 0 | 1.17 | [behave.log](behave.log) |
| diff-worktree | `git diff --check` | 0 | 0.06 | [diff-worktree.log](diff-worktree.log) |
| ooc-base | `env OOC_TMP=$VALIDATION_STORAGE/400-403-a316-ooc/base-results bash $OUTPUT/ooc-base.sh milan_csr KL_pp_shadow milan_datapath` | 1 | 0.62 | [ooc-base.log](ooc-base.log) |
| dp-prereq | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-prereq` | 0 | 87.49 | [dp-prereq.log](dp-prereq.log) |
| dp-01 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-01` | 0 | 0.16 | [dp-01.log](dp-01.log) |
| dp-02 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-02` | 0 | 0.21 | [dp-02.log](dp-02.log) |
| dp-03 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-03` | 0 | 3.32 | [dp-03.log](dp-03.log) |
| dp-04 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-04` | 0 | 0.16 | [dp-04.log](dp-04.log) |
| dp-05 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-05` | 0 | 0.21 | [dp-05.log](dp-05.log) |
| dp-06 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-06` | 0 | 0.16 | [dp-06.log](dp-06.log) |
| dp-07 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-07` | 0 | 0.16 | [dp-07.log](dp-07.log) |
| dp-08 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-08` | 0 | 0.21 | [dp-08.log](dp-08.log) |
| dp-09 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-09` | 0 | 0.16 | [dp-09.log](dp-09.log) |
| dp-10 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-10` | 0 | 0.11 | [dp-10.log](dp-10.log) |
| dp-11 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-11` | 0 | 0.16 | [dp-11.log](dp-11.log) |
| dp-12 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-12` | 0 | 0.16 | [dp-12.log](dp-12.log) |
| dp-13 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-13` | 0 | 5.48 | [dp-13.log](dp-13.log) |
| dp-14 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-14` | 0 | 0.11 | [dp-14.log](dp-14.log) |
| dp-15 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-15` | 0 | 15.0 | [dp-15.log](dp-15.log) |
| dp-16 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-16` | 0 | 0.12 | [dp-16.log](dp-16.log) |
| dp-17 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-17` | 0 | 25.43 | [dp-17.log](dp-17.log) |
| dp-18 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-18` | 0 | 16.26 | [dp-18.log](dp-18.log) |
| dp-19 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-19` | 0 | 0.11 | [dp-19.log](dp-19.log) |
| dp-20 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-20` | 0 | 16.35 | [dp-20.log](dp-20.log) |
| dp-21 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-21` | 0 | 34.47 | [dp-21.log](dp-21.log) |
| dp-22 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-22` | 0 | 0.11 | [dp-22.log](dp-22.log) |
| dp-23 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-23` | 0 | 16.5 | [dp-23.log](dp-23.log) |
| dp-24 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-24` | 0 | 0.11 | [dp-24.log](dp-24.log) |
| diff-final | `git diff --check 864b36f5e9450ef64f75ca3f0d68c44330e447d7 HEAD` | 0 | 0.03 | [diff-final.log](diff-final.log) |
| dp-25 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-25` | 0 | 5.32 | [dp-25.log](dp-25.log) |
| dp-26 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-26` | 0 | 0.11 | [dp-26.log](dp-26.log) |
| em-dash-final | `python3 scripts/check_em_dash.py --base 864b36f5e9450ef64f75ca3f0d68c44330e447d7` | 0 | 3.18 | [em-dash-final.log](em-dash-final.log) |
| dp-27 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-27` | 0 | 0.72 | [dp-27.log](dp-27.log) |
| dp-28 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-28` | 0 | 0.11 | [dp-28.log](dp-28.log) |
| dp-29 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-29` | 0 | 6.06 | [dp-29.log](dp-29.log) |
| dp-30 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-30` | 0 | 0.11 | [dp-30.log](dp-30.log) |
| ooc-base-r2 | `env OOC_TMP=$VALIDATION_STORAGE/400-403-a316-ooc/base-results bash $OUTPUT/ooc-base.sh milan_csr KL_pp_shadow milan_datapath` | 0 | 544.29 | [ooc-base-r2.log](ooc-base-r2.log) |
| dp-31 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-31` | 0 | 454.75 | [dp-31.log](dp-31.log) |
| dp-32 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-32` | 0 | 0.11 | [dp-32.log](dp-32.log) |
| dp-33 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-33` | 0 | 356.89 | [dp-33.log](dp-33.log) |
| dp-34 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-34` | 0 | 0.11 | [dp-34.log](dp-34.log) |
| dp-35 | `make -C tb/verilator/milan_dp -f Makefile -f $OUTPUT/dp-chunks.mk a316-step-35` | 0 | 148.14 | [dp-35.log](dp-35.log) |
| ooc-head-r2 | `env OOC_TMP=$VALIDATION_STORAGE/400-403-a316-ooc/head-results bash $OUTPUT/ooc-head.sh milan_csr KL_pp_shadow milan_datapath` | 0 | 588.77 | [ooc-head-r2.log](ooc-head-r2.log) |
| builder-no-rv32 | `python3 -u $OUTPUT/no-rv32-builder.py` | 0 | 540.55 | [builder-no-rv32.log](builder-no-rv32.log) |

## Area measurement

Round 2 changes no RTL. The bundle changes `milan_csr`, `KL_pp_shadow`, and `milan_datapath`. The before/after replay uses the repository `syn/yosys/ooc.sh` recipe (`synth_xilinx -family xc7 -flatten`) at its default generated shape. The replay adds only the CSR target entry, which the stock area list omits, and redirects the script's root/helper paths to this checkout.

The base arm substitutes only the ten changed RTL/header blobs from the comparison base; the remaining inputs and pinned submodules are identical. These sparse inputs and generated synthesis artifacts live under `$VALIDATION_STORAGE/400-403-a316-ooc`, outside the output directory. No other checkout is created. `ooc-inputs.txt`, `ooc-base.sh` and `ooc-head.sh` record the exact replay. The first local wrapper attempt failed before synthesis because of incorrect path escaping; `ooc-base.log` is retained, and the corrected rerun is recorded separately.

| Module | LUT | LUTRAM | LUT total | FF | RAMB36 | RAMB18 | DSP | CARRY4 |
|---|---|---|---|---|---|---|---|---|
| milan_csr | 4236 | 0 | 4236 | 3573 | 0 | 2 | 0 | 43 |
| KL_pp_shadow | 60855 | 6136 | 66991 | 30187 | 15 | 4 | 6 | 2104 |
| milan_datapath | 90179 | 6640 | 96819 | 43424 | 17 | 20 | 15 | 3614 |

All before/after entries are identical; every reported area delta is zero.

This is mapped default-shape area, not placed utilization or timing.


## Delivery and limits

No push, PR creation/edit, merge, sub-agent, other checkout, hardware access or donor edit was performed. `PR-BODY-original.md` preserves the body read with `gh pr view 566 --json body`; `PR-BODY.md` is the updated reviewable local body. The two closing lines are retained. Independent review and remote validation remain the manager's next steps.

## Coverage notes

The pinned builder run executed 855 mapped compiler invocations and all five recipe elaborations. It reports one unrun historical placed-utilization calibration arm because the old report is absent. The compiler-absent run deliberately leaves compiler-dependent instruments unmeasured; it is not equivalent evidence to the pinned run. Both documentation inventory modes passed. The no-git mode deliberately skips Git inventory parity. The source-analysis gates retain their existing ratchets: 90 lint findings and four pinned-processor front-end findings, with no new findings.

Review-ready issue comment: https://github.com/kebag-logic/milan-fpga/issues/400#issuecomment-5833383739
