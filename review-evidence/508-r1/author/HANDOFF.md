# [A295] Issue #508 round 2 handoff

Status: assignment items 1-3 complete. All 65 required gate commands returned rc 0 at final head `6a9828c172aa4d5d8ee49725e357a10bae2caa52`, from cleared generated outputs. The superproject and all three required submodules are clean. Independent review remains pending.

Starting branch: `508-pp-pin-adopt`.
Starting head: `35f0695815c202392b6b4806bb9f59dd110687ed`.
Requested merge base: `c266432dcb0cdd464205823a3d82cad260eedde2`.
Requested processor pin: `990f96526bb89356c963a260ebbdcf2a77e6623a`.
Scope: assignment items 1-3 only; no push or PR operations.

## Merge resolution per file

Merge commit: `cec6b99da7b26ce9962bcf9a6c05161c9f99439a` (parents: starting head and requested dev). Both requested fetches completed before the merge and processor checkout.

| File | Resolution |
|---|---|
| CHANGELOG.md | Both unreleased sections and both contents entries retained. |
| docs/testing/TESTING.md | Both GSI and GM-step campaign rows retained. |
| scripts/measure_test_evidence.py | Both campaign dispositions retained; processor dispositions from round 1 retained. No ratchet or identity changed. |
| tb/verilator/milan_dp/Makefile | Union of target help and PHONY entries, retaining notify/GSI and GM-step/option-off targets; default sweep retains GM-step and its three controls. |
| tb/verilator/milan_dp/README.md | Both seam and GM-step sections retained; current GM-step contents description; one row per leg, with both branches' historical measurements explicitly distinguished. |

No remote `508-review-evidence` branch was advertised. Round-1 evidence was read from issue comment 5822002238. Public assignment names independent reviewers [R306] and [R307]; the old issue body and project still say Backlog, but the later explicit assignment authorizes this continuation.

## Adopted processor changes

| Processor issues | Merged PR | Adopted behavior |
|---|---|---|
| [92](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/92), [93](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/93) | [109](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/109) | Saved-binding restore, bounded walk, listener boot hold |
| [94](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/94) | [110](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/110) | Descriptor-memory guard; no external port change |
| [43](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/43), [49](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/49) | [111](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/111) | Processor-owned input probing, ACMP status and failure fields |
| [112](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/112) | [114](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/114) | Admission grants wait for the current declaration's evaluation |
| [116](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/116) | [117](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/117) | Parent-gate fixes; no behavior or external port change |
| [113](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/113) | [115](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/115) | Latency-only GET_STREAM_INFO notification; no external port change |

PR 117 merged at `265d6762a58d9d9e545624d6d3f1a34e7006d171`; PR 115 merged at the adopted pin `990f96526bb89356c963a260ebbdcf2a77e6623a`.

Latency visibility: no existing parent notify/[GSI] check drives a latency-only refresh. `sim_nxn.cpp:gsi_talker_failed` fixes latency at 500000 ns. G5's initial registration changes latency together with registration/failure fields, and its exact-count assertion observes the coalesced notification. G6 repeats the same value; G7 changes only FailureInformation. Earlier notify phases send no registering Talker attribute. No assertion needs adaptation, and no independent parent latency-only coverage is claimed. The processor PR 115 response tests own that coverage.

## ROM digests

Required command: `cd syn/yosys && ./ooc.sh --record-rom-digests`.
Result: rc 0; two new pin rows, identical image hashes to a8f8ce81. No manual digest edits.

## Gate table

| Gate | Result | Evidence |
|---|---|---|
| Full builder, pinned SDK | rc 0 on final head; one historical resource-calibration arm NOT RUN | `builder-sdk-candidate.log`; `full-builder-sdk-candidate-argv.jsonl` |
| Full builder, no compiler | rc 0 on final head; compiled census and historical resource calibration NOT RUN | `builder-absent-candidate.log`; `full-builder-absent-argv.jsonl` |
| pp_shadow | rc 0; 371 checks, 0 failures | `pp-shadow.log` |
| milan_dp default sweep chunks | 36/36 commands rc 0; chunks 1-12, 13-23, 24-30, 31-36 all rc 0 | `milan-dp-chunks.json`, `milan-dp-commands.json`, `dp-01.log` through `dp-36.log` |
| milan_dp_render | rc 0; integration legs 152/0 and 60/0; 5/5 built-in control/defect checks | `milan-dp-render.log` |
| nvm_cosim | rc 0; 465/465 checks, 39/39 mutants caught by named checks | `nvm-cosim.log` |
| gsi-mutants | rc 0; 8/8 including golden control and seven named mutant detections | `gsi-mutants.log` |
| Yosys shards 0/4, 1/4, 2/4, 3/4 | all rc 0; 1 + 1 + 26 + 26 = 54/54 full synthesis tops; tied-input and tap-purity checks pass | `yosys-0.log` through `yosys-3.log`; `yosys-results/`; `yosys-inventory.json` |
| behave | rc 0; 14 features, 344 scenarios, 1739 steps, no failures/skips | `behave.log` |
| Source, documentation, idiom, naming, evidence and contract checks | rc 0 on final head | `*-final.log`; all 18 commands |
| git diff --check | rc 0 | `diff-check-final.log` |

## Final state

Final head: `6a9828c172aa4d5d8ee49725e357a10bae2caa52`.
Processor gitlink: `990f96526bb89356c963a260ebbdcf2a77e6623a`.
Remote branch remains `35f0695815c202392b6b4806bb9f59dd110687ed`; no push or PR operation occurred.

Round-2 commits, oldest first, each verified to contain exactly one subject line and no body or trailers:

| Commit | Subject |
|---|---|
| `cec6b99da7b26ce9962bcf9a6c05161c9f99439a` | Merge dev c266432d into processor pin adoption lane |
| `e9f8ea5aa06515bbc86cfaded7f5bd24ad10c5b4` | Adopt processor parent-gate fixes and latency notification at 990f9652 |
| `ee8812c938450aa764f657e738e092e6c6894696` | Regenerate the processor pin diagram and raster manifest |
| `6a9828c172aa4d5d8ee49725e357a10bae2caa52` | Keep the GM-step measurement attributed to the dev branch |

`completion-check.json` records the final audit: 65 required command receipts, all rc 0 and all at the final head, the complete 54-top synthesis inventory, clean superproject/submodules, 471 audited pinned-compiler invocations, and three intentionally unavailable cross-compiler candidates in the absent mode. `git diff --check` also passes over the entire requested-base-to-head diff. The historical intermediate-head builder receipts are superseded by `builder-sdk-candidate.log` and `builder-absent-candidate.log`.

Public review-ready comment: https://github.com/kebag-logic/milan-fpga/issues/508#issuecomment-5825445388. Posted as the final task action; stopped after publication.
Independent reviews, branch publication, hosted candidate checks and merge remain outside this assignment.

## Reproduction and evidence limits

All gate commands ran synchronously in the foreground with a six-hour per-command timeout and direct file logging, without shell pipelines. `gates.jsonl` records each exact argv, cwd, head, duration and exit; the ledger below links the raw output. `$EVIDENCE` means this handoff's directory. `run_gate.py` records the environment additions needed to reproduce the receipts.

The SDK builder uses the same argv[0]-only compiler mapping as `$VALIDATION_STORAGE/408-manager-r7/full-builder-sdk.py`, after verifying the pinned SDK installation. `full-builder-sdk-candidate.py` runs the entire builder with `--require-rv32` and audits all 471 mapped invocations, preserving arguments and subprocess options. The compiler-absent run executes the entire builder again after removing generated builder output; `full-builder-absent.py` makes only the three cross-compiler candidates unavailable and preserves host probes. The audits confirm all three candidates were unavailable and no cross compiler ran.

Both full-builder commands return 0. The SDK run reports one NOT RUN arm: historical resource calibration, which requires an absent placement report. The compiler-absent run reports that arm plus the compiled census/instruments arm as NOT RUN. These are existing builder dispositions; no pass is claimed for an unexecuted arm and no gate was weakened.

The default datapath sweep was expanded from `make --no-print-directory -n run` after clean. Only informational echoes were omitted; all 36 actual recipe commands ran in order, with four chunk exits recorded in `milan-dp-chunks.json`. The notify leg remains 345/0, GM-step 48/0, option-off 234/0, and the NXN family 1709/0, 1711/0, 3137/0 and 1709/0. The default render mutation and GM-step control campaigns report 6/6 and 4/4 respectively.

Documentation checks ran with the Git inventory and with `GIT_DIR=/nonexistent-508-a295-git` to exercise the filesystem fallback used without Git metadata. Both pass; the fallback has the expected inventory-parity skip. Port-contract findings remain 111/111 previously allowed identities, naming remains 96/96, and test-evidence reports 76 <= 77 mutation arms and 3 <= 3 wall-clock identities. No identity or budget was added. Its self-test reports 101/101. The installed HDL frontend ran: zero root findings, four retained processor findings, no new findings.

The pinned converter and Markdown dependencies were placed under `$VALIDATION_STORAGE/508-a295-tools`; the SDK and installed simulator remained in their existing locations. This output directory contains evidence and small reproduction scripts only, with no toolchain, SDK copy, virtual environment or tree export.

## Live command ledger

<!-- gates:start -->
| Command | Exit | Seconds | Log |
|---|---|---|---|
| `clean-start (complete argv in linked log)` (cwd `.`) | 0 | 0.62 | [clean-start.log](clean-start.log) |
| `python3 -c import subprocess; [subprocess.run(a,check=True) for a in [["verilator","--version"],["yosys","-V"],["sv2v","--version"],["git","rev-parse","HEAD"],["git","status","--short"]]]` (cwd `.`) | 0 | 0.16 | [tool-identities.log](tool-identities.log) |
| `python3 scripts/pp_srcs.py --check --selftest` (cwd `.`) | 0 | 0.26 | [pp-srcs.log](pp-srcs.log) |
| `python3 scripts/docs_check.py` (cwd `.`) | 0 | 4.08 | [docs-git.log](docs-git.log) |
| `env GIT_DIR=/nonexistent-508-a295-git python3 scripts/docs_check.py` (cwd `.`) | 0 | 4.07 | [docs-no-git.log](docs-no-git.log) |
| `python3 scripts/check_em_dash.py --base c266432dcb0cdd464205823a3d82cad260eedde2` (cwd `.`) | 2 | 0.87 | [em-dash.log](em-dash.log) |
| `python3 scripts/check_doc_style.py` (cwd `.`) | 0 | 0.06 | [doc-style.log](doc-style.log) |
| `python3 scripts/gen_toc.py --check` (cwd `.`) | 2 | 0.11 | [toc.log](toc.log) |
| `python3 scripts/check_doc_paths.py` (cwd `.`) | 0 | 0.11 | [doc-paths.log](doc-paths.log) |
| `python3 docs/traceability/gen_module_matrix.py --check` (cwd `.`) | 0 | 0.97 | [module-matrix.log](module-matrix.log) |
| `python3 $EVIDENCE/full-builder-sdk.py` (cwd `.`) | 0 | 528.73 | [builder-sdk.log](builder-sdk.log) |
| `python3 scripts/check_em_dash.py --base c266432dcb0cdd464205823a3d82cad260eedde2` (cwd `.`) | 0 | 3.17 | [em-dash-ready.log](em-dash-ready.log) |
| `python3 scripts/gen_toc.py --check` (cwd `.`) | 0 | 2.52 | [toc-ready.log](toc-ready.log) |
| `python3 docs/diagrams/submodule_boundaries.gen.py --check` (cwd `.`) | 0 | 0.36 | [diagram-check.log](diagram-check.log) |
| `python3 scripts/check_diagram_pngs.py` (cwd `.`) | 0 | 0.36 | [diagram-png.log](diagram-png.log) |
| `python3 scripts/check_submodule_docs.py` (cwd `.`) | 0 | 0.41 | [submodule-docs.log](submodule-docs.log) |
| `python3 scripts/xvlog_gate.py --check` (cwd `.`) | 0 | 139.4 | [xvlog.log](xvlog.log) |
| `python3 scripts/check_rtl_source_lists.py` (cwd `.`) | 0 | 1.42 | [rtl-lists.log](rtl-lists.log) |
| `python3 scripts/check_cpp_idiom.py` (cwd `.`) | 0 | 1.22 | [cpp-idiom.log](cpp-idiom.log) |
| `python3 scripts/check_py_idiom.py` (cwd `.`) | 0 | 3.07 | [py-idiom.log](py-idiom.log) |
| `python3 scripts/check_port_contracts.py` (cwd `.`) | 0 | 2.32 | [port-contracts.log](port-contracts.log) |
| `python3 scripts/measure_naming.py --check` (cwd `.`) | 0 | 0.46 | [naming.log](naming.log) |
| `python3 scripts/measure_test_evidence.py --check` (cwd `.`) | 0 | 5.17 | [test-evidence.log](test-evidence.log) |
| `python3 scripts/measure_test_evidence.py --selftest` (cwd `.`) | 0 | 5.17 | [test-evidence-selftest.log](test-evidence-selftest.log) |
| `python3 scripts/lint_rtl.py --check` (cwd `.`) | 0 | 6.02 | [rtl-lint.log](rtl-lint.log) |
| `git diff --check` (cwd `.`) | 0 | 0.02 | [diff-check.log](diff-check.log) |
| `python3 scripts/pp_srcs.py --check --selftest` (cwd `.`) | 0 | 0.21 | [pp-srcs-final.log](pp-srcs-final.log) |
| `python3 scripts/docs_check.py` (cwd `.`) | 0 | 4.07 | [docs-git-final.log](docs-git-final.log) |
| `env GIT_DIR=/nonexistent-508-a295-git python3 scripts/docs_check.py` (cwd `.`) | 0 | 4.07 | [docs-no-git-final.log](docs-no-git-final.log) |
| `python3 scripts/check_em_dash.py --base c266432dcb0cdd464205823a3d82cad260eedde2` (cwd `.`) | 0 | 3.22 | [em-dash-final.log](em-dash-final.log) |
| `python3 scripts/check_doc_style.py` (cwd `.`) | 0 | 0.06 | [doc-style-final.log](doc-style-final.log) |
| `python3 scripts/gen_toc.py --check` (cwd `.`) | 0 | 2.42 | [toc-final.log](toc-final.log) |
| `python3 scripts/check_doc_paths.py` (cwd `.`) | 0 | 0.06 | [doc-paths-final.log](doc-paths-final.log) |
| `python3 docs/traceability/gen_module_matrix.py --check` (cwd `.`) | 0 | 0.97 | [module-matrix-final.log](module-matrix-final.log) |
| `python3 scripts/xvlog_gate.py --check` (cwd `.`) | 0 | 139.9 | [xvlog-final.log](xvlog-final.log) |
| `python3 scripts/check_rtl_source_lists.py` (cwd `.`) | 0 | 1.37 | [rtl-lists-final.log](rtl-lists-final.log) |
| `python3 scripts/check_cpp_idiom.py` (cwd `.`) | 0 | 1.22 | [cpp-idiom-final.log](cpp-idiom-final.log) |
| `python3 scripts/check_py_idiom.py` (cwd `.`) | 0 | 3.22 | [py-idiom-final.log](py-idiom-final.log) |
| `python3 scripts/check_port_contracts.py` (cwd `.`) | 0 | 2.27 | [port-contracts-final.log](port-contracts-final.log) |
| `python3 scripts/measure_naming.py --check` (cwd `.`) | 0 | 0.46 | [naming-final.log](naming-final.log) |
| `python3 scripts/measure_test_evidence.py --check` (cwd `.`) | 0 | 5.12 | [test-evidence-final.log](test-evidence-final.log) |
| `python3 scripts/measure_test_evidence.py --selftest` (cwd `.`) | 0 | 5.17 | [test-evidence-selftest-final.log](test-evidence-selftest-final.log) |
| `python3 scripts/lint_rtl.py --check` (cwd `.`) | 0 | 6.15 | [rtl-lint-final.log](rtl-lint-final.log) |
| `git diff --check` (cwd `.`) | 0 | 0.02 | [diff-check-final.log](diff-check-final.log) |
| `make -C tb/verilator/pp_shadow` (cwd `.`) | 0 | 17.81 | [pp-shadow.log](pp-shadow.log) |
| `python3 ../../../protocol-processor/hdl/acmp/rom/gen_ltn_rom.py -o ltn_rom.hex` (cwd `tb/verilator/milan_dp`) | 0 | 0.06 | [dp-01.log](dp-01.log) |
| `python3 ../../../protocol-processor/hdl/aecp/ucode/gen_ucode.py -o ucode.hex` (cwd `tb/verilator/milan_dp`) | 0 | 0.06 | [dp-02.log](dp-02.log) |
| `python3 ../../../gptp-processor/hdl/ucode/gen_gptp_ucode.py --clk-hz 2000000 --cease-ms 3000 -o gptp_ucode.hex` (cwd `tb/verilator/milan_dp`) | 0 | 0.11 | [dp-03.log](dp-03.log) |
| `python3 gen_divergent_shape.py` (cwd `tb/verilator/milan_dp`) | 0 | 0.11 | [dp-04.log](dp-04.log) |
| `dp-05 (complete argv in linked log)` (cwd `tb/verilator/milan_dp`) | 0 | 14.34 | [dp-05.log](dp-05.log) |
| `./obj_gptp/Vmilan_dp_gptp` (cwd `tb/verilator/milan_dp`) | 0 | 86.44 | [dp-06.log](dp-06.log) |
| `dp-07 (complete argv in linked log)` (cwd `tb/verilator/milan_dp`) | 0 | 14.6 | [dp-07.log](dp-07.log) |
| `./ooc.sh --record-rom-digests` (cwd `syn/yosys`) | 0 | 0.51 | [rom-digests.log](rom-digests.log) |
| `python3 $EVIDENCE/full-builder-sdk.py` (cwd `.`) | 0 | 545.96 | [builder-sdk-final.log](builder-sdk-final.log) |
| `./obj_gptplat/Vmilan_dp_gptplat` (cwd `tb/verilator/milan_dp`) | 0 | 87.21 | [dp-08.log](dp-08.log) |
| `python3 ../../../sw/builder/endstation_builder.py ../../../configs/endstation_ax7101_1x1_tdm8.yaml -o obj_gmstep/aem-build` (cwd `tb/verilator/milan_dp`) | 0 | 0.21 | [dp-09.log](dp-09.log) |
| `python3 ../../../avdecc/gen_aemi_image.py --overlay obj_gmstep/aem-build/endstation_ax7101_1x1_tdm8/aem_overlay.json --line-bytes 576 -o obj_gmstep/aemi.bin` (cwd `tb/verilator/milan_dp`) | 0 | 0.06 | [dp-10.log](dp-10.log) |
| `dp-11 (complete argv in linked log)` (cwd `tb/verilator/milan_dp`) | 0 | 13.95 | [dp-11.log](dp-11.log) |
| `clean-builder-sdk (complete argv in linked log)` (cwd `.`) | 0 | 0.11 | [clean-builder-sdk.log](clean-builder-sdk.log) |
| `./obj_gmstep/Vmilan_dp_gmstep obj_gmstep/aemi.bin 0` (cwd `tb/verilator/milan_dp`) | 0 | 23.87 | [dp-12.log](dp-12.log) |
| `dp-13 (complete argv in linked log)` (cwd `tb/verilator/milan_dp`) | 0 | 13.19 | [dp-13.log](dp-13.log) |
| `dp-14 (complete argv in linked log)` (cwd `tb/verilator/milan_dp`) | 0 | 16.0 | [dp-14.log](dp-14.log) |
| `dp-15 (complete argv in linked log)` (cwd `tb/verilator/milan_dp`) | 0 | 16.6 | [dp-15.log](dp-15.log) |
| `dp-16 (complete argv in linked log)` (cwd `tb/verilator/milan_dp`) | 0 | 16.8 | [dp-16.log](dp-16.log) |
| `dp-17 (complete argv in linked log)` (cwd `tb/verilator/milan_dp`) | 0 | 13.69 | [dp-17.log](dp-17.log) |
| `dp-18 (complete argv in linked log)` (cwd `tb/verilator/milan_dp`) | 0 | 13.14 | [dp-18.log](dp-18.log) |
| `dp-19 (complete argv in linked log)` (cwd `tb/verilator/milan_dp`) | 0 | 13.29 | [dp-19.log](dp-19.log) |
| `dp-20 (complete argv in linked log)` (cwd `tb/verilator/milan_dp`) | 0 | 14.3 | [dp-20.log](dp-20.log) |
| `dp-21 (complete argv in linked log)` (cwd `tb/verilator/milan_dp`) | 0 | 12.99 | [dp-21.log](dp-21.log) |
| `dp-22 (complete argv in linked log)` (cwd `tb/verilator/milan_dp`) | 0 | 14.24 | [dp-22.log](dp-22.log) |
| `dp-23 (complete argv in linked log)` (cwd `tb/verilator/milan_dp`) | 0 | 14.9 | [dp-23.log](dp-23.log) |
| `./obj_dir/Vmilan_dp_sim` (cwd `tb/verilator/milan_dp`) | 0 | 5.32 | [dp-24.log](dp-24.log) |
| `./obj_notify/Vmilan_dp_notify` (cwd `tb/verilator/milan_dp`) | 0 | 14.84 | [dp-25.log](dp-25.log) |
| `./obj_crflic/Vmilan_dp_crflic` (cwd `tb/verilator/milan_dp`) | 0 | 25.01 | [dp-26.log](dp-26.log) |
| `./obj_nxn/Vmilan_dp_nxn` (cwd `tb/verilator/milan_dp`) | 0 | 6.32 | [dp-27.log](dp-27.log) |
| `./obj_nxndv/Vmilan_dp_nxndv` (cwd `tb/verilator/milan_dp`) | 0 | 6.37 | [dp-28.log](dp-28.log) |
| `./obj_nxn8/Vmilan_dp_nxn8` (cwd `tb/verilator/milan_dp`) | 0 | 12.24 | [dp-29.log](dp-29.log) |
| `./obj_nxn4c/Vmilan_dp_nxn4c` (cwd `tb/verilator/milan_dp`) | 0 | 6.48 | [dp-30.log](dp-30.log) |
| `./obj_nolpf/Vmilan_dp_nolpf` (cwd `tb/verilator/milan_dp`) | 0 | 5.37 | [dp-31.log](dp-31.log) |
| `./obj_prune/Vmilan_dp_prune` (cwd `tb/verilator/milan_dp`) | 0 | 0.67 | [dp-32.log](dp-32.log) |
| `./obj_ax1x1/Vmilan_dp_ax1x1` (cwd `tb/verilator/milan_dp`) | 0 | 6.08 | [dp-33.log](dp-33.log) |
| `python3 -c import subprocess; [subprocess.run(a,check=True) for a in [["verilator","--version"],["yosys","-V"],["sv2v","--version"],["git","rev-parse","HEAD"],["git","status","--short"]]]` (cwd `.`) | 0 | 0.16 | [tool-identities-final.log](tool-identities-final.log) |
| `python3 $EVIDENCE/full-builder-sdk-candidate.py` (cwd `.`) | 0 | 540.51 | [builder-sdk-candidate.log](builder-sdk-candidate.log) |
| `clean-builder-absent (complete argv in linked log)` (cwd `.`) | 0 | 0.06 | [clean-builder-absent.log](clean-builder-absent.log) |
| `./obj_aclk/Vmilan_dp_aclk` (cwd `tb/verilator/milan_dp`) | 0 | 450.31 | [dp-34.log](dp-34.log) |
| `python3 $EVIDENCE/full-builder-absent.py` (cwd `.`) | 0 | 433.46 | [builder-absent-candidate.log](builder-absent-candidate.log) |
| `python3 render_mutants.py` (cwd `tb/verilator/milan_dp`) | 0 | 348.17 | [dp-35.log](dp-35.log) |
| `python3 gmstep_mutants.py` (cwd `tb/verilator/milan_dp`) | 0 | 139.43 | [dp-36.log](dp-36.log) |
| `make -C tb/verilator/milan_dp_render` (cwd `.`) | 0 | 325.9 | [milan-dp-render.log](milan-dp-render.log) |
| `make -C tb/verilator/nvm_cosim` (cwd `.`) | 0 | 353.37 | [nvm-cosim.log](nvm-cosim.log) |
| `make -C tb/verilator/milan_dp gsi-mutants` (cwd `.`) | 0 | 227.52 | [gsi-mutants.log](gsi-mutants.log) |
| `behave --no-capture -f plain` (cwd `tests`) | 0 | 1.17 | [behave.log](behave.log) |
| `syn/yosys/run.sh --shard 0/4 --results $EVIDENCE/yosys-results` (cwd `.`) | 0 | 348.47 | [yosys-0.log](yosys-0.log) |
| `syn/yosys/run.sh --shard 1/4 --results $EVIDENCE/yosys-results` (cwd `.`) | 0 | 181.97 | [yosys-1.log](yosys-1.log) |
| `syn/yosys/run.sh --shard 2/4 --results $EVIDENCE/yosys-results` (cwd `.`) | 0 | 86.93 | [yosys-2.log](yosys-2.log) |
| `syn/yosys/run.sh --shard 3/4 --results $EVIDENCE/yosys-results` (cwd `.`) | 0 | 71.71 | [yosys-3.log](yosys-3.log) |
| `python3 $EVIDENCE/verify-completion.py` (cwd `.`) | 0 | 0.11 | [completion.log](completion.log) |
<!-- gates:end -->

Diagram regeneration: `python3 docs/diagrams/submodule_boundaries.gen.py`, rc 0. Editable master changes only the processor pin. SVG/PNG and manifest regenerated; PNG decoded and visually inspected.

Initial setup receipts: em-dash and contents checks returned 2 until the pinned Markdown dependency was installed outside this evidence directory. The first xvlog command itself returned 0; the temporary receipt runner then failed to remove a shared progress file. Per-command progress files fixed the runner. All 18 small gates were rerun on the final head and returned 0.

## Acceptance evidence

| Criterion | Evidence and scope |
|---|---|
| 1: adopted interface and lineage | SUBMODULES adoption table and the datapath suite seam table. Processor pin 990f9652 serves input selectors 5/7 internally and replaces selector 4's failure-code byte. No new external port. |
| 2: listener states | Final notify run `dp-25.log`: G0 DISABLED; G1 ACTIVE/0 immediately on bind; G2 ACTIVE/7 after timeout and ACTIVE/3 on the other sink's refused probe; G3 PASSIVE/0 at retry; G4 COMPLETED/0 after settle. The original issue says PASSIVE after bind; the existing round-1 public note explains ACTIVE first under the adopted processor contract. No state oracle changed in round 2. |
| 3: sink-specific failure information | G5 two distinct full bridge IDs/codes; G6 unchanged refresh; G7 replacement on sink 1 only; G8 withdrawal; G0 missing descriptor; G10 reset. Final notify leg: 345 checks, zero failures. |
| 4: response/notification consistency | `gsi_ck_pushes` requires one notification to each registered controller and body equality with solicited responses. G6 and duplicate probe stay silent. G9 STOP_STREAMING excludes its requester. Latency-only coverage remains in the processor tests, as explained above. |
| 5: negative controls and existing status | Final GSI mutation campaign: golden plus seven mutants, 8/8. Each mutant fails its named property (7 to 30 failed assertions out of 345). Existing output/SRP coverage passed in the 36-command default sweep. No assertions changed. |
| 6: authoritative documentation | Integration guide, register map, troubleshooting, compliance matrix and testing docs from round 1 retained. Round 2 updates pin/adoption text and generated diagram. Final documentation gates pass. |

## Scope limits

- The source assignment is public comment 5824708827; the gate-fix decision is 5822047670.
- No processor source was edited; only its checkout/gitlink moved to merged main.
- No hardware, additional parent checkout, sub-agent, push or PR operation was used.
- The firmware inconsistent-record early return remains outside scope under #495.
- The #551 cold-pipeline case remains unchanged; #553 owns its later flip.
- Independent review, hosted checks, publication and merge are later steps.
- The full assigned gates passed with the explicitly listed unrun builder arms; this is author evidence, not a review verdict.
