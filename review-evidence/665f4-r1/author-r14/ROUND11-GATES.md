[A560]

# Round 11 gate receipts

Candidate: `b98eb2d5a21522bab3bc6bb943332cf8edf11893`. Final individual receipts: 113.

`$SOURCE` is the candidate checkout; `$SCRATCH` is disk scratch; `$BUILDER_TREE` is the frozen builder checkout at `803e8c3c9e7506c4f004d562437ae4f374fbad8e`; its only difference from the final candidate is one ACMP mutation-oracle index, outside builder inputs (see `ROUND11-SOURCE.json`). `$SDK` is the CI-pinned SDK, `$RUNTIME` contains verified link archives, and `$DOCS_ENV` supplies documentation dependencies. `$PINNED_HDL_LIMITED` runs release 5.050 with two build slots and inner jobs limited to eight. These aliases are locations, not bundled dependencies.

Every receipt records the original log size and SHA256. Small retained logs are path-normalized and have their own hash; large logs remain hash/size only. The JSON distinguishes these two byte streams. Superseded development attempts are separate in `ROUND11-DEVELOPMENT.json`.

Long invocations ran detached with an individual log and rc file, followed by bounded foreground waits. The table does not claim a result for an invocation still running.

| Entry | rc | Seconds | Exact argv (working directory in JSON) |
| --- | ---: | ---: | --- |
| asan-final | 0 | 162.739 | `python3 '$SCRATCH/asan.py'` |
| binding-probe | 0 | 21.214 | `python3 '$SCRATCH/binding_required.py'` |
| bound-table | 0 | 0.465 | `python3 '$SCRATCH/check_bounds.py'` |
| builder | 0 | 1166.768 | `env MAKEFLAGS=-j8 python3 sw/builder/test_builder.py --require-rv32` |
| campaign-verified-final | 0 | 1661.861 | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir '$SCRATCH/campaign-frozen'` |
| ci-scope | 0 | 5.778 | `python3 scripts/ci_scope.py --selftest` |
| compiler-absent | 0 | 579.501 | `python3 sw/builder/test_firmware_compiler.py --absent --audit '$SCRATCH/rv32-absent.jsonl'` |
| compiler-controls | 0 | 1.919 | `python3 sw/builder/test_firmware_compiler.py --selftest` |
| compiler-pinned | 0 | 1003.952 | `python3 sw/builder/test_firmware_compiler.py --sdk-destination '$SDK' --audit '$SCRATCH/rv32-pinned.jsonl'` |
| coverage-check | 0 | 222.226 | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --lwsrp third_party/lwSRP --keep '$SCRATCH/coverage-check'` |
| coverage-selftest | 0 | 0.415 | `python3 sw/firmware/gtest/fw_coverage.py --selftest` |
| coverage-write-final | 0 | 211.052 | `python3 sw/firmware/gtest/fw_coverage.py --write --jobs 4 --lwsrp third_party/lwSRP --keep '$SCRATCH/coverage-final'` |
| cpp-final | 0 | 1.618 | `python3 scripts/check_cpp_idiom.py` |
| doc-paths-final | 0 | 0.114 | `python3 scripts/check_doc_paths.py` |
| doc-style-final | 0 | 0.064 | `python3 scripts/check_doc_style.py` |
| docs-00 | 0 | 0.265 | `python3 scripts/gen_hdl_reference.py --selftest` |
| docs-01 | 0 | 1.819 | `python3 scripts/gen_hdl_reference.py --output '$SCRATCH/milan-hdl-reference'` |
| docs-02 | 0 | 5.992 | `python3 scripts/docs_check.py` |
| docs-03 | 0 | 3.782 | `python3 scripts/check_em_dash.py --base d8b355fe0f41d49dca6cae1cd8b3826e2edde364` |
| docs-04 | 0 | 0.064 | `python3 scripts/check_doc_style.py` |
| docs-05 | 0 | 0.064 | `python3 scripts/check_doc_style.py --selftest` |
| docs-06 | 0 | 0.214 | `python3 scripts/check_gptp_docs.py` |
| docs-07 | 0 | 0.266 | `python3 scripts/check_gptp_docs.py --selftest` |
| docs-08 | 0 | 0.466 | `python3 docs/DOC_MAP.gen.py --check` |
| docs-09 | 0 | 0.521 | `python3 docs/DOC_MAP.gen.py --selftest` |
| docs-10 | 0 | 0.416 | `python3 docs/diagrams/timesync_chain.gen.py --check` |
| docs-11 | 0 | 0.466 | `python3 docs/diagrams/timesync_chain.gen.py --selftest` |
| docs-12 | 0 | 0.164 | `python3 scripts/check_solution_docs.py` |
| docs-13 | 0 | 2.878 | `python3 scripts/check_solution_docs.py --selftest` |
| docs-14 | 0 | 0.517 | `python3 docs/diagrams/submodule_boundaries.gen.py --check` |
| docs-15 | 0 | 0.62 | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` |
| docs-16 | 0 | 0.569 | `python3 scripts/check_submodule_docs.py` |
| docs-17 | 0 | 0.065 | `python3 scripts/check_submodule_docs.py --selftest` |
| docs-18 | 0 | 0.167 | `python3 scripts/gen_wavedrom.py --selftest` |
| docs-19 | 0 | 0.318 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` |
| docs-20 | 0 | 0.466 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` |
| docs-21 | 0 | 0.366 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` |
| docs-22 | 0 | 0.418 | `python3 scripts/check_diagram_pngs.py` |
| docs-23 | 0 | 7.084 | `python3 scripts/check_diagram_pngs.py --selftest` |
| docs-24 | 0 | 1.072 | `python3 scripts/check_feature_status.py --self-test` |
| docs-25 | 0 | 1.375 | `python3 docs/traceability/gen_module_matrix.py --check` |
| docs-26 | 0 | 0.269 | `python3 scripts/check_gptp_docs.py --with-submodule` |
| docs-27 | 0 | 0.767 | `make -C gptp-processor docs` |
| docs-28 | 0 | 0.218 | `python3 scripts/measure_control_flow.py --selftest` |
| docs-29 | 0 | 0.067 | `python3 scripts/measure_cohesion.py --selftest` |
| docs-30 | 0 | 18.625 | `python3 scripts/check_baremetal_only.py --check` |
| docs-31 | 0 | 6.743 | `python3 scripts/check_baremetal_only.py --selftest` |
| docs-32 | 0 | 1.171 | `python3 scripts/ci_rv32_sdk_selftest.py` |
| docs-33 | 0 | 0.767 | `python3 scripts/ci_rv32_sdk.py --destination '$SDK'` |
| docs-34 | 0 | 2.326 | `python3 scripts/check_nvm_record_space.py` |
| docs-35 | 0 | 45.847 | `python3 scripts/check_nvm_record_space.py --self-test` |
| docs-36 | 0 | 0.816 | `python3 scripts/check_nvm_capture.py` |
| docs-37 | 0 | 75.481 | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` |
| docs-38 | 0 | 0.115 | `python3 scripts/check_soc_sources.py` |
| docs-39 | 0 | 0.214 | `python3 scripts/check_soc_sources.py --selftest` |
| docs-40 | 0 | 2.17 | `python3 sw/litex/iob_pack_selftest.py` |
| docs-41 | 0 | 1.52 | `python3 scripts/check_rtl_source_lists.py` |
| docs-42 | 0 | 2.975 | `python3 scripts/check_rtl_source_lists.py --selftest` |
| docs-43 | 0 | 0.567 | `python3 scripts/measure_naming.py --check` |
| docs-44 | 0 | 0.566 | `python3 scripts/measure_naming.py --selftest` |
| docs-45 | 0 | 2.923 | `python3 scripts/check_port_contracts.py` |
| docs-46 | 0 | 3.327 | `python3 scripts/check_port_contracts.py --selftest` |
| docs-47 | 0 | 1.677 | `python3 scripts/measure_fail_fast.py --check` |
| docs-48 | 0 | 1.669 | `python3 scripts/measure_fail_fast.py --selftest` |
| docs-49 | 0 | 1.869 | `python3 scripts/check_todo_ownership.py` |
| docs-50 | 0 | 1.921 | `python3 scripts/check_todo_ownership.py --selftest` |
| docs-51 | 0 | 6.89 | `python3 scripts/measure_test_evidence.py --check` |
| docs-52 | 0 | 6.737 | `python3 scripts/measure_test_evidence.py --selftest` |
| docs-53 | 0 | 0.466 | `python3 scripts/check_hygiene.py --check` |
| docs-54 | 0 | 0.467 | `python3 scripts/check_hygiene.py --selftest` |
| docs-55 | 0 | 0.466 | `python3 scripts/check_sv_idiom.py` |
| docs-56 | 0 | 0.515 | `python3 scripts/check_sv_idiom.py --selftest` |
| docs-57 | 0 | 1.62 | `python3 scripts/check_cpp_idiom.py` |
| docs-58 | 0 | 1.719 | `python3 scripts/check_cpp_idiom.py --selftest` |
| docs-59 | 0 | 4.178 | `python3 scripts/check_py_idiom.py` |
| docs-60 | 0 | 4.029 | `python3 scripts/check_py_idiom.py --selftest` |
| docs-61 | 0 | 0.265 | `python3 scripts/check_sh_idiom.py` |
| docs-62 | 0 | 0.264 | `python3 scripts/check_sh_idiom.py --selftest` |
| docs-63 | 0 | 0.214 | `python3 scripts/ci_events.py --check` |
| docs-64 | 0 | 17.816 | `python3 scripts/ci_events.py --selftest` |
| docs-65 | 0 | 0.114 | `python3 scripts/check_doc_paths.py` |
| docs-66 | 0 | 0.364 | `python3 scripts/check_archive.py` |
| docs-67 | 0 | 0.064 | `python3 scripts/check_archive.py --selftest` |
| docs-68 | 0 | 0.867 | `python3 scripts/gen_toc.py --selftest` |
| docs-69 | 0 | 3.023 | `python3 scripts/gen_toc.py --verify-anchors` |
| docs-70 | 0 | 5.029 | `python3 scripts/gen_toc.py --check` |
| docs-71 | 0 | 0.114 | `python3 avdecc/gen_aem_store.py --self-test` |
| docs-72 | 0 | 14.966 | `python3 scripts/check_sweep_shape.py --self-test` |
| docs-73 | 0 | 0.516 | `python3 scripts/check_deploy_shape.py --self-test` |
| docs-74 | 0 | 56.739 | `python3 scripts/check_entity_shape.py --self-test` |
| docs-archive-feature | 0 | 0.967 | `python3 scripts/check_feature_status.py` |
| docs-archive | 0 | 5.431 | `python3 scripts/docs_check.py` |
| docs-final | 0 | 5.527 | `python3 scripts/docs_check.py` |
| docs-selftest | 0 | 0.214 | `python3 scripts/docs_check.py --selftest` |
| docs-wire | 0 | 0.265 | `python3 scripts/check_wire_accountability.py --self-test` |
| em-dash-final | 0 | 3.234 | `python3 scripts/check_em_dash.py --base d8b355fe0f41d49dca6cae1cd8b3826e2edde364` |
| f3-images | 0 | 4.132 | `python3 sw/firmware/ctrl/test/ctrl_image.py --out '$SCRATCH/f3-images'` |
| image-selftest | 0 | 8.838 | `python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32` |
| images-final | 0 | 9.706 | `python3 '$SCRATCH/images.py'` |
| maap-diff | 0 | 152.335 | `python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep '$SCRATCH/maap-diff'` |
| mailbox-contract | 0 | 0.164 | `python3 sw/mailbox/gen_mailbox.py --check` |
| mailbox | 0 | 31.043 | `make -C tb/verilator/mbx -j8 VBUILD_JOBS=2` |
| new-plants-verified | 0 | 111.905 | `python3 '$SCRATCH/new_plants.py'` |
| nvm-campaign | 0 | 1829.281 | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 4` |
| park-check | 0 | 59.719 | `python3 '$SCRATCH/park_check.py'` |
| py-final | 0 | 4.175 | `python3 scripts/check_py_idiom.py` |
| reentry-oracle-correction | 0 | 8.64 | `python3 '$SCRATCH/reentry_oracle.py'` |
| review11-final | 0 | 21.13 | `python3 '$SCRATCH/review11.py'` |
| reviewer-probes | 0 | 320.71 | `python3 '$SCRATCH/review_probes.py'` |
| rv32-selftest | 0 | 7.234 | `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` |
| source-diff | 0 | 0.008 | `git diff --check 82a79638405c3365e4078da471be56758f8dd679 HEAD` |
| tally-mutants | 0 | 59.48 | `python3 sw/firmware/gtest/tally_selftest.py --mutants` |
| toc-final | 0 | 4.374 | `python3 scripts/gen_toc.py --check` |
