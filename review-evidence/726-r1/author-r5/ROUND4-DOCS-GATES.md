# Round 4 documentation workflow receipts

Head: `1add0cfbcc778c5292a5935631ca7b47c612b990`.

All 78 executable docs-check commands and three companion commands completed
with exit code 0. Dependency-install steps are prerequisites, not counted as checks.
The pinned runtime is 3.12.3; the dependency receipt records package versions.
The table gives the job commands as plain shell. Commands run unpiped.

The offline runner self-test executed inside a disposable, read-only,
network-disabled CI container. It did not run as a host orchestrator.
The complete builder used a writable scratch export of the exact source bytes,
read-only submodules and the pinned target SDK. Its actual container exit was 0.
It reports 19 optional NOT RUN arms; those arms have no passing claim.
The first 570-second observer ended incomplete; the second captured completion.
The compiler-absence run is a passing negative control with no compiler calls.
The no-git inventory check reports its expected parity skip.

`$SCRATCH` is disk scratch, `$ROOT` the candidate checkout, and `$RUNNER_TEMP`
a disk-backed runner temporary directory. Refer to the workflow for dependencies.

| Receipt | Workflow step | Command | Result |
|---|---|---|---|
| docs-00 | Build the validated HDL reference | `python3 scripts/gen_hdl_reference.py --selftest` | rc 0 |
| docs-01 | Build the validated HDL reference | `python3 scripts/gen_hdl_reference.py --output $SCRATCH/milan-hdl-reference` | rc 0 |
| docs-02 | Link health, wording, dead-reference and local-info gate | `python3 scripts/docs_check.py` | rc 0 |
| docs-03 | Added-line em-dash gate | `python3 scripts/check_em_dash.py --base c6bd08c6` | rc 0 |
| docs-04 | Concise audience documentation gate | `python3 scripts/check_doc_style.py` | rc 0 |
| docs-05 | Concise audience documentation gate | `python3 scripts/check_doc_style.py --selftest` | rc 0 |
| docs-06 | Concise audience documentation gate | `python3 scripts/check_gptp_docs.py` | rc 0 |
| docs-07 | Concise audience documentation gate | `python3 scripts/check_gptp_docs.py --selftest` | rc 0 |
| docs-08 | Audience diagram no-drift gate | `python3 docs/DOC_MAP.gen.py --check` | rc 0 |
| docs-09 | Audience diagram no-drift gate | `python3 docs/DOC_MAP.gen.py --selftest` | rc 0 |
| docs-10 | Audience diagram no-drift gate | `python3 docs/diagrams/timesync_chain.gen.py --check` | rc 0 |
| docs-11 | Audience diagram no-drift gate | `python3 docs/diagrams/timesync_chain.gen.py --selftest` | rc 0 |
| docs-12 | Product solution source-fact gate | `python3 scripts/check_solution_docs.py` | rc 0 |
| docs-13 | Product solution source-fact gate | `python3 scripts/check_solution_docs.py --selftest` | rc 0 |
| docs-14 | Verified submodule documentation gate | `python3 docs/diagrams/submodule_boundaries.gen.py --check` | rc 0 |
| docs-15 | Verified submodule documentation gate | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | rc 0 |
| docs-16 | Verified submodule documentation gate | `python3 scripts/check_submodule_docs.py` | rc 0 |
| docs-17 | Verified submodule documentation gate | `python3 scripts/check_submodule_docs.py --selftest` | rc 0 |
| docs-18 | HDL timing diagram no-drift gate | `python3 scripts/gen_wavedrom.py --selftest` | rc 0 |
| docs-19 | HDL timing diagram no-drift gate | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | rc 0 |
| docs-20 | HDL timing diagram no-drift gate | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | rc 0 |
| docs-21 | HDL timing diagram no-drift gate | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | rc 0 |
| docs-22 | Published diagram PNG gate | `python3 scripts/check_diagram_pngs.py` | rc 0 |
| docs-23 | Published diagram PNG gate | `python3 scripts/check_diagram_pngs.py --selftest` | rc 0 |
| docs-24 | Milan feature-status consistency gate | `python3 scripts/check_feature_status.py --self-test` | rc 0 |
| docs-25 | Traceability matrix no-drift gate | `python3 docs/traceability/gen_module_matrix.py --check` | rc 0 |
| docs-26 | Imported gPTP documentation gate | `python3 scripts/check_gptp_docs.py --with-submodule` | rc 0 |
| docs-27 | Imported gPTP documentation gate | `make -C gptp-processor docs` | rc 0 |
| docs-28 | Code-quality measurement self-tests | `python3 scripts/measure_control_flow.py --selftest` | rc 0 |
| docs-29 | Code-quality measurement self-tests | `python3 scripts/measure_cohesion.py --selftest` | rc 0 |
| docs-30 | Bare-metal scope gate | `python3 scripts/check_baremetal_only.py --check` | rc 0 |
| docs-31 | Bare-metal scope gate | `python3 scripts/check_baremetal_only.py --selftest` | rc 0 |
| docs-32 | Install and verify the pinned RV32 SDK | `python3 scripts/ci_rv32_sdk_selftest.py` | rc 0 |
| docs-33 | Compiler-absent firmware controls | `python3 sw/builder/test_firmware_compiler.py --selftest` | rc 0 |
| docs-34 | Compiler-absent firmware controls | `python3 sw/builder/test_firmware_compiler.py --absent --audit $SCRATCH/rv32-absent.jsonl` | rc 0; compiler-absence negative control |
| docs-35 | End-station builder gates | `python3 sw/builder/test_builder.py --require-rv32` | container rc 0; 19 NOT RUN; see builder-complete receipt |
| docs-36 | NVM record-space gate | `python3 scripts/check_nvm_record_space.py` | rc 0 |
| docs-37 | NVM record-space gate | `python3 scripts/check_nvm_record_space.py --self-test` | rc 0 |
| docs-38 | Capture measurement census and clock gate | `python3 scripts/check_nvm_capture.py` | rc 0 |
| docs-39 | Saved-state writer gate | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | rc 0 |
| docs-40 | SoC source-list gate (Vivado would fail 40 min in without this) | `python3 scripts/check_soc_sources.py` | rc 0 |
| docs-41 | SoC source-list gate (Vivado would fail 40 min in without this) | `python3 scripts/check_soc_sources.py --selftest` | rc 0 |
| docs-42 | SoC source-list gate (Vivado would fail 40 min in without this) | `python3 sw/litex/iob_pack_selftest.py` | rc 0 |
| docs-43 | RTL source-list drift gate | `python3 scripts/check_rtl_source_lists.py` | rc 0 |
| docs-44 | RTL source-list drift gate | `python3 scripts/check_rtl_source_lists.py --selftest` | rc 0 |
| docs-45 | Boundary-unit naming ratchet | `python3 scripts/measure_naming.py --check` | rc 0 |
| docs-46 | Boundary-unit naming ratchet | `python3 scripts/measure_naming.py --selftest` | rc 0 |
| docs-47 | Port contract gate | `python3 scripts/check_port_contracts.py` | rc 0 |
| docs-48 | Port contract gate | `python3 scripts/check_port_contracts.py --selftest` | rc 0 |
| docs-49 | Fail-fast ratchet | `python3 scripts/measure_fail_fast.py --check` | rc 0 |
| docs-50 | Fail-fast ratchet | `python3 scripts/measure_fail_fast.py --selftest` | rc 0 |
| docs-51 | TODO ownership gate | `python3 scripts/check_todo_ownership.py` | rc 0 |
| docs-52 | TODO ownership gate | `python3 scripts/check_todo_ownership.py --selftest` | rc 0 |
| docs-53 | Test-evidence ratchet | `python3 scripts/measure_test_evidence.py --check` | rc 0 |
| docs-54 | Test-evidence ratchet | `python3 scripts/measure_test_evidence.py --selftest` | rc 0 |
| docs-55 | Mechanical hygiene ratchet | `python3 scripts/check_hygiene.py --check` | rc 0 |
| docs-56 | Mechanical hygiene ratchet | `python3 scripts/check_hygiene.py --selftest` | rc 0 |
| docs-57 | SystemVerilog idiom gate | `python3 scripts/check_sv_idiom.py` | rc 0 |
| docs-58 | SystemVerilog idiom gate | `python3 scripts/check_sv_idiom.py --selftest` | rc 0 |
| docs-59 | C and C++ idiom gate | `python3 scripts/check_cpp_idiom.py` | rc 0 |
| docs-60 | C and C++ idiom gate | `python3 scripts/check_cpp_idiom.py --selftest` | rc 0 |
| docs-61 | Python idiom gate | `python3 scripts/check_py_idiom.py` | rc 0 |
| docs-62 | Python idiom gate | `python3 scripts/check_py_idiom.py --selftest` | rc 0 |
| docs-63 | Shell idiom gate | `python3 scripts/check_sh_idiom.py` | rc 0 |
| docs-64 | Shell idiom gate | `python3 scripts/check_sh_idiom.py --selftest` | rc 0 |
| docs-65 | CI event and SHA contract gate | `python3 scripts/ci_events.py --check` | rc 0 |
| docs-66 | CI event and SHA contract gate | `python3 scripts/ci_events.py --selftest` | rc 0 |
| docs-67 | Local act runner contract gate | `python3 scripts/act_ci.py --selftest` | rc 0 |
| docs-68 | Doc cited-path gate | `python3 scripts/check_doc_paths.py` | rc 0 |
| docs-69 | Archive integrity gate | `python3 scripts/check_archive.py` | rc 0 |
| docs-70 | Archive integrity gate | `python3 scripts/check_archive.py --selftest` | rc 0 |
| docs-71 | Per-page contents gate | `python3 scripts/gen_toc.py --selftest` | rc 0 |
| docs-72 | Per-page contents gate | `python3 scripts/gen_toc.py --verify-anchors` | rc 0 |
| docs-73 | Per-page contents gate | `python3 scripts/gen_toc.py --check` | rc 0 |
| docs-74 | AEM store generator self-test | `python3 avdecc/gen_aem_store.py --self-test` | rc 0 |
| docs-75 | Sweep/build shape gate | `python3 scripts/check_sweep_shape.py --self-test` | rc 0 |
| docs-76 | Deploy shape gate | `python3 scripts/check_deploy_shape.py --self-test` | rc 0 |
| docs-77 | Entity shape gate | `python3 scripts/check_entity_shape.py --self-test` | rc 0 |
| wire | Companion check | `python3 scripts/check_wire_accountability.py --self-test` | rc 0 |
| no-git-docs | Companion check | `python3 $SCRATCH/no-git/scripts/docs_check.py` | rc 0 |
| no-git-feature | Companion check | `python3 $SCRATCH/no-git/scripts/check_feature_status.py` | rc 0 |

Final committed-head reruns of docs_check, check_doc_style, gen_toc --check,
check_em_dash --base c6bd08c6 and check_doc_paths also returned 0.
`ROUND4-GATES.tsv` includes those separate receipts.
