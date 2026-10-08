[A560]

# Round 12 gate receipts

Candidate: `efea74858dffc482820d4f19c26c38796a57ff75`. Final individual receipts: 114.

All 113 Round 11 gate entries have a passing Round 12 counterpart.
The additional independent round-11 feedback probes also pass at IF=1/2.
The builder and compiler snapshots freeze 7b47f333ecde4af16e32ca95730f56c3c454d0eb.
The candidate adds only the standing IF=1 p11 plant selection. All builder,
compiler, firmware C/C++, image and sanitizer inputs match those snapshots.
The full campaign, coverage check and final docs checks repeat at the candidate.
The mailbox export has identical inputs; the final archive contains the candidate.
ROUND12-SOURCE.json records the complete commit sequence and the one-file delta.

`$SOURCE` is the candidate checkout, `$SCRATCH` is disk scratch, and `$PACKET`
is this evidence directory. `$SDK` is the CI-pinned SDK; `$RUNTIME` contains
verified link archives. `$DOCS_ENV` supplies documentation dependencies.
`$PINNED_HDL_LIMITED` selects release 5.050, two build slots and eight inner jobs.

Each original log has a size and SHA256. Retained small logs are path-normalized
and have separate hashes. Large logs and binaries are represented by metadata only.
The initial archive-link failure was corrected and rerun; its receipt is retained
in ROUND12-DEVELOPMENT.json. It is not a final gate result.

| Entry | rc | Seconds | Exact argv (working directory in JSON) |
| --- | ---: | ---: | --- |
| asan-final | 0 | 358.618 | `python3 '$SCRATCH/asan.py'` |
| binding-probe | 0 | 24.041 | `python3 '$SCRATCH/binding_required.py'` |
| bound-table | 0 | 0.667 | `python3 '$SCRATCH/check_bounds.py'` |
| builder | 0 | 1449.073 | `env MAKEFLAGS=-j8 python3 sw/builder/test_builder.py --require-rv32` |
| campaign | 0 | 2183.883 | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir '$SCRATCH/campaign'` |
| ci-scope | 0 | 6.74 | `python3 scripts/ci_scope.py --selftest` |
| compiler-absent | 0 | 688.968 | `python3 sw/builder/test_firmware_compiler.py --absent --audit '$SCRATCH/rv32-absent.jsonl'` |
| compiler-controls | 0 | 2.74 | `python3 sw/builder/test_firmware_compiler.py --selftest` |
| compiler-pinned | 0 | 1261.735 | `python3 sw/builder/test_firmware_compiler.py --sdk-destination '$SDK' --audit '$SCRATCH/rv32-pinned.jsonl'` |
| coverage-check | 0 | 260.713 | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep '$SCRATCH/coverage-check-if1-selection'` |
| coverage-selftest | 0 | 0.817 | `python3 sw/firmware/gtest/fw_coverage.py --selftest` |
| coverage-write | 0 | 262.66 | `python3 sw/firmware/gtest/fw_coverage.py --write --jobs 4 --lwsrp third_party/lwSRP --keep '$SCRATCH/coverage-final'` |
| cpp-final | 0 | 2.072 | `python3 scripts/check_cpp_idiom.py` |
| doc-paths-final | 0 | 0.165 | `python3 scripts/check_doc_paths.py` |
| doc-style-final | 0 | 0.114 | `python3 scripts/check_doc_style.py` |
| docs-00 | 0 | 0.365 | `python3 scripts/gen_hdl_reference.py --selftest` |
| docs-01 | 0 | 1.97 | `python3 scripts/gen_hdl_reference.py --output '$SCRATCH/milan-hdl-reference'` |
| docs-02 | 0 | 6.137 | `python3 scripts/docs_check.py` |
| docs-03 | 0 | 4.63 | `python3 scripts/check_em_dash.py --base d8b355fe0f41d49dca6cae1cd8b3826e2edde364` |
| docs-04 | 0 | 0.114 | `python3 scripts/check_doc_style.py` |
| docs-05 | 0 | 0.064 | `python3 scripts/check_doc_style.py --selftest` |
| docs-06 | 0 | 0.315 | `python3 scripts/check_gptp_docs.py` |
| docs-07 | 0 | 0.315 | `python3 scripts/check_gptp_docs.py --selftest` |
| docs-08 | 0 | 0.517 | `python3 docs/DOC_MAP.gen.py --check` |
| docs-09 | 0 | 0.616 | `python3 docs/DOC_MAP.gen.py --selftest` |
| docs-10 | 0 | 0.465 | `python3 docs/diagrams/timesync_chain.gen.py --check` |
| docs-11 | 0 | 0.566 | `python3 docs/diagrams/timesync_chain.gen.py --selftest` |
| docs-12 | 0 | 0.165 | `python3 scripts/check_solution_docs.py` |
| docs-13 | 0 | 3.384 | `python3 scripts/check_solution_docs.py --selftest` |
| docs-14 | 0 | 0.566 | `python3 docs/diagrams/submodule_boundaries.gen.py --check` |
| docs-15 | 0 | 0.666 | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` |
| docs-16 | 0 | 0.617 | `python3 scripts/check_submodule_docs.py` |
| docs-17 | 0 | 0.064 | `python3 scripts/check_submodule_docs.py --selftest` |
| docs-18 | 0 | 0.215 | `python3 scripts/gen_wavedrom.py --selftest` |
| docs-19 | 0 | 0.365 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` |
| docs-20 | 0 | 0.417 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` |
| docs-21 | 0 | 0.466 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` |
| docs-22 | 0 | 0.365 | `python3 scripts/check_diagram_pngs.py` |
| docs-23 | 0 | 7.879 | `python3 scripts/check_diagram_pngs.py --selftest` |
| docs-24 | 0 | 1.22 | `python3 scripts/check_feature_status.py --self-test` |
| docs-25 | 0 | 1.318 | `python3 docs/traceability/gen_module_matrix.py --check` |
| docs-26 | 0 | 0.214 | `python3 scripts/check_gptp_docs.py --with-submodule` |
| docs-27 | 0 | 0.82 | `make -C gptp-processor docs` |
| docs-28 | 0 | 0.164 | `python3 scripts/measure_control_flow.py --selftest` |
| docs-29 | 0 | 0.064 | `python3 scripts/measure_cohesion.py --selftest` |
| docs-30 | 0 | 20.18 | `python3 scripts/check_baremetal_only.py --check` |
| docs-31 | 0 | 9.221 | `python3 scripts/check_baremetal_only.py --selftest` |
| docs-32 | 0 | 1.593 | `python3 scripts/ci_rv32_sdk_selftest.py` |
| docs-33 | 0 | 2.133 | `python3 scripts/ci_rv32_sdk.py --destination '$SDK'` |
| docs-34 | 0 | 2.884 | `python3 scripts/check_nvm_record_space.py` |
| docs-35 | 0 | 52.937 | `python3 scripts/check_nvm_record_space.py --self-test` |
| docs-36 | 0 | 0.967 | `python3 scripts/check_nvm_capture.py` |
| docs-37 | 0 | 89.864 | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` |
| docs-38 | 0 | 0.165 | `python3 scripts/check_soc_sources.py` |
| docs-39 | 0 | 0.265 | `python3 scripts/check_soc_sources.py --selftest` |
| docs-40 | 0 | 2.726 | `python3 sw/litex/iob_pack_selftest.py` |
| docs-41 | 0 | 1.769 | `python3 scripts/check_rtl_source_lists.py` |
| docs-42 | 0 | 3.686 | `python3 scripts/check_rtl_source_lists.py --selftest` |
| docs-43 | 0 | 0.565 | `python3 scripts/measure_naming.py --check` |
| docs-44 | 0 | 0.566 | `python3 scripts/measure_naming.py --selftest` |
| docs-45 | 0 | 3.024 | `python3 scripts/check_port_contracts.py` |
| docs-46 | 0 | 3.676 | `python3 scripts/check_port_contracts.py --selftest` |
| docs-47 | 0 | 1.719 | `python3 scripts/measure_fail_fast.py --check` |
| docs-48 | 0 | 1.823 | `python3 scripts/measure_fail_fast.py --selftest` |
| docs-49 | 0 | 2.071 | `python3 scripts/check_todo_ownership.py` |
| docs-50 | 0 | 2.22 | `python3 scripts/check_todo_ownership.py --selftest` |
| docs-51 | 0 | 7.545 | `python3 scripts/measure_test_evidence.py --check` |
| docs-52 | 0 | 7.093 | `python3 scripts/measure_test_evidence.py --selftest` |
| docs-53 | 0 | 0.415 | `python3 scripts/check_hygiene.py --check` |
| docs-54 | 0 | 0.416 | `python3 scripts/check_hygiene.py --selftest` |
| docs-55 | 0 | 0.516 | `python3 scripts/check_sv_idiom.py` |
| docs-56 | 0 | 0.469 | `python3 scripts/check_sv_idiom.py --selftest` |
| docs-57 | 0 | 1.72 | `python3 scripts/check_cpp_idiom.py` |
| docs-58 | 0 | 1.87 | `python3 scripts/check_cpp_idiom.py --selftest` |
| docs-59 | 0 | 4.276 | `python3 scripts/check_py_idiom.py` |
| docs-60 | 0 | 4.278 | `python3 scripts/check_py_idiom.py --selftest` |
| docs-61 | 0 | 0.265 | `python3 scripts/check_sh_idiom.py` |
| docs-62 | 0 | 0.265 | `python3 scripts/check_sh_idiom.py --selftest` |
| docs-63 | 0 | 0.315 | `python3 scripts/ci_events.py --check` |
| docs-64 | 0 | 18.722 | `python3 scripts/ci_events.py --selftest` |
| docs-65 | 0 | 0.114 | `python3 scripts/check_doc_paths.py` |
| docs-66 | 0 | 0.415 | `python3 scripts/check_archive.py` |
| docs-67 | 0 | 0.064 | `python3 scripts/check_archive.py --selftest` |
| docs-68 | 0 | 0.869 | `python3 scripts/gen_toc.py --selftest` |
| docs-69 | 0 | 3.575 | `python3 scripts/gen_toc.py --verify-anchors` |
| docs-70 | 0 | 5.181 | `python3 scripts/gen_toc.py --check` |
| docs-71 | 0 | 0.114 | `python3 avdecc/gen_aem_store.py --self-test` |
| docs-72 | 0 | 19.551 | `python3 scripts/check_sweep_shape.py --self-test` |
| docs-73 | 0 | 0.566 | `python3 scripts/check_deploy_shape.py --self-test` |
| docs-74 | 0 | 69.705 | `python3 scripts/check_entity_shape.py --self-test` |
| docs-archive-feature | 0 | 1.017 | `python3 scripts/check_feature_status.py` |
| docs-archive | 0 | 6.184 | `python3 scripts/docs_check.py` |
| docs-final | 0 | 6.434 | `python3 scripts/docs_check.py` |
| docs-selftest | 0 | 0.265 | `python3 scripts/docs_check.py --selftest` |
| docs-wire | 0 | 0.466 | `python3 scripts/check_wire_accountability.py --self-test` |
| em-dash-final | 0 | 5.636 | `python3 scripts/check_em_dash.py --base d8b355fe0f41d49dca6cae1cd8b3826e2edde364` |
| f3-images | 0 | 5.331 | `python3 sw/firmware/ctrl/test/ctrl_image.py --out '$SCRATCH/f3-images'` |
| image-selftest | 0 | 14.451 | `python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32` |
| images-final | 0 | 12.666 | `python3 '$SCRATCH/images.py'` |
| maap-diff | 0 | 183.131 | `python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep '$SCRATCH/maap-diff'` |
| mailbox-contract | 0 | 0.265 | `python3 sw/mailbox/gen_mailbox.py --check` |
| mailbox | 0 | 38.858 | `make -C tb/verilator/mbx -j8 VBUILD_JOBS=2` |
| new-plants-final | 0 | 163.036 | `python3 '$SCRATCH/new_plants.py'` |
| nvm-campaign | 0 | 2330.013 | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 4` |
| park-check | 0 | 65.516 | `python3 '$SCRATCH/park_check.py'` |
| py-final | 0 | 5.53 | `python3 scripts/check_py_idiom.py` |
| reentry-oracle | 0 | 13.26 | `python3 '$SCRATCH/reentry_oracle.py'` |
| review11-final | 0 | 27.63 | `python3 '$SCRATCH/review11.py'` |
| review12-final | 0 | 28.72 | `python3 '$SCRATCH/review12.py'` |
| reviewer-probes | 0 | 393.39 | `python3 '$SCRATCH/review_probes.py'` |
| rv32-selftest | 0 | 10.2 | `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` |
| source-diff | 0 | 0.064 | `git diff --check 82a79638405c3365e4078da471be56758f8dd679 HEAD` |
| tally-mutants | 0 | 84.374 | `python3 sw/firmware/gtest/tally_selftest.py --mutants` |
| toc-final | 0 | 6.285 | `python3 scripts/gen_toc.py --check` |
