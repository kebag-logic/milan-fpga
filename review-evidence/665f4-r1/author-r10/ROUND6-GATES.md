[A560]

# Round 6 gates

Head: `cce554f64f6bdab1f6d26e5c4d7b46d54d228c52`. All 98 final invocations exited 0 without pipelines. The two firmware shards jointly cover every control plant; each also runs the full SRP campaign and all positives. Repeated SRP plants are counted once. The 75 documentation-bank entries exclude the manager-owned compiler-absent check. Builder-bank evidence remains manager-owned.

`$SOURCE` is the candidate checkout, `$SCRATCH` is disk scratch, `$SDK` is the CI-pinned ilp32d SDK, `$RUNTIME` is the verified freestanding runtime, `$DOCS_ENV` is the documentation environment, `$CGREEN` is the dependency test prefix, `$HDL_TOOLS` provides release 5.050, and `$ARCHIVE` is the exact committed source without Git metadata. Helpers are retained under `round6-helpers/`; set these variables and invoke each helper through Python.

| Receipt | Command | rc | Seconds | Working directory |
|---|---|---:|---:|---|
| `firmware-shard0-final` | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --mutation-shard 0 2 --jobs 4 --build-dir $SCRATCH/firmware-shard0` | 0 | 551.257 | `$SOURCE` |
| `firmware-shard1-final` | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --mutation-shard 1 2 --jobs 4 --build-dir $SCRATCH/firmware-shard1` | 0 | 542.885 | `$SOURCE` |
| `coverage-check` | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep $SCRATCH/coverage-check` | 0 | 199.728 | `$SOURCE` |
| `firmware-nvm` | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | 97.097 | `$SOURCE` |
| `coverage-selftest` | `python3 sw/firmware/gtest/fw_coverage.py --selftest` | 0 | 0.417 | `$SOURCE` |
| `rv32-selftest` | `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | 0 | 5.636 | `$SOURCE` |
| `tally-mutants` | `python3 sw/firmware/gtest/tally_selftest.py --mutants` | 0 | 52.614 | `$SOURCE` |
| `mailbox-contract` | `python3 sw/mailbox/gen_mailbox.py --check` | 0 | 0.165 | `$SOURCE` |
| `mailbox` | `make -C $SCRATCH/mailbox/tb/verilator/mbx -j2 VBUILD_JOBS=8 VERILATOR=$SCRATCH_PARENT/verilator-j8` | 0 | 57.368 | `$SOURCE` |
| `maap-differential` | `python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep $SCRATCH/maap-diff` | 0 | 142.353 | `$SOURCE` |
| `upstream-positive` | `python3 $SCRATCH/upstream_positive.py` | 0 | 3.376 | `$SOURCE` |
| `reviewer-probes-final` | `python3 $SCRATCH/probes.py` | 0 | 12.105 | `$SOURCE` |
| `reviewer-retry-control` | `python3 $SCRATCH/probe_control.py` | 0 | 11.451 | `$SOURCE` |
| `linked-size-final` | `python3 $SCRATCH/images.py` | 0 | 8.455 | `$SOURCE` |
| `docs-00` | `python3 scripts/gen_hdl_reference.py --selftest` | 0 | 0.315 | `$SOURCE` |
| `docs-01` | `python3 scripts/gen_hdl_reference.py --output $SCRATCH/milan-hdl-reference` | 0 | 1.919 | `$SOURCE` |
| `docs-02` | `python3 scripts/docs_check.py` | 0 | 6.083 | `$SOURCE` |
| `docs-03` | `python3 scripts/check_em_dash.py --base e21c1ca024d37ea188ad15b5c8f9c2dae18628df` | 0 | 3.627 | `$SOURCE` |
| `docs-05` | `python3 scripts/check_doc_style.py --selftest` | 0 | 0.064 | `$SOURCE` |
| `docs-06` | `python3 scripts/check_gptp_docs.py` | 0 | 0.215 | `$SOURCE` |
| `docs-07` | `python3 scripts/check_gptp_docs.py --selftest` | 0 | 0.264 | `$SOURCE` |
| `docs-08` | `python3 docs/DOC_MAP.gen.py --check` | 0 | 0.415 | `$SOURCE` |
| `docs-09` | `python3 docs/DOC_MAP.gen.py --selftest` | 0 | 0.516 | `$SOURCE` |
| `docs-10` | `python3 docs/diagrams/timesync_chain.gen.py --check` | 0 | 0.415 | `$SOURCE` |
| `docs-11` | `python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 | 0.465 | `$SOURCE` |
| `docs-12` | `python3 scripts/check_solution_docs.py` | 0 | 0.164 | `$SOURCE` |
| `docs-13` | `python3 scripts/check_solution_docs.py --selftest` | 0 | 2.77 | `$SOURCE` |
| `docs-14` | `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | 0.465 | `$SOURCE` |
| `docs-15` | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 | 0.515 | `$SOURCE` |
| `docs-16` | `python3 scripts/check_submodule_docs.py` | 0 | 0.515 | `$SOURCE` |
| `docs-17` | `python3 scripts/check_submodule_docs.py --selftest` | 0 | 0.064 | `$SOURCE` |
| `docs-18` | `python3 scripts/gen_wavedrom.py --selftest` | 0 | 0.164 | `$SOURCE` |
| `docs-19` | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | 0 | 0.314 | `$SOURCE` |
| `docs-20` | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | 0 | 0.365 | `$SOURCE` |
| `docs-21` | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | 0 | 0.365 | `$SOURCE` |
| `docs-22` | `python3 scripts/check_diagram_pngs.py` | 0 | 0.364 | `$SOURCE` |
| `docs-23` | `python3 scripts/check_diagram_pngs.py --selftest` | 0 | 6.888 | `$SOURCE` |
| `docs-24` | `python3 scripts/check_feature_status.py --self-test` | 0 | 0.917 | `$SOURCE` |
| `docs-25` | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | 1.268 | `$SOURCE` |
| `docs-26` | `python3 scripts/check_gptp_docs.py --with-submodule` | 0 | 0.214 | `$SOURCE` |
| `docs-27` | `make -C gptp-processor docs` | 0 | 0.765 | `$SOURCE` |
| `docs-28` | `python3 scripts/measure_control_flow.py --selftest` | 0 | 0.164 | `$SOURCE` |
| `docs-29` | `python3 scripts/measure_cohesion.py --selftest` | 0 | 0.064 | `$SOURCE` |
| `docs-30` | `python3 scripts/check_baremetal_only.py --check` | 0 | 18.376 | `$SOURCE` |
| `docs-31` | `python3 scripts/check_baremetal_only.py --selftest` | 0 | 6.587 | `$SOURCE` |
| `docs-32` | `python3 scripts/ci_rv32_sdk_selftest.py` | 0 | 1.167 | `$SOURCE` |
| `docs-33` | `python3 scripts/ci_rv32_sdk.py --destination $SDK` | 0 | 1.418 | `$SOURCE` |
| `docs-34` | `python3 scripts/check_nvm_record_space.py` | 0 | 2.32 | `$SOURCE` |
| `docs-35` | `python3 scripts/check_nvm_record_space.py --self-test` | 0 | 44.553 | `$SOURCE` |
| `docs-36` | `python3 scripts/check_nvm_capture.py` | 0 | 0.867 | `$SOURCE` |
| `docs-37` | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | 72.447 | `$SOURCE` |
| `docs-38` | `python3 scripts/check_soc_sources.py` | 0 | 0.164 | `$SOURCE` |
| `docs-39` | `python3 scripts/check_soc_sources.py --selftest` | 0 | 0.264 | `$SOURCE` |
| `docs-40` | `python3 sw/litex/iob_pack_selftest.py` | 0 | 2.122 | `$SOURCE` |
| `docs-41` | `python3 scripts/check_rtl_source_lists.py` | 0 | 1.568 | `$SOURCE` |
| `docs-42` | `python3 scripts/check_rtl_source_lists.py --selftest` | 0 | 2.983 | `$SOURCE` |
| `docs-43` | `python3 scripts/measure_naming.py --check` | 0 | 0.515 | `$SOURCE` |
| `docs-44` | `python3 scripts/measure_naming.py --selftest` | 0 | 0.567 | `$SOURCE` |
| `docs-45` | `python3 scripts/check_port_contracts.py` | 0 | 2.979 | `$SOURCE` |
| `docs-46` | `python3 scripts/check_port_contracts.py --selftest` | 0 | 3.432 | `$SOURCE` |
| `docs-47` | `python3 scripts/measure_fail_fast.py --check` | 0 | 1.821 | `$SOURCE` |
| `docs-48` | `python3 scripts/measure_fail_fast.py --selftest` | 0 | 1.771 | `$SOURCE` |
| `docs-49` | `python3 scripts/check_todo_ownership.py` | 0 | 1.869 | `$SOURCE` |
| `docs-50` | `python3 scripts/check_todo_ownership.py --selftest` | 0 | 1.969 | `$SOURCE` |
| `docs-51` | `python3 scripts/measure_test_evidence.py --check` | 0 | 6.836 | `$SOURCE` |
| `docs-52` | `python3 scripts/measure_test_evidence.py --selftest` | 0 | 6.837 | `$SOURCE` |
| `docs-53` | `python3 scripts/check_hygiene.py --check` | 0 | 0.415 | `$SOURCE` |
| `docs-54` | `python3 scripts/check_hygiene.py --selftest` | 0 | 0.467 | `$SOURCE` |
| `docs-55` | `python3 scripts/check_sv_idiom.py` | 0 | 0.517 | `$SOURCE` |
| `docs-56` | `python3 scripts/check_sv_idiom.py --selftest` | 0 | 0.516 | `$SOURCE` |
| `docs-58` | `python3 scripts/check_cpp_idiom.py --selftest` | 0 | 1.719 | `$SOURCE` |
| `docs-60` | `python3 scripts/check_py_idiom.py --selftest` | 0 | 4.478 | `$SOURCE` |
| `docs-61` | `python3 scripts/check_sh_idiom.py` | 0 | 0.265 | `$SOURCE` |
| `docs-62` | `python3 scripts/check_sh_idiom.py --selftest` | 0 | 0.265 | `$SOURCE` |
| `docs-63` | `python3 scripts/ci_events.py --check` | 0 | 0.215 | `$SOURCE` |
| `docs-64` | `python3 scripts/ci_events.py --selftest` | 0 | 18.229 | `$SOURCE` |
| `docs-65` | `python3 scripts/check_doc_paths.py` | 0 | 0.114 | `$SOURCE` |
| `docs-66` | `python3 scripts/check_archive.py` | 0 | 0.415 | `$SOURCE` |
| `docs-67` | `python3 scripts/check_archive.py --selftest` | 0 | 0.064 | `$SOURCE` |
| `docs-68` | `python3 scripts/gen_toc.py --selftest` | 0 | 0.915 | `$SOURCE` |
| `docs-69` | `python3 scripts/gen_toc.py --verify-anchors` | 0 | 3.025 | `$SOURCE` |
| `docs-70` | `python3 scripts/gen_toc.py --check` | 0 | 4.88 | `$SOURCE` |
| `docs-71` | `python3 avdecc/gen_aem_store.py --self-test` | 0 | 0.114 | `$SOURCE` |
| `docs-72` | `python3 scripts/check_sweep_shape.py --self-test` | 0 | 15.432 | `$SOURCE` |
| `docs-73` | `python3 scripts/check_deploy_shape.py --self-test` | 0 | 0.465 | `$SOURCE` |
| `docs-74` | `python3 scripts/check_entity_shape.py --self-test` | 0 | 59.154 | `$SOURCE` |
| `docs-style-final` | `python3 scripts/check_doc_style.py` | 0 | 0.064 | `$SOURCE` |
| `cpp-idiom-final` | `python3 scripts/check_cpp_idiom.py` | 0 | 1.718 | `$SOURCE` |
| `py-idiom-final` | `python3 scripts/check_py_idiom.py` | 0 | 4.425 | `$SOURCE` |
| `docs-selftest` | `python3 scripts/docs_check.py --selftest` | 0 | 0.214 | `$SOURCE` |
| `docs-wire` | `python3 scripts/check_wire_accountability.py --self-test` | 0 | 0.315 | `$SOURCE` |
| `ci-scope` | `python3 scripts/ci_scope.py --selftest` | 0 | 5.428 | `$SOURCE` |
| `em-dash-final` | `python3 scripts/check_em_dash.py --base e21c1ca024d37ea188ad15b5c8f9c2dae18628df` | 0 | 3.59 | `$SOURCE` |
| `docs-final` | `python3 scripts/docs_check.py` | 0 | 5.688 | `$SOURCE` |
| `docs-archive` | `python3 scripts/docs_check.py` | 0 | 5.882 | `$ARCHIVE` |
| `docs-archive-feature` | `python3 scripts/check_feature_status.py` | 0 | 1.067 | `$ARCHIVE` |
| `source-diff` | `git diff --check 500b8f64443777685e6a54049d933476710d26f0 HEAD` | 0 | 0.016 | `$SOURCE` |
| `integrity` | `python3 $SCRATCH/integrity.py` | 0 | 0.415 | `$SOURCE` |

## Helper details

The linked-size helper verifies every runtime provenance hash, then links shapes `endstation_ax7101_1x1_tdm8` and `endstation_ax7101_8x8`, each at IF=1 and IF=2. `ROUND6-SIZES.json` retains section and storage counts and hashes of all four ELF/map pairs. These are linked size fixtures, not executed target images.

The reviewer helper compiles the unchanged R533-5 `scripts/independent.cpp` at IF=1 and IF=2. Its control removes retry in a scratch copy; the withdrawal test must fail its active-state assertion. Probe results are evidence, not a reviewer verdict.

The dependency helper runs OFF and ON profiles at the parent pin, with CMake, CTest, unit tests and Behave. Full dependency reversals were unchanged by this round and retain prior evidence; no new reversal run is claimed.

The mailbox source copy is inventoried in `ROUND6-MAILBOX-SOURCE.json`; the compiled mailbox inputs are unchanged by the SRP repair. The wrapper uses release 5.050, caps inner jobs at eight and allows two simultaneous builds. Larger logs are hashed and sized but not copied.
