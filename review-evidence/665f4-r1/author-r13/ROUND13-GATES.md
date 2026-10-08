[A560]

# Round 13 gate results

All 86 final command records return zero. Supervisor records are not counted twice.
See ROUND13-REPRODUCE.md for path aliases and prerequisites.
Logs over 200 KB are represented by original byte size and SHA-256 only.
Retained logs normalize execution paths; both hashes are recorded in JSON.

| Gate | Command | Exit | Seconds |
| --- | --- | ---: | ---: |
| asan | `python3 '$SCRATCH/asan.py'` | 0 | 149.024 |
| coverage-check | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep '$SCRATCH/coverage-build'` | 0 | 223.421 |
| ctrl-full | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir '$SCRATCH/ctrl-build'` | 0 | 1833.669 |
| diff-final | `git diff --check efea74858dffc482820d4f19c26c38796a57ff75 HEAD` | 0 | 0.008 |
| docs-00 | `python3 scripts/gen_hdl_reference.py --selftest` | 0 | 0.265 |
| docs-01 | `python3 scripts/gen_hdl_reference.py --output '$SCRATCH/milan-hdl-reference'` | 0 | 1.918 |
| docs-02 | `python3 scripts/docs_check.py` | 0 | 6.034 |
| docs-03 | `python3 scripts/check_em_dash.py --base efea74858dffc482820d4f19c26c38796a57ff75` | 0 | 3.887 |
| docs-04 | `python3 scripts/check_doc_style.py` | 0 | 0.115 |
| docs-05 | `python3 scripts/check_doc_style.py --selftest` | 0 | 0.064 |
| docs-06 | `python3 scripts/check_gptp_docs.py` | 0 | 0.214 |
| docs-07 | `python3 scripts/check_gptp_docs.py --selftest` | 0 | 0.265 |
| docs-08 | `python3 docs/DOC_MAP.gen.py --check` | 0 | 0.415 |
| docs-09 | `python3 docs/DOC_MAP.gen.py --selftest` | 0 | 0.465 |
| docs-10 | `python3 docs/diagrams/timesync_chain.gen.py --check` | 0 | 0.416 |
| docs-11 | `python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 | 0.465 |
| docs-12 | `python3 scripts/check_solution_docs.py` | 0 | 0.164 |
| docs-13 | `python3 scripts/check_solution_docs.py --selftest` | 0 | 3.278 |
| docs-14 | `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | 0.466 |
| docs-15 | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 | 0.52 |
| docs-16 | `python3 scripts/check_submodule_docs.py` | 0 | 0.566 |
| docs-17 | `python3 scripts/check_submodule_docs.py --selftest` | 0 | 0.064 |
| docs-18 | `python3 scripts/gen_wavedrom.py --selftest` | 0 | 0.164 |
| docs-19 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | 0 | 0.365 |
| docs-20 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | 0 | 0.415 |
| docs-21 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | 0 | 0.415 |
| docs-22 | `python3 scripts/check_diagram_pngs.py` | 0 | 0.415 |
| docs-23 | `python3 scripts/check_diagram_pngs.py --selftest` | 0 | 7.687 |
| docs-24 | `python3 scripts/check_feature_status.py --self-test` | 0 | 0.966 |
| docs-25 | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | 1.318 |
| docs-26 | `python3 scripts/check_gptp_docs.py --with-submodule` | 0 | 0.215 |
| docs-27 | `make -C gptp-processor docs` | 0 | 0.816 |
| docs-28 | `python3 scripts/measure_control_flow.py --selftest` | 0 | 0.164 |
| docs-29 | `python3 scripts/measure_cohesion.py --selftest` | 0 | 0.064 |
| docs-30 | `python3 scripts/check_baremetal_only.py --check` | 0 | 20.77 |
| docs-31 | `python3 scripts/check_baremetal_only.py --selftest` | 0 | 8.096 |
| docs-32 | `python3 scripts/ci_rv32_sdk_selftest.py` | 0 | 1.368 |
| docs-33 | `python3 scripts/ci_rv32_sdk.py --destination '$SDK'` | 0 | 1.834 |
| docs-34 | `python3 scripts/check_nvm_record_space.py` | 0 | 2.622 |
| docs-35 | `python3 scripts/check_nvm_record_space.py --self-test` | 0 | 49.072 |
| docs-36 | `python3 scripts/check_nvm_capture.py` | 0 | 0.967 |
| docs-37 | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | 77.572 |
| docs-38 | `python3 scripts/check_soc_sources.py` | 0 | 0.164 |
| docs-39 | `python3 scripts/check_soc_sources.py --selftest` | 0 | 0.264 |
| docs-40 | `python3 sw/litex/iob_pack_selftest.py` | 0 | 2.723 |
| docs-41 | `python3 scripts/check_rtl_source_lists.py` | 0 | 1.669 |
| docs-42 | `python3 scripts/check_rtl_source_lists.py --selftest` | 0 | 2.973 |
| docs-43 | `python3 scripts/measure_naming.py --check` | 0 | 0.515 |
| docs-44 | `python3 scripts/measure_naming.py --selftest` | 0 | 0.516 |
| docs-45 | `python3 scripts/check_port_contracts.py` | 0 | 2.673 |
| docs-46 | `python3 scripts/check_port_contracts.py --selftest` | 0 | 3.373 |
| docs-47 | `python3 scripts/measure_fail_fast.py --check` | 0 | 1.819 |
| docs-48 | `python3 scripts/measure_fail_fast.py --selftest` | 0 | 1.824 |
| docs-49 | `python3 scripts/check_todo_ownership.py` | 0 | 1.919 |
| docs-50 | `python3 scripts/check_todo_ownership.py --selftest` | 0 | 1.918 |
| docs-51 | `python3 scripts/measure_test_evidence.py --check` | 0 | 7.092 |
| docs-52 | `python3 scripts/measure_test_evidence.py --selftest` | 0 | 7.189 |
| docs-53 | `python3 scripts/check_hygiene.py --check` | 0 | 0.466 |
| docs-54 | `python3 scripts/check_hygiene.py --selftest` | 0 | 0.468 |
| docs-55 | `python3 scripts/check_sv_idiom.py` | 0 | 0.517 |
| docs-56 | `python3 scripts/check_sv_idiom.py --selftest` | 0 | 0.516 |
| docs-57 | `python3 scripts/check_cpp_idiom.py` | 0 | 1.718 |
| docs-58 | `python3 scripts/check_cpp_idiom.py --selftest` | 0 | 1.868 |
| docs-59 | `python3 scripts/check_py_idiom.py` | 0 | 4.426 |
| docs-60 | `python3 scripts/check_py_idiom.py --selftest` | 0 | 4.63 |
| docs-61 | `python3 scripts/check_sh_idiom.py` | 0 | 0.265 |
| docs-62 | `python3 scripts/check_sh_idiom.py --selftest` | 0 | 0.265 |
| docs-63 | `python3 scripts/ci_events.py --check` | 0 | 0.214 |
| docs-64 | `python3 scripts/ci_events.py --selftest` | 0 | 18.74 |
| docs-65 | `python3 scripts/check_doc_paths.py` | 0 | 0.114 |
| docs-66 | `python3 scripts/check_archive.py` | 0 | 0.415 |
| docs-67 | `python3 scripts/check_archive.py --selftest` | 0 | 0.114 |
| docs-68 | `python3 scripts/gen_toc.py --selftest` | 0 | 0.918 |
| docs-69 | `python3 scripts/gen_toc.py --verify-anchors` | 0 | 3.274 |
| docs-70 | `python3 scripts/gen_toc.py --check` | 0 | 5.431 |
| docs-71 | `python3 avdecc/gen_aem_store.py --self-test` | 0 | 0.114 |
| docs-72 | `python3 scripts/check_sweep_shape.py --self-test` | 0 | 15.433 |
| docs-73 | `python3 scripts/check_deploy_shape.py --self-test` | 0 | 0.515 |
| docs-74 | `python3 scripts/check_entity_shape.py --self-test` | 0 | 59.592 |
| docs-archive | `python3 scripts/docs_check.py` | 0 | 5.58 |
| em-dash-final | `python3 scripts/check_em_dash.py --base efea74858dffc482820d4f19c26c38796a57ff75` | 0 | 3.526 |
| focused | `python3 '$SCRATCH/focused.py'` | 0 | 34.376 |
| mailbox-contract | `python3 sw/mailbox/gen_mailbox.py --check` | 0 | 0.166 |
| new-plants | `python3 '$SCRATCH/new_plants.py'` | 0 | 29.351 |
| python-final | `python3 scripts/check_py_idiom.py` | 0 | 4.226 |
| review-probes | `python3 '$SCRATCH/review_probes.py'` | 0 | 22.73 |
