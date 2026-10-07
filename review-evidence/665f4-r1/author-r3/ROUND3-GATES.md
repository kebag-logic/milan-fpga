[A560]

# Round 3 gate evidence

Head: `c1049de1970e93d2c36ace62891ee9d947cd3191`. Relates to #665.

One required documentation command remains incomplete: the compiler-absent check timed out twice at 540 seconds, including an isolated retry. Every other final gate row below has exit 0. Paths are neutral parameters; logs retain their diagnostics with path substitution only.

The first 77 commands are every executable check in `.github/workflows/docs.yml`'s `docs-check` job except its separate runner self-test (listed next) and the explicitly delegated builder bank. Dependency installation, checkout, caching and artifact-upload steps are setup/publication, not omitted verdicts.

The runner's offline self-test ran inside a disposable, unprivileged job container: read-only committed archive, disk scratch, no network, credentials or daemon socket. It did not execute as the host orchestrator. The two archive checks and wire-accountability check cover the other documentation workflow jobs.

| Command | rc | Seconds | Receipt |
|---|---:|---:|---|
| `python3 scripts/gen_hdl_reference.py --selftest` | 0 | 0.265 | [docs-00.log](round3-receipts/docs-00.log) |
| `python3 scripts/gen_hdl_reference.py --output $SCRATCH/milan-hdl-reference` | 0 | 1.87 | [docs-01.log](round3-receipts/docs-01.log) |
| `python3 scripts/docs_check.py` | 0 | 6.035 | [docs-02.log](round3-receipts/docs-02.log) |
| `python3 scripts/check_em_dash.py --base d51b373ad7e8e8381af2797be3ebb8ee45c62e3c` | 0 | 3.726 | [docs-03.log](round3-receipts/docs-03.log) |
| `python3 scripts/check_doc_style.py` | 0 | 0.064 | [docs-04.log](round3-receipts/docs-04.log) |
| `python3 scripts/check_doc_style.py --selftest` | 0 | 0.064 | [docs-05.log](round3-receipts/docs-05.log) |
| `python3 scripts/check_gptp_docs.py` | 0 | 0.214 | [docs-06.log](round3-receipts/docs-06.log) |
| `python3 scripts/check_gptp_docs.py --selftest` | 0 | 0.264 | [docs-07.log](round3-receipts/docs-07.log) |
| `python3 docs/DOC_MAP.gen.py --check` | 0 | 0.428 | [docs-08.log](round3-receipts/docs-08.log) |
| `python3 docs/DOC_MAP.gen.py --selftest` | 0 | 0.517 | [docs-09.log](round3-receipts/docs-09.log) |
| `python3 docs/diagrams/timesync_chain.gen.py --check` | 0 | 0.415 | [docs-10.log](round3-receipts/docs-10.log) |
| `python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 | 0.465 | [docs-11.log](round3-receipts/docs-11.log) |
| `python3 scripts/check_solution_docs.py` | 0 | 0.164 | [docs-12.log](round3-receipts/docs-12.log) |
| `python3 scripts/check_solution_docs.py --selftest` | 0 | 3.022 | [docs-13.log](round3-receipts/docs-13.log) |
| `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | 0.465 | [docs-14.log](round3-receipts/docs-14.log) |
| `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 | 0.565 | [docs-15.log](round3-receipts/docs-15.log) |
| `python3 scripts/check_submodule_docs.py` | 0 | 0.615 | [docs-16.log](round3-receipts/docs-16.log) |
| `python3 scripts/check_submodule_docs.py --selftest` | 0 | 0.064 | [docs-17.log](round3-receipts/docs-17.log) |
| `python3 scripts/gen_wavedrom.py --selftest` | 0 | 0.165 | [docs-18.log](round3-receipts/docs-18.log) |
| `python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | 0 | 0.367 | [docs-19.log](round3-receipts/docs-19.log) |
| `python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | 0 | 0.518 | [docs-20.log](round3-receipts/docs-20.log) |
| `python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | 0 | 0.417 | [docs-21.log](round3-receipts/docs-21.log) |
| `python3 scripts/check_diagram_pngs.py` | 0 | 0.415 | [docs-22.log](round3-receipts/docs-22.log) |
| `python3 scripts/check_diagram_pngs.py --selftest` | 0 | 7.301 | [docs-23.log](round3-receipts/docs-23.log) |
| `python3 scripts/check_feature_status.py --self-test` | 0 | 1.017 | [docs-24.log](round3-receipts/docs-24.log) |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 | 1.319 | [docs-25.log](round3-receipts/docs-25.log) |
| `python3 scripts/check_gptp_docs.py --with-submodule` | 0 | 0.215 | [docs-26.log](round3-receipts/docs-26.log) |
| `make -C gptp-processor docs` | 0 | 0.867 | [docs-27.log](round3-receipts/docs-27.log) |
| `python3 scripts/measure_control_flow.py --selftest` | 0 | 0.164 | [docs-28.log](round3-receipts/docs-28.log) |
| `python3 scripts/measure_cohesion.py --selftest` | 0 | 0.065 | [docs-29.log](round3-receipts/docs-29.log) |
| `python3 scripts/check_baremetal_only.py --check` | 0 | 19.732 | [docs-30.log](round3-receipts/docs-30.log) |
| `python3 scripts/check_baremetal_only.py --selftest` | 0 | 7.6 | [docs-31.log](round3-receipts/docs-31.log) |
| `python3 scripts/ci_rv32_sdk_selftest.py` | 0 | 1.319 | [docs-32.log](round3-receipts/docs-32.log) |
| `python3 scripts/ci_rv32_sdk.py --destination $SDK` | 0 | 1.871 | [docs-33.log](round3-receipts/docs-33.log) |
| `python3 sw/builder/test_firmware_compiler.py --selftest` | 0 | 2.077 | [docs-34.log](round3-receipts/docs-34.log) |
| `python3 sw/builder/test_firmware_compiler.py --absent --audit $SCRATCH/rv32-absent.jsonl` | 124 | 540.008 | [docs-35.log](round3-receipts/docs-35.log) |
| `python3 scripts/check_nvm_record_space.py` | 0 | 2.679 | [docs-36.log](round3-receipts/docs-36.log) |
| `python3 scripts/check_nvm_record_space.py --self-test` | 0 | 47.563 | [docs-37.log](round3-receipts/docs-37.log) |
| `python3 scripts/check_nvm_capture.py` | 0 | 1.016 | [docs-38.log](round3-receipts/docs-38.log) |
| `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | 75.642 | [docs-39.log](round3-receipts/docs-39.log) |
| `python3 scripts/check_soc_sources.py` | 0 | 0.168 | [docs-40.log](round3-receipts/docs-40.log) |
| `python3 scripts/check_soc_sources.py --selftest` | 0 | 0.373 | [docs-41.log](round3-receipts/docs-41.log) |
| `python3 sw/litex/iob_pack_selftest.py` | 0 | 2.786 | [docs-42.log](round3-receipts/docs-42.log) |
| `python3 scripts/check_rtl_source_lists.py` | 0 | 1.726 | [docs-43.log](round3-receipts/docs-43.log) |
| `python3 scripts/check_rtl_source_lists.py --selftest` | 0 | 3.377 | [docs-44.log](round3-receipts/docs-44.log) |
| `python3 scripts/measure_naming.py --check` | 0 | 0.568 | [docs-45.log](round3-receipts/docs-45.log) |
| `python3 scripts/measure_naming.py --selftest` | 0 | 0.567 | [docs-46.log](round3-receipts/docs-46.log) |
| `python3 scripts/check_port_contracts.py` | 0 | 2.827 | [docs-47.log](round3-receipts/docs-47.log) |
| `python3 scripts/check_port_contracts.py --selftest` | 0 | 3.281 | [docs-48.log](round3-receipts/docs-48.log) |
| `python3 scripts/measure_fail_fast.py --check` | 0 | 1.72 | [docs-49.log](round3-receipts/docs-49.log) |
| `python3 scripts/measure_fail_fast.py --selftest` | 0 | 1.768 | [docs-50.log](round3-receipts/docs-50.log) |
| `python3 scripts/check_todo_ownership.py` | 0 | 1.824 | [docs-51.log](round3-receipts/docs-51.log) |
| `python3 scripts/check_todo_ownership.py --selftest` | 0 | 1.923 | [docs-52.log](round3-receipts/docs-52.log) |
| `python3 scripts/measure_test_evidence.py --check` | 0 | 7.058 | [docs-53.log](round3-receipts/docs-53.log) |
| `python3 scripts/measure_test_evidence.py --selftest` | 0 | 7.155 | [docs-54.log](round3-receipts/docs-54.log) |
| `python3 scripts/check_hygiene.py --check` | 0 | 0.422 | [docs-55.log](round3-receipts/docs-55.log) |
| `python3 scripts/check_hygiene.py --selftest` | 0 | 0.418 | [docs-56.log](round3-receipts/docs-56.log) |
| `python3 scripts/check_sv_idiom.py` | 0 | 0.516 | [docs-57.log](round3-receipts/docs-57.log) |
| `python3 scripts/check_sv_idiom.py --selftest` | 0 | 0.516 | [docs-58.log](round3-receipts/docs-58.log) |
| `python3 scripts/check_cpp_idiom.py` | 0 | 1.726 | [docs-59.log](round3-receipts/docs-59.log) |
| `python3 scripts/check_cpp_idiom.py --selftest` | 0 | 1.878 | [docs-60.log](round3-receipts/docs-60.log) |
| `python3 scripts/check_py_idiom.py` | 0 | 4.901 | [docs-61.log](round3-receipts/docs-61.log) |
| `python3 scripts/check_py_idiom.py --selftest` | 0 | 4.933 | [docs-62.log](round3-receipts/docs-62.log) |
| `python3 scripts/check_sh_idiom.py` | 0 | 0.265 | [docs-63.log](round3-receipts/docs-63.log) |
| `python3 scripts/check_sh_idiom.py --selftest` | 0 | 0.268 | [docs-64.log](round3-receipts/docs-64.log) |
| `python3 scripts/ci_events.py --check` | 0 | 0.215 | [docs-65.log](round3-receipts/docs-65.log) |
| `python3 scripts/ci_events.py --selftest` | 0 | 18.663 | [docs-66.log](round3-receipts/docs-66.log) |
| `python3 scripts/check_doc_paths.py` | 0 | 0.115 | [docs-67.log](round3-receipts/docs-67.log) |
| `python3 scripts/check_archive.py` | 0 | 0.421 | [docs-68.log](round3-receipts/docs-68.log) |
| `python3 scripts/check_archive.py --selftest` | 0 | 0.064 | [docs-69.log](round3-receipts/docs-69.log) |
| `python3 scripts/gen_toc.py --selftest` | 0 | 1.017 | [docs-70.log](round3-receipts/docs-70.log) |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | 3.279 | [docs-71.log](round3-receipts/docs-71.log) |
| `python3 scripts/gen_toc.py --check` | 0 | 5.083 | [docs-72.log](round3-receipts/docs-72.log) |
| `python3 avdecc/gen_aem_store.py --self-test` | 0 | 0.114 | [docs-73.log](round3-receipts/docs-73.log) |
| `python3 scripts/check_sweep_shape.py --self-test` | 0 | 16.24 | [docs-74.log](round3-receipts/docs-74.log) |
| `python3 scripts/check_deploy_shape.py --self-test` | 0 | 0.519 | [docs-75.log](round3-receipts/docs-75.log) |
| `python3 scripts/check_entity_shape.py --self-test` | 0 | 57.445 | [docs-76.log](round3-receipts/docs-76.log) |
| `sudo -n docker run --rm --network none --cap-drop ALL --security-opt no-new-privileges --pids-limit 256 --memory 2g --cpus 4 --user 1000:1000 --mount type=bind,src=$SCRATCH/committed-source,dst=/work,readonly --mount type=bind,src=$SCRATCH/isolated-scratch,dst=/scratch --workdir /work --env TMPDIR=/scratch --env PYTHONDONTWRITEBYTECODE=1 catthehacker/ubuntu:full-latest python3 scripts/act_ci.py --selftest` | 0 | 4.425 | [docs-act-selftest.log](round3-receipts/docs-act-selftest.log) |
| `python3 scripts/docs_check.py` | 0 | 5.783 | [docs-archive.log](round3-receipts/docs-archive.log) |
| `python3 scripts/check_feature_status.py` | 0 | 1.066 | [docs-archive-feature.log](round3-receipts/docs-archive-feature.log) |
| `python3 scripts/check_wire_accountability.py --self-test` | 0 | 0.315 | [docs-wire.log](round3-receipts/docs-wire.log) |
| `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir $SCRATCH/firmware-complete` | 0 | 435.339 | [firmware-final.log](round3-receipts/firmware-final.log) |
| `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep $SCRATCH/coverage-final` | 0 | 177.289 | [coverage-final.log](round3-receipts/coverage-final.log) |
| `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | 0 | 4.89 | [firmware-shared.log](round3-receipts/firmware-shared.log) |
| `python3 sw/firmware/gtest/tally_selftest.py --mutants` | 0 | 62.505 | [firmware-tally.log](round3-receipts/firmware-tally.log) |
| `python3 sw/firmware/gtest/fw_coverage.py --selftest` | 0 | 0.465 | [coverage-selftest.log](round3-receipts/coverage-selftest.log) |
| `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | 93.419 | [firmware-nvm.log](round3-receipts/firmware-nvm.log) |
| `make -C $SCRATCH/mailbox/tb/verilator/mbx -j2 VERILATOR=$PINNED_J8_WRAPPER` | 0 | 63.018 | [mailbox.log](round3-receipts/mailbox.log) |
| `python3 sw/mailbox/gen_mailbox.py --check` | 0 | 0.164 | [mailbox-contract.log](round3-receipts/mailbox-contract.log) |
| `python3 scripts/lint_rtl.py` | 0 | 8.888 | [rtl-lint.log](round3-receipts/rtl-lint.log) |
| `python3 $SCRATCH/images.py` | 0 | 7.282 | [linked-size.log](round3-receipts/linked-size.log) |
| `python3 $SCRATCH/upstream_positive.py` | 0 | 2.57 | [upstream-positive.log](round3-receipts/upstream-positive.log) |
| `python3 $LWSRP/tests/check_reversals.py --work-dir $SCRATCH/upstream-reversals --prefix $CGREEN` | 0 | 27.353 | [upstream-reversals.log](round3-receipts/upstream-reversals.log) |

## Execution details

The mailbox run used a disk copy of the committed inputs. `ROUND3-INTEGRITY.json` verifies 59 input files, including all firmware inputs consumed by that Makefile. Its wrapper pins release 5.050, changes inner builds to `-j8`, and limits concurrent builds to two. The root make used `-j2`; all firmware/campaign drivers used at most four workers.

`linked-size` executes `ctrl_image.py` for both listed entity configurations and IF=1/2 with the runtime archives named in `ROUND2-RUNTIME.json`. All 60 runtime provenance entries, including archives and generated header, were rehashed without mismatch. `ROUND3-SIZE.json` records the four current-head outputs.

`upstream-positive` runs configure/build/ctest/direct unit execution and behavior tests for `LWSRP_MILAN=OFF` and `ON`. Exact commands are in its receipt. The reversal command then executes all 40 controls, including the three named note-4/5 reversals. Their individual failing-test logs are included.

## Development and supplemental results

The first compiler-absent documentation check reached the 540-second foreground bound while other compilation was active. The isolated retry also reached 540 seconds. Both exit 124 receipts are retained; neither is counted as a pass. This docs workflow entry invokes `test_baremetal_profile_contract`, but the explicit delegation names the builder bank. The packet does not silently extend that exemption to claim this separate required docs entry passed. STOP is the resulting status.

A new C++ probe initially lacked an explicit void-pointer conversion. It was corrected before the recorded head. The complete firmware and coverage runs above include the corrected source. An earlier campaign loaded an old mutation site during editing; the final complete campaign reloaded and caught all 67 sites. No build failure counts as a catch.

Unmodified published reviewer probes produced 20 passing cases and two P3 setup failures (one per interface count). P3 asserts that a newly bound sink has `vlan_requested == false`; the new implementation deliberately copies already-requested shared-VID state at bind. The wire checks in that old P3 therefore do not execute. The assigned verification explicitly permits P3 or an equivalent. `LastNeverEligibleBindingWithdrawsTheSharedVidInEitherOrder` creates the never-requesting binding before the VID request, retains that false-state assertion, checks both unbind orders on every interface, and catches `last-ineligible-vid-leaks`. The untouched R533 shared-rebind probe, R532 P1/P2/P4/P5, all four R532 gap probes and the R533 MVRP probe pass at IF=1/2. The full supplemental log is retained; it is not represented as an all-green gate.

## Remaining responsibilities

The manager's candidate bank owns the builder bank, including the compiler-present contract and external resource-calibration arm. The compiler-absent check above intentionally reports its missing target instruments; that negative-control result is not substituted for the compiler-present bank. Hosted checks, the trusted local replica after publication, current-dev merge-candidate gates and independent re-review remain required.
