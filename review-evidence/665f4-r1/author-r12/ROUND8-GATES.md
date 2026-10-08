[A560]

# Round 8 gate receipts

Candidate: `a6e6916826448f81de2b779ca61a87a9f8c47278`. All 102 final individual invocations exit 0; all validation jobs have finished.

`$SOURCE` is the candidate checkout; `$SCRATCH` is disk scratch; `$BUILDER_TREE` is the detached scratch checkout at the same head. `$SDK` is the CI-pinned SDK, `$RUNTIME` contains verified link archives, and `$DOCS_ENV` supplies documentation dependencies. `$PINNED_HDL_LIMITED` runs release 5.050 with two build slots and inner jobs limited to eight. These aliases are locations, not bundled dependencies.

Every receipt records the original log size and SHA256. Small retained logs are path-normalized and have their own hash; large logs remain hash/size only. The JSON distinguishes these two byte streams. Superseded development attempts are separate in `ROUND8-DEVELOPMENT.json`.

Long invocations ran detached with an individual log and rc file, followed by bounded foreground waits. The table does not claim a result for an invocation still running.

| Entry | rc | Seconds | Exact argv (working directory in JSON) |
| --- | ---: | ---: | --- |
| builder-final | 0 | 1225.317 | `env 'VERILATOR=$PINNED_HDL_LIMITED' MAKEFLAGS=-j8 python3 sw/builder/test_builder.py --require-rv32` |
| campaign | 0 | 1463.483 | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir '$SCRATCH/campaign'` |
| ci-scope | 0 | 5.399 | `python3 scripts/ci_scope.py --selftest` |
| compiler-absent | 0 | 593.499 | `python3 sw/builder/test_firmware_compiler.py --absent --audit '$SCRATCH/rv32-absent.jsonl'` |
| compiler-controls | 0 | 2.236 | `python3 sw/builder/test_firmware_compiler.py --selftest` |
| compiler-pinned | 0 | 1004.809 | `python3 sw/builder/test_firmware_compiler.py --sdk-destination '$SDK' --audit '$SCRATCH/rv32-pinned.jsonl'` |
| coverage-check | 0 | 234.729 | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep '$SCRATCH/coverage-check'` |
| coverage-selftest | 0 | 0.465 | `python3 sw/firmware/gtest/fw_coverage.py --selftest` |
| coverage-write2 | 0 | 226.512 | `python3 sw/firmware/gtest/fw_coverage.py --write --jobs 4 --keep '$SCRATCH/coverage-write2'` |
| docs-00 | 0 | 0.265 | `python3 scripts/gen_hdl_reference.py --selftest` |
| docs-01-final | 0 | 1.869 | `python3 scripts/gen_hdl_reference.py --output '$SCRATCH/milan-hdl-reference'` |
| docs-02 | 0 | 6.089 | `python3 scripts/docs_check.py` |
| docs-03 | 0 | 3.978 | `python3 scripts/check_em_dash.py --base d8b355fe0f41d49dca6cae1cd8b3826e2edde364` |
| docs-04 | 0 | 0.064 | `python3 scripts/check_doc_style.py` |
| docs-05 | 0 | 0.064 | `python3 scripts/check_doc_style.py --selftest` |
| docs-06 | 0 | 0.214 | `python3 scripts/check_gptp_docs.py` |
| docs-07 | 0 | 0.264 | `python3 scripts/check_gptp_docs.py --selftest` |
| docs-08 | 0 | 0.515 | `python3 docs/DOC_MAP.gen.py --check` |
| docs-09 | 0 | 0.515 | `python3 docs/DOC_MAP.gen.py --selftest` |
| docs-10 | 0 | 0.415 | `python3 docs/diagrams/timesync_chain.gen.py --check` |
| docs-11 | 0 | 0.566 | `python3 docs/diagrams/timesync_chain.gen.py --selftest` |
| docs-12 | 0 | 0.164 | `python3 scripts/check_solution_docs.py` |
| docs-13 | 0 | 3.276 | `python3 scripts/check_solution_docs.py --selftest` |
| docs-14 | 0 | 0.516 | `python3 docs/diagrams/submodule_boundaries.gen.py --check` |
| docs-15 | 0 | 0.616 | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` |
| docs-16 | 0 | 0.616 | `python3 scripts/check_submodule_docs.py` |
| docs-17 | 0 | 0.064 | `python3 scripts/check_submodule_docs.py --selftest` |
| docs-18 | 0 | 0.215 | `python3 scripts/gen_wavedrom.py --selftest` |
| docs-19 | 0 | 0.365 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` |
| docs-20 | 0 | 0.466 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` |
| docs-21 | 0 | 0.466 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` |
| docs-22 | 0 | 0.415 | `python3 scripts/check_diagram_pngs.py` |
| docs-23 | 0 | 7.387 | `python3 scripts/check_diagram_pngs.py --selftest` |
| docs-24 | 0 | 1.067 | `python3 scripts/check_feature_status.py --self-test` |
| docs-25 | 0 | 1.368 | `python3 docs/traceability/gen_module_matrix.py --check` |
| docs-26 | 0 | 0.214 | `python3 scripts/check_gptp_docs.py --with-submodule` |
| docs-27 | 0 | 0.817 | `make -C gptp-processor docs` |
| docs-28 | 0 | 0.164 | `python3 scripts/measure_control_flow.py --selftest` |
| docs-29 | 0 | 0.064 | `python3 scripts/measure_cohesion.py --selftest` |
| docs-30 | 0 | 19.872 | `python3 scripts/check_baremetal_only.py --check` |
| docs-31 | 0 | 7.487 | `python3 scripts/check_baremetal_only.py --selftest` |
| docs-32 | 0 | 1.268 | `python3 scripts/ci_rv32_sdk_selftest.py` |
| docs-33 | 0 | 1.77 | `python3 scripts/ci_rv32_sdk.py --destination '$SDK'` |
| docs-34 | 0 | 2.472 | `python3 scripts/check_nvm_record_space.py` |
| docs-35 | 0 | 48.211 | `python3 scripts/check_nvm_record_space.py --self-test` |
| docs-36 | 0 | 0.867 | `python3 scripts/check_nvm_capture.py` |
| docs-37 | 0 | 77.987 | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` |
| docs-38 | 0 | 0.114 | `python3 scripts/check_soc_sources.py` |
| docs-39 | 0 | 0.265 | `python3 scripts/check_soc_sources.py --selftest` |
| docs-40 | 0 | 2.32 | `python3 sw/litex/iob_pack_selftest.py` |
| docs-41 | 0 | 1.669 | `python3 scripts/check_rtl_source_lists.py` |
| docs-42 | 0 | 3.123 | `python3 scripts/check_rtl_source_lists.py --selftest` |
| docs-43 | 0 | 0.515 | `python3 scripts/measure_naming.py --check` |
| docs-44 | 0 | 0.566 | `python3 scripts/measure_naming.py --selftest` |
| docs-45 | 0 | 2.832 | `python3 scripts/check_port_contracts.py` |
| docs-46 | 0 | 3.221 | `python3 scripts/check_port_contracts.py --selftest` |
| docs-47 | 0 | 1.718 | `python3 scripts/measure_fail_fast.py --check` |
| docs-48 | 0 | 1.72 | `python3 scripts/measure_fail_fast.py --selftest` |
| docs-49 | 0 | 1.87 | `python3 scripts/check_todo_ownership.py` |
| docs-50 | 0 | 1.921 | `python3 scripts/check_todo_ownership.py --selftest` |
| docs-51 | 0 | 6.986 | `python3 scripts/measure_test_evidence.py --check` |
| docs-52 | 0 | 7.286 | `python3 scripts/measure_test_evidence.py --selftest` |
| docs-53 | 0 | 0.415 | `python3 scripts/check_hygiene.py --check` |
| docs-54 | 0 | 0.415 | `python3 scripts/check_hygiene.py --selftest` |
| docs-55 | 0 | 0.515 | `python3 scripts/check_sv_idiom.py` |
| docs-56 | 0 | 0.516 | `python3 scripts/check_sv_idiom.py --selftest` |
| docs-57 | 0 | 1.72 | `python3 scripts/check_cpp_idiom.py` |
| docs-58 | 0 | 1.869 | `python3 scripts/check_cpp_idiom.py --selftest` |
| docs-59 | 0 | 4.73 | `python3 scripts/check_py_idiom.py` |
| docs-60 | 0 | 4.68 | `python3 scripts/check_py_idiom.py --selftest` |
| docs-61 | 0 | 0.315 | `python3 scripts/check_sh_idiom.py` |
| docs-62 | 0 | 0.315 | `python3 scripts/check_sh_idiom.py --selftest` |
| docs-63 | 0 | 0.216 | `python3 scripts/ci_events.py --check` |
| docs-64 | 0 | 16.907 | `python3 scripts/ci_events.py --selftest` |
| docs-65 | 0 | 0.114 | `python3 scripts/check_doc_paths.py` |
| docs-66 | 0 | 0.415 | `python3 scripts/check_archive.py` |
| docs-67 | 0 | 0.065 | `python3 scripts/check_archive.py --selftest` |
| docs-68 | 0 | 0.818 | `python3 scripts/gen_toc.py --selftest` |
| docs-69 | 0 | 2.922 | `python3 scripts/gen_toc.py --verify-anchors` |
| docs-70 | 0 | 4.476 | `python3 scripts/gen_toc.py --check` |
| docs-71 | 0 | 0.114 | `python3 avdecc/gen_aem_store.py --self-test` |
| docs-72 | 0 | 14.561 | `python3 scripts/check_sweep_shape.py --self-test` |
| docs-73 | 0 | 0.517 | `python3 scripts/check_deploy_shape.py --self-test` |
| docs-74 | 0 | 60.525 | `python3 scripts/check_entity_shape.py --self-test` |
| docs-archive-feature | 0 | 1.116 | `python3 scripts/check_feature_status.py` |
| docs-archive | 0 | 5.833 | `python3 scripts/docs_check.py` |
| docs-final | 0 | 5.881 | `python3 scripts/docs_check.py` |
| docs-selftest | 0 | 0.214 | `python3 scripts/docs_check.py --selftest` |
| docs-wire | 0 | 0.314 | `python3 scripts/check_wire_accountability.py --self-test` |
| em-dash-final | 0 | 3.679 | `python3 scripts/check_em_dash.py --base d8b355fe0f41d49dca6cae1cd8b3826e2edde364` |
| f3-images | 0 | 5.198 | `python3 sw/firmware/ctrl/test/ctrl_image.py --out '$SCRATCH/f3-images'` |
| focused3 | 0 | 27.194 | `python3 '$SCRATCH/focused.py'` |
| image-selftest | 0 | 10.398 | `python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32` |
| images | 0 | 10.423 | `python3 '$SCRATCH/images.py'` |
| maap-diff | 0 | 160.341 | `python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep '$SCRATCH/maap-diff'` |
| mailbox-contract | 0 | 0.164 | `python3 sw/mailbox/gen_mailbox.py --check` |
| mailbox-final | 0 | 42.373 | `make -C '$SCRATCH/mailbox/tb/verilator/mbx' -j1 VERILATOR_JOBS=1 'VERILATOR=$PINNED_HDL_LIMITED'` |
| nvm-campaign | 0 | 1916.029 | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 4` |
| rv32-selftest | 0 | 7.76 | `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` |
| source-diff | 0 | 0.016 | `git diff --check f74b9403b330ce316eeec6f724846f16def98443 HEAD` |
| tally-mutants | 0 | 64.692 | `python3 sw/firmware/gtest/tally_selftest.py --mutants` |
| toc | 0 | 5.086 | `python3 scripts/gen_toc.py --check` |
