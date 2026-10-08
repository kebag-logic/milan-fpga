[A560]

# Round 5 gate receipts

Head: `500b8f64443777685e6a54049d933476710d26f0`. All final commands exit 0. Commands ran without pipelines. `ROUND5-GATES.json` records raw log hashes and sizes separately from retained normalized logs. `$SOURCE` is the candidate, `$SCRATCH` is disk scratch, `$SDK` is the pinned RV32 SDK, `$CGREEN` is the host unit-test dependency prefix, `$DOCS_ENV` is the documentation environment, `$LWSRP` is the separate dependency clone, `$RUNTIME` is the verified freestanding runtime, and `$ARCHIVE` is a tracked export of this exact parent commit with no Git metadata.

The 76 documentation-bank entries exclude the manager-owned compiler-absent entry; the compiler self-test remains included. Builder-bank results are not claimed here. Source bytes and pins were checked after all commands; final standalone firmware positives were run after documentation fault controls restored their inputs.

| Receipt | Command | rc | Seconds | Working directory |
|---|---|---:|---:|---|
| `firmware-final` | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir $SCRATCH/firmware-final` | 0 | 443.262 | `$SOURCE` |
| `firmware-positive-final` | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --jobs 4 --build-dir $SCRATCH/firmware-positive-final` | 0 | 153.706 | `$SOURCE` |
| `coverage-final` | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep $SCRATCH/coverage-final` | 0 | 173.53 | `$SOURCE` |
| `firmware-nvm` | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | 98.629 | `$SOURCE` |
| `coverage-selftest` | `python3 sw/firmware/gtest/fw_coverage.py --selftest` | 0 | 0.465 | `$SOURCE` |
| `rv32-selftest` | `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | 0 | 4.996 | `$SOURCE` |
| `tally-mutants` | `python3 sw/firmware/gtest/tally_selftest.py --mutants` | 0 | 59.325 | `$SOURCE` |
| `mailbox-contract` | `python3 sw/mailbox/gen_mailbox.py --check` | 0 | 0.165 | `$SOURCE` |
| `mailbox-final` | `make -C $SCRATCH/mailbox/tb/verilator/mbx -j2 VERILATOR=$SCRATCH_PARENT/verilator-j8` | 0 | 61.918 | `$SOURCE` |
| `upstream-positive` | `python3 $SCRATCH/upstream_positive.py` | 0 | 3.826 | `$SOURCE` |
| `upstream-reversals-off` | `python3 $LWSRP/tests/check_reversals.py --work-dir $SCRATCH/reversals-off --prefix $CGREEN --milan OFF` | 0 | 87.781 | `$SOURCE` |
| `upstream-reversals-on` | `python3 $LWSRP/tests/check_reversals.py --work-dir $SCRATCH/reversals-on --prefix $CGREEN --milan ON` | 0 | 87.87 | `$SOURCE` |
| `upstream-doc-sentences` | `python3 $LWSRP/doc/tools/check_sentences.py` | 0 | 0.064 | `$LWSRP` |
| `upstream-doc-references` | `python3 $LWSRP/doc/tools/check_references.py` | 0 | 0.114 | `$LWSRP` |
| `upstream-doc-reference-selftest` | `python3 $LWSRP/doc/tools/check_references.py --self-test` | 0 | 0.064 | `$LWSRP` |
| `upstream-doc-links` | `python3 $LWSRP/doc/tools/check_links.py` | 0 | 2.721 | `$LWSRP` |
| `docs-00` | `python3 scripts/gen_hdl_reference.py --selftest` | 0 | 0.265 | `$SOURCE` |
| `docs-01` | `python3 scripts/gen_hdl_reference.py --output $SCRATCH/milan-hdl-reference` | 0 | 2.022 | `$SOURCE` |
| `docs-02` | `python3 scripts/docs_check.py` | 0 | 6.385 | `$SOURCE` |
| `docs-03` | `python3 scripts/check_em_dash.py --base 6f7deea15a9160761b30aaa93fe152f20d416695` | 0 | 3.673 | `$SOURCE` |
| `docs-04` | `python3 scripts/check_doc_style.py` | 0 | 0.064 | `$SOURCE` |
| `docs-05` | `python3 scripts/check_doc_style.py --selftest` | 0 | 0.064 | `$SOURCE` |
| `docs-06` | `python3 scripts/check_gptp_docs.py` | 0 | 0.215 | `$SOURCE` |
| `docs-07` | `python3 scripts/check_gptp_docs.py --selftest` | 0 | 0.264 | `$SOURCE` |
| `docs-08` | `python3 docs/DOC_MAP.gen.py --check` | 0 | 0.465 | `$SOURCE` |
| `docs-09` | `python3 docs/DOC_MAP.gen.py --selftest` | 0 | 0.515 | `$SOURCE` |
| `docs-10` | `python3 docs/diagrams/timesync_chain.gen.py --check` | 0 | 0.415 | `$SOURCE` |
| `docs-11` | `python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 | 0.515 | `$SOURCE` |
| `docs-12` | `python3 scripts/check_solution_docs.py` | 0 | 0.164 | `$SOURCE` |
| `docs-13` | `python3 scripts/check_solution_docs.py --selftest` | 0 | 3.02 | `$SOURCE` |
| `docs-14` | `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | 0.465 | `$SOURCE` |
| `docs-15` | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 | 0.565 | `$SOURCE` |
| `docs-16` | `python3 scripts/check_submodule_docs.py` | 0 | 0.565 | `$SOURCE` |
| `docs-17` | `python3 scripts/check_submodule_docs.py --selftest` | 0 | 0.064 | `$SOURCE` |
| `docs-18` | `python3 scripts/gen_wavedrom.py --selftest` | 0 | 0.164 | `$SOURCE` |
| `docs-19` | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | 0 | 0.315 | `$SOURCE` |
| `docs-20` | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | 0 | 0.415 | `$SOURCE` |
| `docs-21` | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | 0 | 0.365 | `$SOURCE` |
| `docs-22` | `python3 scripts/check_diagram_pngs.py` | 0 | 0.415 | `$SOURCE` |
| `docs-23` | `python3 scripts/check_diagram_pngs.py --selftest` | 0 | 7.342 | `$SOURCE` |
| `docs-24` | `python3 scripts/check_feature_status.py --self-test` | 0 | 1.016 | `$SOURCE` |
| `docs-25` | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | 1.274 | `$SOURCE` |
| `docs-26` | `python3 scripts/check_gptp_docs.py --with-submodule` | 0 | 0.214 | `$SOURCE` |
| `docs-27` | `make -C gptp-processor docs` | 0 | 0.816 | `$SOURCE` |
| `docs-28` | `python3 scripts/measure_control_flow.py --selftest` | 0 | 0.165 | `$SOURCE` |
| `docs-29` | `python3 scripts/measure_cohesion.py --selftest` | 0 | 0.064 | `$SOURCE` |
| `docs-30` | `python3 scripts/check_baremetal_only.py --check` | 0 | 19.821 | `$SOURCE` |
| `docs-31` | `python3 scripts/check_baremetal_only.py --selftest` | 0 | 7.594 | `$SOURCE` |
| `docs-32` | `python3 scripts/ci_rv32_sdk_selftest.py` | 0 | 1.267 | `$SOURCE` |
| `docs-33` | `python3 scripts/ci_rv32_sdk.py --destination $SDK` | 0 | 1.969 | `$SOURCE` |
| `docs-34` | `python3 sw/builder/test_firmware_compiler.py --selftest` | 0 | 1.97 | `$SOURCE` |
| `docs-35` | `python3 scripts/check_nvm_record_space.py` | 0 | 2.571 | `$SOURCE` |
| `docs-36` | `python3 scripts/check_nvm_record_space.py --self-test` | 0 | 50.484 | `$SOURCE` |
| `docs-37` | `python3 scripts/check_nvm_capture.py` | 0 | 0.966 | `$SOURCE` |
| `docs-38` | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | 79.778 | `$SOURCE` |
| `docs-39` | `python3 scripts/check_soc_sources.py` | 0 | 0.164 | `$SOURCE` |
| `docs-40` | `python3 scripts/check_soc_sources.py --selftest` | 0 | 0.265 | `$SOURCE` |
| `docs-41` | `python3 sw/litex/iob_pack_selftest.py` | 0 | 2.426 | `$SOURCE` |
| `docs-42` | `python3 scripts/check_rtl_source_lists.py` | 0 | 1.725 | `$SOURCE` |
| `docs-43` | `python3 scripts/check_rtl_source_lists.py --selftest` | 0 | 3.276 | `$SOURCE` |
| `docs-44` | `python3 scripts/measure_naming.py --check` | 0 | 0.519 | `$SOURCE` |
| `docs-45` | `python3 scripts/measure_naming.py --selftest` | 0 | 0.566 | `$SOURCE` |
| `docs-46` | `python3 scripts/check_port_contracts.py` | 0 | 2.874 | `$SOURCE` |
| `docs-47` | `python3 scripts/check_port_contracts.py --selftest` | 0 | 3.425 | `$SOURCE` |
| `docs-48` | `python3 scripts/measure_fail_fast.py --check` | 0 | 1.723 | `$SOURCE` |
| `docs-49` | `python3 scripts/measure_fail_fast.py --selftest` | 0 | 1.721 | `$SOURCE` |
| `docs-50` | `python3 scripts/check_todo_ownership.py` | 0 | 1.92 | `$SOURCE` |
| `docs-51` | `python3 scripts/check_todo_ownership.py --selftest` | 0 | 1.921 | `$SOURCE` |
| `docs-52` | `python3 scripts/measure_test_evidence.py --check` | 0 | 7.086 | `$SOURCE` |
| `docs-53` | `python3 scripts/measure_test_evidence.py --selftest` | 0 | 7.144 | `$SOURCE` |
| `docs-54` | `python3 scripts/check_hygiene.py --check` | 0 | 0.417 | `$SOURCE` |
| `docs-55` | `python3 scripts/check_hygiene.py --selftest` | 0 | 0.415 | `$SOURCE` |
| `docs-56` | `python3 scripts/check_sv_idiom.py` | 0 | 0.516 | `$SOURCE` |
| `docs-57` | `python3 scripts/check_sv_idiom.py --selftest` | 0 | 0.515 | `$SOURCE` |
| `docs-58` | `python3 scripts/check_cpp_idiom.py` | 0 | 1.672 | `$SOURCE` |
| `docs-59` | `python3 scripts/check_cpp_idiom.py --selftest` | 0 | 1.821 | `$SOURCE` |
| `docs-60` | `python3 scripts/check_py_idiom.py` | 0 | 4.838 | `$SOURCE` |
| `docs-61` | `python3 scripts/check_py_idiom.py --selftest` | 0 | 4.68 | `$SOURCE` |
| `docs-62` | `python3 scripts/check_sh_idiom.py` | 0 | 0.265 | `$SOURCE` |
| `docs-63` | `python3 scripts/check_sh_idiom.py --selftest` | 0 | 0.265 | `$SOURCE` |
| `docs-64` | `python3 scripts/ci_events.py --check` | 0 | 0.265 | `$SOURCE` |
| `docs-65` | `python3 scripts/ci_events.py --selftest` | 0 | 18.545 | `$SOURCE` |
| `docs-66` | `python3 scripts/check_doc_paths.py` | 0 | 0.114 | `$SOURCE` |
| `docs-67` | `python3 scripts/check_archive.py` | 0 | 0.415 | `$SOURCE` |
| `docs-68` | `python3 scripts/check_archive.py --selftest` | 0 | 0.064 | `$SOURCE` |
| `docs-69` | `python3 scripts/gen_toc.py --selftest` | 0 | 0.967 | `$SOURCE` |
| `docs-70` | `python3 scripts/gen_toc.py --verify-anchors` | 0 | 3.273 | `$SOURCE` |
| `docs-71` | `python3 scripts/gen_toc.py --check` | 0 | 5.035 | `$SOURCE` |
| `docs-72` | `python3 avdecc/gen_aem_store.py --self-test` | 0 | 0.114 | `$SOURCE` |
| `docs-73` | `python3 scripts/check_sweep_shape.py --self-test` | 0 | 16.668 | `$SOURCE` |
| `docs-74` | `python3 scripts/check_deploy_shape.py --self-test` | 0 | 0.465 | `$SOURCE` |
| `docs-75` | `python3 scripts/check_entity_shape.py --self-test` | 0 | 58.936 | `$SOURCE` |
| `docs-selftest` | `python3 scripts/docs_check.py --selftest` | 0 | 0.214 | `$SOURCE` |
| `docs-wire` | `python3 scripts/check_wire_accountability.py --self-test` | 0 | 0.315 | `$SOURCE` |
| `em-dash-final` | `python3 scripts/check_em_dash.py --base 6f7deea15a9160761b30aaa93fe152f20d416695` | 0 | 3.727 | `$SOURCE` |
| `docs-final` | `python3 scripts/docs_check.py` | 0 | 5.703 | `$SOURCE` |
| `source-diff` | `git diff --check 6f7deea15a9160761b30aaa93fe152f20d416695 HEAD` | 0 | 0.008 | `$SOURCE` |
| `ci-scope` | `python3 scripts/ci_scope.py --selftest` | 0 | 5.437 | `$SOURCE` |
| `docs-archive` | `python3 scripts/docs_check.py` | 0 | 5.831 | `$ARCHIVE` |
| `docs-archive-feature` | `python3 scripts/check_feature_status.py` | 0 | 1.118 | `$ARCHIVE` |
| `hdl-reference-final` | `python3 scripts/gen_hdl_reference.py --output $SCRATCH/milan-hdl-reference-final` | 0 | 1.818 | `$SOURCE` |
| `linked-size-final` | `python3 $SCRATCH/images.py` | 0 | 7.15 | `$SOURCE` |

## Expanded helper commands

The linked-size helper checks every runtime provenance hash, then executes `python3 sw/firmware/ctrl/test/ctrl_image.py --config configs/<shape>.yaml --output $SCRATCH/image-<shape>-if<N> --interfaces <N> --libc $RUNTIME/libc.a --compiler-runtime $RUNTIME/libcompiler_rt.a` for both `endstation_ax7101_1x1_tdm8` and `endstation_ax7101_8x8`, at N=1 and N=2. All four commands exit 0.

The dependency-positive helper runs the following for PROFILE=OFF and PROFILE=ON, in `$LWSRP` at `ced667d8ee35929ab5f9e77a1c5396e173a693d8`:

```sh
cmake -S "$LWSRP" -B "$SCRATCH/upstream-$PROFILE" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_PREFIX_PATH="$CGREEN" -DLWSRP_MILAN="$PROFILE"
cmake --build "$SCRATCH/upstream-$PROFILE" --parallel 2
ctest --test-dir "$SCRATCH/upstream-$PROFILE" --output-on-failure
"$SCRATCH/upstream-$PROFILE/unit_tests"
SHLAN_LIBRARY="$SCRATCH/upstream-$PROFILE/libshlan.so" behave --no-capture -f plain
```

`LD_LIBRARY_PATH` points to `$CGREEN/lib`. The recorded helper uses lower-case profile directory names. No production source differs from the public parent pin. The mailbox copy contains byte-identical tracked inputs recorded in `ROUND5-MAILBOX-SOURCE.json`; its wrapper replaces unbounded inner jobs with eight and permits at most two simultaneous HDL builds, using release 5.050.
