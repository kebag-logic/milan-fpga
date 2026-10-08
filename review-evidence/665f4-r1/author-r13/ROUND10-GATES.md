[A560]

# Round 10 gate receipts

Candidate: `82a79638405c3365e4078da471be56758f8dd679`. Final individual receipts: 110.

`$SOURCE` is the candidate checkout; `$SCRATCH` is disk scratch; `$BUILDER_TREE` is the detached scratch checkout at `da36eb15f38d23aa4cddc9183e62e0a94f339dd9`; the final commit updates the coverage ratchet, one test fixture, the IF=1 mutation selection and header prose. Production behavior and builder inputs are unchanged. Final coverage and sanitizer checks include the expanded fixture. `$SDK` is the CI-pinned SDK, `$RUNTIME` contains verified link archives, and `$DOCS_ENV` supplies documentation dependencies. `$PINNED_HDL_LIMITED` runs release 5.050 with two build slots and inner jobs limited to eight. These aliases are locations, not bundled dependencies.

Every receipt records the original log size and SHA256. Small retained logs are path-normalized and have their own hash; large logs remain hash/size only. The JSON distinguishes these two byte streams. Superseded development attempts are separate in `ROUND10-DEVELOPMENT.json`.

Long invocations ran detached with an individual log and rc file, followed by bounded foreground waits. The table does not claim a result for an invocation still running.

| Entry | rc | Seconds | Exact argv (working directory in JSON) |
| --- | ---: | ---: | --- |
| asan | 0 | 172.655 | `python3 '$SCRATCH/asan.py'` |
| binding-probe | 0 | 20.82 | `python3 '$SCRATCH/binding_required.py'` |
| bound-table | 0 | 0.772 | `python3 '$SCRATCH/check_bounds.py'` |
| builder | 0 | 1279.723 | `env MAKEFLAGS=-j8 python3 sw/builder/test_builder.py --require-rv32` |
| campaign-final | 0 | 1756.434 | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir '$SCRATCH/campaign-final'` |
| ci-scope | 0 | 5.943 | `python3 scripts/ci_scope.py --selftest` |
| compiler-absent | 0 | 573.4 | `python3 sw/builder/test_firmware_compiler.py --absent --audit '$SCRATCH/rv32-absent.jsonl'` |
| compiler-controls | 0 | 2.018 | `python3 sw/builder/test_firmware_compiler.py --selftest` |
| compiler-pinned | 0 | 1084.719 | `python3 sw/builder/test_firmware_compiler.py --sdk-destination '$SDK' --audit '$SCRATCH/rv32-pinned.jsonl'` |
| coverage-check | 0 | 241.669 | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep '$SCRATCH/coverage-check'` |
| coverage-selftest | 0 | 0.565 | `python3 sw/firmware/gtest/fw_coverage.py --selftest` |
| coverage-write-final | 0 | 242.994 | `python3 sw/firmware/gtest/fw_coverage.py --write --jobs 4 --keep '$SCRATCH/coverage-write-final'` |
| cpp-final | 0 | 1.871 | `python3 scripts/check_cpp_idiom.py` |
| doc-paths-final | 0 | 0.114 | `python3 scripts/check_doc_paths.py` |
| doc-style-final | 0 | 0.064 | `python3 scripts/check_doc_style.py` |
| docs-00 | 0 | 0.424 | `python3 scripts/gen_hdl_reference.py --selftest` |
| docs-01 | 0 | 2.88 | `python3 scripts/gen_hdl_reference.py --output '$SCRATCH/milan-hdl-reference'` |
| docs-02 | 0 | 7.115 | `python3 scripts/docs_check.py` |
| docs-03 | 0 | 9.31 | `python3 scripts/check_em_dash.py --base d8b355fe0f41d49dca6cae1cd8b3826e2edde364` |
| docs-04 | 0 | 0.065 | `python3 scripts/check_doc_style.py` |
| docs-05 | 0 | 0.119 | `python3 scripts/check_doc_style.py --selftest` |
| docs-06 | 0 | 0.267 | `python3 scripts/check_gptp_docs.py` |
| docs-07 | 0 | 0.269 | `python3 scripts/check_gptp_docs.py --selftest` |
| docs-08 | 0 | 0.821 | `python3 docs/DOC_MAP.gen.py --check` |
| docs-09 | 0 | 0.824 | `python3 docs/DOC_MAP.gen.py --selftest` |
| docs-10 | 0 | 0.824 | `python3 docs/diagrams/timesync_chain.gen.py --check` |
| docs-11 | 0 | 0.973 | `python3 docs/diagrams/timesync_chain.gen.py --selftest` |
| docs-12 | 0 | 0.166 | `python3 scripts/check_solution_docs.py` |
| docs-13 | 0 | 3.231 | `python3 scripts/check_solution_docs.py --selftest` |
| docs-14 | 0 | 0.768 | `python3 docs/diagrams/submodule_boundaries.gen.py --check` |
| docs-15 | 0 | 0.868 | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` |
| docs-16 | 0 | 1.31 | `python3 scripts/check_submodule_docs.py` |
| docs-17 | 0 | 0.12 | `python3 scripts/check_submodule_docs.py --selftest` |
| docs-18 | 0 | 0.273 | `python3 scripts/gen_wavedrom.py --selftest` |
| docs-19 | 0 | 0.673 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` |
| docs-20 | 0 | 0.775 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` |
| docs-21 | 0 | 0.675 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` |
| docs-22 | 0 | 0.672 | `python3 scripts/check_diagram_pngs.py` |
| docs-23 | 0 | 11.444 | `python3 scripts/check_diagram_pngs.py --selftest` |
| docs-24 | 0 | 1.292 | `python3 scripts/check_feature_status.py --self-test` |
| docs-25 | 0 | 1.799 | `python3 docs/traceability/gen_module_matrix.py --check` |
| docs-26 | 0 | 0.469 | `python3 scripts/check_gptp_docs.py --with-submodule` |
| docs-27 | 0 | 1.482 | `make -C gptp-processor docs` |
| docs-28 | 0 | 0.368 | `python3 scripts/measure_control_flow.py --selftest` |
| docs-29 | 0 | 0.116 | `python3 scripts/measure_cohesion.py --selftest` |
| docs-30 | 0 | 23.11 | `python3 scripts/check_baremetal_only.py --check` |
| docs-31 | 0 | 17.556 | `python3 scripts/check_baremetal_only.py --selftest` |
| docs-32 | 0 | 3.002 | `python3 scripts/ci_rv32_sdk_selftest.py` |
| docs-33 | 0 | 1.021 | `python3 scripts/ci_rv32_sdk.py --destination '$SDK'` |
| docs-34 | 0 | 3.936 | `python3 scripts/check_nvm_record_space.py` |
| docs-35 | 0 | 58.101 | `python3 scripts/check_nvm_record_space.py --self-test` |
| docs-36 | 0 | 1.324 | `python3 scripts/check_nvm_capture.py` |
| docs-37 | 0 | 91.666 | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` |
| docs-38 | 0 | 0.265 | `python3 scripts/check_soc_sources.py` |
| docs-39 | 0 | 0.316 | `python3 scripts/check_soc_sources.py --selftest` |
| docs-40 | 0 | 5.04 | `python3 sw/litex/iob_pack_selftest.py` |
| docs-41 | 0 | 2.174 | `python3 scripts/check_rtl_source_lists.py` |
| docs-42 | 0 | 3.397 | `python3 scripts/check_rtl_source_lists.py --selftest` |
| docs-43 | 0 | 0.569 | `python3 scripts/measure_naming.py --check` |
| docs-44 | 0 | 0.518 | `python3 scripts/measure_naming.py --selftest` |
| docs-45 | 0 | 2.779 | `python3 scripts/check_port_contracts.py` |
| docs-46 | 0 | 3.231 | `python3 scripts/check_port_contracts.py --selftest` |
| docs-47 | 0 | 2.027 | `python3 scripts/measure_fail_fast.py --check` |
| docs-48 | 0 | 2.596 | `python3 scripts/measure_fail_fast.py --selftest` |
| docs-49 | 0 | 1.885 | `python3 scripts/check_todo_ownership.py` |
| docs-50 | 0 | 1.933 | `python3 scripts/check_todo_ownership.py --selftest` |
| docs-51 | 0 | 7.288 | `python3 scripts/measure_test_evidence.py --check` |
| docs-52 | 0 | 7.188 | `python3 scripts/measure_test_evidence.py --selftest` |
| docs-53 | 0 | 0.416 | `python3 scripts/check_hygiene.py --check` |
| docs-54 | 0 | 0.416 | `python3 scripts/check_hygiene.py --selftest` |
| docs-55 | 0 | 0.465 | `python3 scripts/check_sv_idiom.py` |
| docs-56 | 0 | 0.568 | `python3 scripts/check_sv_idiom.py --selftest` |
| docs-57 | 0 | 1.721 | `python3 scripts/check_cpp_idiom.py` |
| docs-58 | 0 | 1.925 | `python3 scripts/check_cpp_idiom.py --selftest` |
| docs-59 | 0 | 4.129 | `python3 scripts/check_py_idiom.py` |
| docs-60 | 0 | 4.176 | `python3 scripts/check_py_idiom.py --selftest` |
| docs-61 | 0 | 0.265 | `python3 scripts/check_sh_idiom.py` |
| docs-62 | 0 | 0.265 | `python3 scripts/check_sh_idiom.py --selftest` |
| docs-63 | 0 | 0.215 | `python3 scripts/ci_events.py --check` |
| docs-64 | 0 | 18.882 | `python3 scripts/ci_events.py --selftest` |
| docs-65 | 0 | 0.115 | `python3 scripts/check_doc_paths.py` |
| docs-66 | 0 | 0.416 | `python3 scripts/check_archive.py` |
| docs-67 | 0 | 0.065 | `python3 scripts/check_archive.py --selftest` |
| docs-68 | 0 | 0.968 | `python3 scripts/gen_toc.py --selftest` |
| docs-69 | 0 | 3.075 | `python3 scripts/gen_toc.py --verify-anchors` |
| docs-70 | 0 | 5.335 | `python3 scripts/gen_toc.py --check` |
| docs-71 | 0 | 0.216 | `python3 avdecc/gen_aem_store.py --self-test` |
| docs-72 | 0 | 17.823 | `python3 scripts/check_sweep_shape.py --self-test` |
| docs-73 | 0 | 0.871 | `python3 scripts/check_deploy_shape.py --self-test` |
| docs-74 | 0 | 60.881 | `python3 scripts/check_entity_shape.py --self-test` |
| docs-archive-feature | 0 | 1.068 | `python3 scripts/check_feature_status.py` |
| docs-archive | 0 | 6.033 | `python3 scripts/docs_check.py` |
| docs-final | 0 | 6.135 | `python3 scripts/docs_check.py` |
| docs-selftest | 0 | 0.215 | `python3 scripts/docs_check.py --selftest` |
| docs-wire | 0 | 0.315 | `python3 scripts/check_wire_accountability.py --self-test` |
| em-dash-final | 0 | 3.78 | `python3 scripts/check_em_dash.py --base d8b355fe0f41d49dca6cae1cd8b3826e2edde364` |
| f3-images | 0 | 4.529 | `python3 sw/firmware/ctrl/test/ctrl_image.py --out '$SCRATCH/f3-images'` |
| image-selftest | 0 | 9.184 | `python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32` |
| images | 0 | 9.95 | `python3 '$SCRATCH/images.py'` |
| maap-diff | 0 | 151.377 | `python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep '$SCRATCH/maap-diff'` |
| mailbox-contract | 0 | 0.165 | `python3 sw/mailbox/gen_mailbox.py --check` |
| mailbox | 0 | 46.586 | `make -C tb/verilator/mbx -j8 VBUILD_JOBS=2` |
| nvm-campaign | 0 | 2014.433 | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 4` |
| park-check | 0 | 54.017 | `python3 '$SCRATCH/park_check.py'` |
| py-final | 0 | 4.934 | `python3 scripts/check_py_idiom.py` |
| reviewer-probes | 0 | 340.322 | `python3 '$SCRATCH/review_probes.py'` |
| rv32-selftest | 0 | 7.53 | `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` |
| source-diff | 0 | 0.008 | `git diff --check edeef61c5a0cc6c18caa61db4019a8e378baf366 HEAD` |
| tally-mutants | 0 | 62.277 | `python3 sw/firmware/gtest/tally_selftest.py --mutants` |
| toc-final | 0 | 5.181 | `python3 scripts/gen_toc.py --check` |
