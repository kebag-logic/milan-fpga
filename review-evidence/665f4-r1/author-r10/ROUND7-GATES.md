[A560]

# Round 7 gate receipts

Head: `f74b9403b330ce316eeec6f724846f16def98443`. Every final invocation below exits 0. Commands run in the
candidate root unless the working-directory column says otherwise. Runs were
foreground, with four campaign workers or fewer and at most two HDL builds.
The three firmware shards took 531.058, 501.561 and 509.471 seconds separately.
Raw and normalized hashes are separate in `ROUND7-GATES.json`; the 13 MB MAAP
log is represented only by its size and SHA256. Development failures are listed
separately and do not count as evidence of a pass.

Use disk scratch, the CI-pinned SDK, HDL release 5.050, and the installed
repository documentation dependencies. Set `SOURCE`, `SCRATCH`, `PACKET`,
`REVIEW_PACKET`, `SDK`, `DOCS_ENV`, `RUNTIME`, `CGREEN` and `PINNED_VERILATOR`
to installation locations; `REVIEW_PACKET` names `reviews/R532-6` in the public
review evidence. Export `TMPDIR="$SCRATCH"`, `PYTHONDONTWRITEBYTECODE=1`,
`MILAN_RV32_CC="$SDK/bin/riscv32-buildroot-linux-gnu-gcc"`,
`VERILATOR="$PINNED_VERILATOR"`, `VERILATOR_JOBS=2`, and add `$DOCS_ENV/bin`
to `PATH`. Helpers are under `round7-helpers/` and read those variables.
They reproduce the commands; their retained log receipts came from equivalent
helpers with local paths substituted. Runtime provenance is in
`ROUND7-RUNTIME.json`; expand its path variables for local verification.

Prepare the mailbox export exactly as follows before its table entry:

```sh
git archive --format=tar --output "$SCRATCH/mailbox-inputs.tar" HEAD tb/verilator/mbx tb/common hdl/milan/mailbox sw/firmware/ctrl sw/mailbox
mkdir -p "$SCRATCH/mailbox"
tar -xf "$SCRATCH/mailbox-inputs.tar" -C "$SCRATCH/mailbox"
```

Prepare a no-Git committed source export before the two archive checks:

```sh
git archive --format=tar --output "$SCRATCH/committed-source.tar" HEAD
mkdir -p "$SCRATCH/committed-source"
tar -xf "$SCRATCH/committed-source.tar" -C "$SCRATCH/committed-source"
```

`ROUND7-SIZE.md` specifies the two historical exports before the linked-size
helper. `ROUND7-TESTS.md` records test-to-plant discriminators. The compiler-absent
run and builder bank remain manager-owned under issue comment 6036016117;
no pass is claimed for them by this packet.

| Receipt | Working directory | Exact command | rc | Seconds |
| --- | --- | --- | ---: | ---: |
| `firmware-shard0` | `$SOURCE` | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --mutation-shard 0 3 --jobs 4 --build-dir "$SCRATCH/firmware-shard0"` | 0 | 531.058 |
| `firmware-shard1` | `$SOURCE` | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --mutation-shard 1 3 --jobs 4 --build-dir "$SCRATCH/firmware-shard1"` | 0 | 501.561 |
| `firmware-shard2` | `$SOURCE` | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --mutation-shard 2 3 --jobs 4 --build-dir "$SCRATCH/firmware-shard2"` | 0 | 509.471 |
| `probes-final` | `$SOURCE` | `python3 "$PACKET/round7-helpers/probes.py"` | 0 | 48.819 |
| `new-plants-if1` | `$SOURCE` | `python3 "$PACKET/round7-helpers/new_plants_if1.py"` | 0 | 37.89 |
| `coverage-write` | `$SOURCE` | `python3 sw/firmware/gtest/fw_coverage.py --write --jobs 4 --keep "$SCRATCH/coverage-final"` | 0 | 202.906 |
| `coverage-check` | `$SOURCE` | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep "$SCRATCH/coverage-final"` | 0 | 184.513 |
| `coverage-selftest` | `$SOURCE` | `python3 sw/firmware/gtest/fw_coverage.py --selftest` | 0 | 0.465 |
| `rv32-selftest` | `$SOURCE` | `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | 0 | 5.581 |
| `tally-mutants` | `$SOURCE` | `python3 sw/firmware/gtest/tally_selftest.py --mutants` | 0 | 58.196 |
| `firmware-nvm-final` | `$SOURCE` | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | 94.894 |
| `mailbox-contract` | `$SOURCE` | `python3 sw/mailbox/gen_mailbox.py --check` | 0 | 0.164 |
| `mailbox` | `$SOURCE` | `make -C "$SCRATCH/mailbox/tb/verilator/mbx" -j2 VERILATOR_JOBS=2 "VERILATOR=$PINNED_VERILATOR"` | 0 | 41.141 |
| `maap-differential` | `$SOURCE` | `python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep "$SCRATCH/maap-diff"` | 0 | 145.509 |
| `upstream-positive` | `$SOURCE` | `python3 "$PACKET/round7-helpers/upstream_positive.py"` | 0 | 3.629 |
| `linked-size-verified` | `$SOURCE` | `python3 "$PACKET/round7-helpers/images.py"` | 0 | 20.909 |
| `docs-selftest` | `$SOURCE` | `python3 scripts/docs_check.py --selftest` | 0 | 0.215 |
| `docs-00` | `$SOURCE` | `python3 scripts/gen_hdl_reference.py --selftest` | 0 | 0.267 |
| `docs-01` | `$SOURCE` | `python3 scripts/gen_hdl_reference.py --output "$SCRATCH/milan-hdl-reference"` | 0 | 1.969 |
| `docs-02` | `$SOURCE` | `python3 scripts/docs_check.py` | 0 | 6.068 |
| `docs-03` | `$SOURCE` | `python3 scripts/check_em_dash.py --base e21c1ca024d37ea188ad15b5c8f9c2dae18628df` | 0 | 3.929 |
| `docs-04` | `$SOURCE` | `python3 scripts/check_doc_style.py` | 0 | 0.064 |
| `docs-05` | `$SOURCE` | `python3 scripts/check_doc_style.py --selftest` | 0 | 0.064 |
| `docs-06` | `$SOURCE` | `python3 scripts/check_gptp_docs.py` | 0 | 0.264 |
| `docs-07` | `$SOURCE` | `python3 scripts/check_gptp_docs.py --selftest` | 0 | 0.266 |
| `docs-08` | `$SOURCE` | `python3 docs/DOC_MAP.gen.py --check` | 0 | 0.566 |
| `docs-09` | `$SOURCE` | `python3 docs/DOC_MAP.gen.py --selftest` | 0 | 0.566 |
| `docs-10` | `$SOURCE` | `python3 docs/diagrams/timesync_chain.gen.py --check` | 0 | 0.566 |
| `docs-11` | `$SOURCE` | `python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 | 0.618 |
| `docs-12` | `$SOURCE` | `python3 scripts/check_solution_docs.py` | 0 | 0.114 |
| `docs-13` | `$SOURCE` | `python3 scripts/check_solution_docs.py --selftest` | 0 | 2.822 |
| `docs-14` | `$SOURCE` | `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | 0.515 |
| `docs-15` | `$SOURCE` | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 | 0.668 |
| `docs-16` | `$SOURCE` | `python3 scripts/check_submodule_docs.py` | 0 | 0.565 |
| `docs-17` | `$SOURCE` | `python3 scripts/check_submodule_docs.py --selftest` | 0 | 0.064 |
| `docs-18` | `$SOURCE` | `python3 scripts/gen_wavedrom.py --selftest` | 0 | 0.164 |
| `docs-19` | `$SOURCE` | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | 0 | 0.365 |
| `docs-20` | `$SOURCE` | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | 0 | 0.416 |
| `docs-21` | `$SOURCE` | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | 0 | 0.365 |
| `docs-22` | `$SOURCE` | `python3 scripts/check_diagram_pngs.py` | 0 | 0.417 |
| `docs-23` | `$SOURCE` | `python3 scripts/check_diagram_pngs.py --selftest` | 0 | 7.689 |
| `docs-24` | `$SOURCE` | `python3 scripts/check_feature_status.py --self-test` | 0 | 0.917 |
| `docs-25` | `$SOURCE` | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | 1.268 |
| `docs-26` | `$SOURCE` | `python3 scripts/check_gptp_docs.py --with-submodule` | 0 | 0.214 |
| `docs-27` | `$SOURCE` | `make -C gptp-processor docs` | 0 | 0.817 |
| `docs-28` | `$SOURCE` | `python3 scripts/measure_control_flow.py --selftest` | 0 | 0.164 |
| `docs-29` | `$SOURCE` | `python3 scripts/measure_cohesion.py --selftest` | 0 | 0.064 |
| `docs-30` | `$SOURCE` | `python3 scripts/check_baremetal_only.py --check` | 0 | 19.178 |
| `docs-31` | `$SOURCE` | `python3 scripts/check_baremetal_only.py --selftest` | 0 | 7.592 |
| `docs-32` | `$SOURCE` | `python3 scripts/ci_rv32_sdk_selftest.py` | 0 | 1.438 |
| `docs-33` | `$SOURCE` | `python3 scripts/ci_rv32_sdk.py --destination "$SDK"` | 0 | 2.02 |
| `docs-34` | `$SOURCE` | `python3 scripts/check_nvm_record_space.py` | 0 | 2.523 |
| `docs-35` | `$SOURCE` | `python3 scripts/check_nvm_record_space.py --self-test` | 0 | 47.35 |
| `docs-36` | `$SOURCE` | `python3 scripts/check_nvm_capture.py` | 0 | 0.916 |
| `docs-37` | `$SOURCE` | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | 78.479 |
| `docs-38` | `$SOURCE` | `python3 scripts/check_soc_sources.py` | 0 | 0.164 |
| `docs-39` | `$SOURCE` | `python3 scripts/check_soc_sources.py --selftest` | 0 | 0.214 |
| `docs-40` | `$SOURCE` | `python3 sw/litex/iob_pack_selftest.py` | 0 | 2.536 |
| `docs-41` | `$SOURCE` | `python3 scripts/check_rtl_source_lists.py` | 0 | 1.724 |
| `docs-42` | `$SOURCE` | `python3 scripts/check_rtl_source_lists.py --selftest` | 0 | 3.328 |
| `docs-43` | `$SOURCE` | `python3 scripts/measure_naming.py --check` | 0 | 0.567 |
| `docs-44` | `$SOURCE` | `python3 scripts/measure_naming.py --selftest` | 0 | 0.519 |
| `docs-45` | `$SOURCE` | `python3 scripts/check_port_contracts.py` | 0 | 2.778 |
| `docs-46` | `$SOURCE` | `python3 scripts/check_port_contracts.py --selftest` | 0 | 3.28 |
| `docs-47` | `$SOURCE` | `python3 scripts/measure_fail_fast.py --check` | 0 | 1.718 |
| `docs-48` | `$SOURCE` | `python3 scripts/measure_fail_fast.py --selftest` | 0 | 1.719 |
| `docs-49` | `$SOURCE` | `python3 scripts/check_todo_ownership.py` | 0 | 1.771 |
| `docs-50` | `$SOURCE` | `python3 scripts/check_todo_ownership.py --selftest` | 0 | 1.869 |
| `docs-51` | `$SOURCE` | `python3 scripts/measure_test_evidence.py --check` | 0 | 7.137 |
| `docs-52` | `$SOURCE` | `python3 scripts/measure_test_evidence.py --selftest` | 0 | 7.237 |
| `docs-53` | `$SOURCE` | `python3 scripts/check_hygiene.py --check` | 0 | 0.415 |
| `docs-54` | `$SOURCE` | `python3 scripts/check_hygiene.py --selftest` | 0 | 0.466 |
| `docs-55` | `$SOURCE` | `python3 scripts/check_sv_idiom.py` | 0 | 0.515 |
| `docs-56` | `$SOURCE` | `python3 scripts/check_sv_idiom.py --selftest` | 0 | 0.465 |
| `docs-57` | `$SOURCE` | `python3 scripts/check_cpp_idiom.py` | 0 | 1.72 |
| `docs-58` | `$SOURCE` | `python3 scripts/check_cpp_idiom.py --selftest` | 0 | 1.869 |
| `docs-59` | `$SOURCE` | `python3 scripts/check_py_idiom.py` | 0 | 4.477 |
| `docs-60` | `$SOURCE` | `python3 scripts/check_py_idiom.py --selftest` | 0 | 4.024 |
| `docs-61` | `$SOURCE` | `python3 scripts/check_sh_idiom.py` | 0 | 0.264 |
| `docs-62` | `$SOURCE` | `python3 scripts/check_sh_idiom.py --selftest` | 0 | 0.265 |
| `docs-63` | `$SOURCE` | `python3 scripts/ci_events.py --check` | 0 | 0.214 |
| `docs-64` | `$SOURCE` | `python3 scripts/ci_events.py --selftest` | 0 | 17.725 |
| `docs-65` | `$SOURCE` | `python3 scripts/check_doc_paths.py` | 0 | 0.114 |
| `docs-66` | `$SOURCE` | `python3 scripts/check_archive.py` | 0 | 0.415 |
| `docs-67` | `$SOURCE` | `python3 scripts/check_archive.py --selftest` | 0 | 0.064 |
| `docs-68` | `$SOURCE` | `python3 scripts/gen_toc.py --selftest` | 0 | 0.866 |
| `docs-69` | `$SOURCE` | `python3 scripts/gen_toc.py --verify-anchors` | 0 | 2.871 |
| `docs-70` | `$SOURCE` | `python3 scripts/gen_toc.py --check` | 0 | 5.629 |
| `docs-71` | `$SOURCE` | `python3 avdecc/gen_aem_store.py --self-test` | 0 | 0.114 |
| `docs-72` | `$SOURCE` | `python3 scripts/check_sweep_shape.py --self-test` | 0 | 15.375 |
| `docs-73` | `$SOURCE` | `python3 scripts/check_deploy_shape.py --self-test` | 0 | 0.566 |
| `docs-74` | `$SOURCE` | `python3 scripts/check_entity_shape.py --self-test` | 0 | 56.845 |
| `em-dash-final` | `$SOURCE` | `python3 scripts/check_em_dash.py --base e21c1ca024d37ea188ad15b5c8f9c2dae18628df` | 0 | 3.278 |
| `docs-final` | `$SOURCE` | `python3 scripts/docs_check.py` | 0 | 5.627 |
| `docs-wire` | `$SOURCE` | `python3 scripts/check_wire_accountability.py --self-test` | 0 | 0.316 |
| `ci-scope` | `$SOURCE` | `python3 scripts/ci_scope.py --selftest` | 0 | 5.327 |
| `source-diff` | `$SOURCE` | `git diff --check cce554f64f6bdab1f6d26e5c4d7b46d54d228c52 HEAD` | 0 | 0.008 |
| `docs-archive` | `$SCRATCH/committed-source` | `python3 scripts/docs_check.py` | 0 | 5.485 |
| `docs-archive-feature` | `$SCRATCH/committed-source` | `python3 scripts/check_feature_status.py` | 0 | 0.966 |
