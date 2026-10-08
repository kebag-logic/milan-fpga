[A560]

# Round 9 gate receipts

Candidate: `edeef61c5a0cc6c18caa61db4019a8e378baf366`. Final individual receipts: 107.

`$SOURCE` is the candidate checkout; `$SCRATCH` is disk scratch; `$BUILDER_TREE` is the detached scratch checkout at `877c0b9d04078867e2bef481903745198527844c`; the final commit changes only the coverage ratchet, outside the builder inputs. The source proof records that exact one-file difference. `$SDK` is the CI-pinned SDK, `$RUNTIME` contains verified link archives, and `$DOCS_ENV` supplies documentation dependencies. `$PINNED_HDL_LIMITED` runs release 5.050 with two build slots and inner jobs limited to eight. These aliases are locations, not bundled dependencies.

Every receipt records the original log size and SHA256. Small retained logs are path-normalized and have their own hash; large logs remain hash/size only. The JSON distinguishes these two byte streams. Superseded development attempts are separate in `ROUND9-DEVELOPMENT.json`.

Long invocations ran detached with an individual log and rc file, followed by bounded foreground waits. The table does not claim a result for an invocation still running.

| Entry | rc | Seconds | Exact argv (working directory in JSON) |
| --- | ---: | ---: | --- |
| acmp-asan-final | 0 | 71.873 | `python3 '$SCRATCH/reviews/R532-8/scripts/probe_acmp_a0.py' '$SOURCE' '$SCRATCH/acmp-asan-final-build'` |
| binding-probe | 0 | 19.899 | `python3 '$SCRATCH/reviews/R533-8/binding_required.py'` |
| bound-table | 0 | 0.466 | `python3 '$SCRATCH/reviews/R533-8/check_bounds.py'` |
| builder-final | 0 | 1224.443 | `env MAKEFLAGS=-j8 python3 sw/builder/test_builder.py --require-rv32` |
| campaign-verified | 0 | 1553.049 | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir '$SCRATCH/campaign-verified'` |
| ci-scope | 0 | 5.636 | `python3 scripts/ci_scope.py --selftest` |
| compiler-absent | 0 | 581.477 | `python3 sw/builder/test_firmware_compiler.py --absent --audit '$SCRATCH/rv32-absent.jsonl'` |
| compiler-controls | 0 | 1.718 | `python3 sw/builder/test_firmware_compiler.py --selftest` |
| compiler-pinned | 0 | 1021.593 | `python3 sw/builder/test_firmware_compiler.py --sdk-destination '$SDK' --audit '$SCRATCH/rv32-pinned.jsonl'` |
| coverage-check | 0 | 231.366 | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep '$SCRATCH/coverage-check'` |
| coverage-selftest | 0 | 0.415 | `python3 sw/firmware/gtest/fw_coverage.py --selftest` |
| coverage-write-final | 0 | 224.792 | `python3 sw/firmware/gtest/fw_coverage.py --write --jobs 4 --keep '$SCRATCH/coverage-write-final'` |
| docs-00 | 0 | 0.215 | `python3 scripts/gen_hdl_reference.py --selftest` |
| docs-01 | 0 | 1.843 | `python3 scripts/gen_hdl_reference.py --output '$SCRATCH/milan-hdl-reference'` |
| docs-02 | 0 | 5.771 | `python3 scripts/docs_check.py` |
| docs-03 | 0 | 3.538 | `python3 scripts/check_em_dash.py --base d8b355fe0f41d49dca6cae1cd8b3826e2edde364` |
| docs-04 | 0 | 0.064 | `python3 scripts/check_doc_style.py` |
| docs-05 | 0 | 0.064 | `python3 scripts/check_doc_style.py --selftest` |
| docs-06 | 0 | 0.215 | `python3 scripts/check_gptp_docs.py` |
| docs-07 | 0 | 0.215 | `python3 scripts/check_gptp_docs.py --selftest` |
| docs-08 | 0 | 0.468 | `python3 docs/DOC_MAP.gen.py --check` |
| docs-09 | 0 | 0.566 | `python3 docs/DOC_MAP.gen.py --selftest` |
| docs-10 | 0 | 0.434 | `python3 docs/diagrams/timesync_chain.gen.py --check` |
| docs-11 | 0 | 0.516 | `python3 docs/diagrams/timesync_chain.gen.py --selftest` |
| docs-12 | 0 | 0.164 | `python3 scripts/check_solution_docs.py` |
| docs-13 | 0 | 2.801 | `python3 scripts/check_solution_docs.py --selftest` |
| docs-14 | 0 | 0.566 | `python3 docs/diagrams/submodule_boundaries.gen.py --check` |
| docs-15 | 0 | 0.616 | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` |
| docs-16 | 0 | 0.566 | `python3 scripts/check_submodule_docs.py` |
| docs-17 | 0 | 0.067 | `python3 scripts/check_submodule_docs.py --selftest` |
| docs-18 | 0 | 0.164 | `python3 scripts/gen_wavedrom.py --selftest` |
| docs-19 | 0 | 0.315 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` |
| docs-20 | 0 | 0.415 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` |
| docs-21 | 0 | 0.415 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` |
| docs-22 | 0 | 0.416 | `python3 scripts/check_diagram_pngs.py` |
| docs-23 | 0 | 7.711 | `python3 scripts/check_diagram_pngs.py --selftest` |
| docs-24 | 0 | 0.966 | `python3 scripts/check_feature_status.py --self-test` |
| docs-25 | 0 | 1.267 | `python3 docs/traceability/gen_module_matrix.py --check` |
| docs-26 | 0 | 0.214 | `python3 scripts/check_gptp_docs.py --with-submodule` |
| docs-27 | 0 | 0.768 | `make -C gptp-processor docs` |
| docs-28 | 0 | 0.164 | `python3 scripts/measure_control_flow.py --selftest` |
| docs-29 | 0 | 0.064 | `python3 scripts/measure_cohesion.py --selftest` |
| docs-30 | 0 | 19.547 | `python3 scripts/check_baremetal_only.py --check` |
| docs-31 | 0 | 7.049 | `python3 scripts/check_baremetal_only.py --selftest` |
| docs-32 | 0 | 1.218 | `python3 scripts/ci_rv32_sdk_selftest.py` |
| docs-33 | 0 | 1.326 | `python3 scripts/ci_rv32_sdk.py --destination '$SDK'` |
| docs-34 | 0 | 2.675 | `python3 scripts/check_nvm_record_space.py` |
| docs-35 | 0 | 47.427 | `python3 scripts/check_nvm_record_space.py --self-test` |
| docs-36 | 0 | 1.018 | `python3 scripts/check_nvm_capture.py` |
| docs-37 | 0 | 79.453 | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` |
| docs-38 | 0 | 0.165 | `python3 scripts/check_soc_sources.py` |
| docs-39 | 0 | 0.265 | `python3 scripts/check_soc_sources.py --selftest` |
| docs-40 | 0 | 2.574 | `python3 sw/litex/iob_pack_selftest.py` |
| docs-41 | 0 | 1.67 | `python3 scripts/check_rtl_source_lists.py` |
| docs-42 | 0 | 3.026 | `python3 scripts/check_rtl_source_lists.py --selftest` |
| docs-43 | 0 | 0.515 | `python3 scripts/measure_naming.py --check` |
| docs-44 | 0 | 0.566 | `python3 scripts/measure_naming.py --selftest` |
| docs-45 | 0 | 2.822 | `python3 scripts/check_port_contracts.py` |
| docs-46 | 0 | 3.127 | `python3 scripts/check_port_contracts.py --selftest` |
| docs-47 | 0 | 1.823 | `python3 scripts/measure_fail_fast.py --check` |
| docs-48 | 0 | 1.621 | `python3 scripts/measure_fail_fast.py --selftest` |
| docs-49 | 0 | 1.819 | `python3 scripts/check_todo_ownership.py` |
| docs-50 | 0 | 1.77 | `python3 scripts/check_todo_ownership.py --selftest` |
| docs-51 | 0 | 6.648 | `python3 scripts/measure_test_evidence.py --check` |
| docs-52 | 0 | 7.035 | `python3 scripts/measure_test_evidence.py --selftest` |
| docs-53 | 0 | 0.415 | `python3 scripts/check_hygiene.py --check` |
| docs-54 | 0 | 0.415 | `python3 scripts/check_hygiene.py --selftest` |
| docs-55 | 0 | 0.516 | `python3 scripts/check_sv_idiom.py` |
| docs-56 | 0 | 0.516 | `python3 scripts/check_sv_idiom.py --selftest` |
| docs-57 | 0 | 1.772 | `python3 scripts/check_cpp_idiom.py` |
| docs-58 | 0 | 1.877 | `python3 scripts/check_cpp_idiom.py --selftest` |
| docs-59 | 0 | 4.688 | `python3 scripts/check_py_idiom.py` |
| docs-60 | 0 | 4.398 | `python3 scripts/check_py_idiom.py --selftest` |
| docs-61 | 0 | 0.265 | `python3 scripts/check_sh_idiom.py` |
| docs-62 | 0 | 0.265 | `python3 scripts/check_sh_idiom.py --selftest` |
| docs-63 | 0 | 0.214 | `python3 scripts/ci_events.py --check` |
| docs-64 | 0 | 17.912 | `python3 scripts/ci_events.py --selftest` |
| docs-65 | 0 | 0.129 | `python3 scripts/check_doc_paths.py` |
| docs-66 | 0 | 0.415 | `python3 scripts/check_archive.py` |
| docs-67 | 0 | 0.114 | `python3 scripts/check_archive.py --selftest` |
| docs-68 | 0 | 0.916 | `python3 scripts/gen_toc.py --selftest` |
| docs-69 | 0 | 3.223 | `python3 scripts/gen_toc.py --verify-anchors` |
| docs-70 | 0 | 4.776 | `python3 scripts/gen_toc.py --check` |
| docs-71 | 0 | 0.114 | `python3 avdecc/gen_aem_store.py --self-test` |
| docs-72 | 0 | 15.235 | `python3 scripts/check_sweep_shape.py --self-test` |
| docs-73 | 0 | 0.469 | `python3 scripts/check_deploy_shape.py --self-test` |
| docs-74 | 0 | 58.8 | `python3 scripts/check_entity_shape.py --self-test` |
| docs-archive-feature | 0 | 1.068 | `python3 scripts/check_feature_status.py` |
| docs-archive | 0 | 5.843 | `python3 scripts/docs_check.py` |
| docs-final | 0 | 5.84 | `python3 scripts/docs_check.py` |
| docs-selftest | 0 | 0.164 | `python3 scripts/docs_check.py --selftest` |
| docs-wire | 0 | 0.316 | `python3 scripts/check_wire_accountability.py --self-test` |
| em-dash-final | 0 | 3.63 | `python3 scripts/check_em_dash.py --base d8b355fe0f41d49dca6cae1cd8b3826e2edde364` |
| f3-images | 0 | 4.174 | `python3 sw/firmware/ctrl/test/ctrl_image.py --out '$SCRATCH/f3-images'` |
| image-selftest | 0 | 8.937 | `python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32` |
| images-final | 0 | 9.744 | `python3 '$SCRATCH/images.py'` |
| maap-diff | 0 | 144.545 | `python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep '$SCRATCH/maap-diff'` |
| mailbox-contract | 0 | 0.164 | `python3 sw/mailbox/gen_mailbox.py --check` |
| mailbox-verified | 0 | 30.34 | `make -C '$SCRATCH/mailbox/tb/verilator/mbx' -j8 VBUILD_JOBS=2` |
| new-plants-final | 0 | 141.678 | `python3 '$SCRATCH/new_plants.py'` |
| nvm-campaign | 0 | 1887.939 | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 4` |
| remaining-plants | 0 | 18.482 | `python3 '$SCRATCH/remaining_plants.py'` |
| reviewer-bounds | 0 | 134.577 | `python3 '$SCRATCH/reviewer_bounds.py'` |
| rv32-selftest | 0 | 6.328 | `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` |
| source-diff | 0 | 0.016 | `git diff --check f74b9403b330ce316eeec6f724846f16def98443 HEAD` |
| tally-mutants | 0 | 55.396 | `python3 sw/firmware/gtest/tally_selftest.py --mutants` |
| toc | 0 | 4.778 | `python3 scripts/gen_toc.py --check` |
