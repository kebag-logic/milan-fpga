#!/usr/bin/env bash
# Run docs-workflow gate steps (from .github/workflows/docs.yml) on the clean clone.
# Usage: run_gates.sh <chunk>
set -u
G=$VALIDATION_STORAGE/640-a720d/gates
WT=$G/wt
export PATH="$G/venv/bin:$PATH"
export RUNNER_TEMP=$G/runner_temp
export GITHUB_WORKSPACE=$WT
export MAKEFLAGS="-j1 --no-print-directory"
cd "$WT"
run() { # id, command
  local id="$1"; shift
  local t0=$(date +%s)
  ( set -o pipefail; timeout "${STEP_TIMEOUT:-560}" bash -c "$*" ) > "$G/logs/$id.log" 2>&1
  local rc=$?
  echo "$rc" > "$G/logs/$id.rc"
  printf '%s\trc=%s\t%ss\t%s\n' "$id" "$rc" "$(( $(date +%s) - t0 ))" "$(tail -1 "$G/logs/$id.log" | cut -c1-150)"
}
case "$1" in
a)
run gate_7_docs_check "python3 scripts/docs_check.py"
run gate_8_em_dash "python3 scripts/check_em_dash.py --base 1f29f189279f9fc0132f4918e47342b87d22f33a"
run gate_9_style "python3 scripts/check_doc_style.py && python3 scripts/check_doc_style.py --selftest && python3 scripts/check_gptp_docs.py && python3 scripts/check_gptp_docs.py --selftest"
run gate_10_diagram_nodrift "python3 docs/DOC_MAP.gen.py --check && python3 docs/DOC_MAP.gen.py --selftest && python3 docs/diagrams/timesync_chain.gen.py --check && python3 docs/diagrams/timesync_chain.gen.py --selftest"
run gate_11_solution "python3 scripts/check_solution_docs.py && python3 scripts/check_solution_docs.py --selftest"
run gate_12_submodule_docs "python3 docs/diagrams/submodule_boundaries.gen.py --check && python3 docs/diagrams/submodule_boundaries.gen.py --selftest && python3 scripts/check_submodule_docs.py && python3 scripts/check_submodule_docs.py --selftest"
run gate_13_wavedrom "python3 scripts/gen_wavedrom.py --selftest && python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check && python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check && python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check"
run gate_14_pngs "python3 scripts/check_diagram_pngs.py && python3 scripts/check_diagram_pngs.py --selftest"
run gate_15_feature "python3 scripts/check_feature_status.py --self-test"
run gate_16_traceability "python3 docs/traceability/gen_module_matrix.py --check"
run gate_21_baremetal "python3 scripts/check_baremetal_only.py --check && python3 scripts/check_baremetal_only.py --selftest"
run gate_43_doc_paths "python3 scripts/check_doc_paths.py"
run gate_44_archive "python3 scripts/check_archive.py && python3 scripts/check_archive.py --selftest"
run gate_45_toc "python3 scripts/gen_toc.py --selftest && python3 scripts/gen_toc.py --verify-anchors && python3 scripts/gen_toc.py --check"
;;
b)
run gate_1_hdl_reference "python3 scripts/gen_hdl_reference.py --selftest && python3 scripts/gen_hdl_reference.py --output $RUNNER_TEMP/milan-hdl-reference"
run gate_18_gptp_submodule "python3 scripts/check_gptp_docs.py --with-submodule && make -C gptp-processor docs"
run gate_19_measure_selftests "python3 scripts/measure_control_flow.py --selftest && python3 scripts/measure_cohesion.py --selftest"
run gate_26_nvm_record_space "python3 scripts/check_nvm_record_space.py && python3 scripts/check_nvm_record_space.py --self-test"
run gate_27_nvm_capture "python3 scripts/check_nvm_capture.py"
run gate_28_nvm_writer "python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test"
run gate_29_soc_sources "python3 scripts/check_soc_sources.py && python3 scripts/check_soc_sources.py --selftest && python3 sw/litex/iob_pack_selftest.py"
run gate_30_rtl_source_lists "python3 scripts/check_rtl_source_lists.py && python3 scripts/check_rtl_source_lists.py --selftest"
run gate_31_naming "python3 scripts/measure_naming.py --check && python3 scripts/measure_naming.py --selftest"
run gate_32_port_contracts "python3 scripts/check_port_contracts.py && python3 scripts/check_port_contracts.py --selftest"
run gate_33_fail_fast "python3 scripts/measure_fail_fast.py --check && python3 scripts/measure_fail_fast.py --selftest"
run gate_34_todo "python3 scripts/check_todo_ownership.py && python3 scripts/check_todo_ownership.py --selftest"
run gate_35_test_evidence "python3 scripts/measure_test_evidence.py --check && python3 scripts/measure_test_evidence.py --selftest"
run gate_36_hygiene "python3 scripts/check_hygiene.py --check && python3 scripts/check_hygiene.py --selftest"
run gate_37_sv_idiom "python3 scripts/check_sv_idiom.py && python3 scripts/check_sv_idiom.py --selftest"
run gate_38_cpp_idiom "python3 scripts/check_cpp_idiom.py && python3 scripts/check_cpp_idiom.py --selftest"
run gate_39_py_idiom "python3 scripts/check_py_idiom.py && python3 scripts/check_py_idiom.py --selftest"
run gate_40_sh_idiom "python3 scripts/check_sh_idiom.py && python3 scripts/check_sh_idiom.py --selftest"
run gate_46_aem_store "python3 avdecc/gen_aem_store.py --self-test"
run gate_47_sweep_shape "python3 scripts/check_sweep_shape.py --self-test"
run gate_48_deploy_shape "python3 scripts/check_deploy_shape.py --self-test"
run gate_49_entity_shape "python3 scripts/check_entity_shape.py --self-test"
;;
c)
run gate_50_ci_controls "python3 scripts/ci_gate_workflows.py --check && python3 scripts/ci_gate_workflows_selftest.py && python3 scripts/ci_case_receipts_selftest.py && python3 scripts/ci_make_cases_selftest.py && python3 scripts/ci_maap_cases_selftest.py && python3 scripts/ci_capture_cases_selftest.py && python3 scripts/ci_suite_pieces_selftest.py && python3 scripts/ci_suite_collect_selftest.py && python3 scripts/ci_fail_fast_selftest.py && python3 scripts/ci_runtime_evidence_selftest.py && python3 scripts/ci_install_cache_selftest.py && python3 scripts/generate_ci_evidence_pins.py --check && python3 scripts/ci_workflow_plan_selftest.py && python3 scripts/ci_manifest_selftest.py"
run gate_41_ci_events "python3 scripts/ci_events.py --check && python3 scripts/ci_events.py --selftest"
run gate_42_act_runner "python3 scripts/act_ci.py --selftest && d=\$(mktemp -d -p $RUNNER_TEMP) && install -m 0555 scripts/act_ci.py \$d/act_ci.py && python3 -I \$d/act_ci.py --selftest --worktree $GITHUB_WORKSPACE"
run wire_accountability "python3 scripts/check_wire_accountability.py --self-test"
;;
d0)
run gate_25_0_builder "python3 scripts/ci_builder_legs.py run 0 --receipt $RUNNER_TEMP/builder-leg-0.json -- python3 sw/builder/test_builder.py --require-rv32"
;;
d1)
run gate_25_1_builder "python3 scripts/ci_builder_legs.py run 1 --receipt $RUNNER_TEMP/builder-leg-1.json -- python3 sw/builder/test_builder.py --require-rv32"
;;
e)
export HOME=$VALIDATION_STORAGE/640-a720d/home
run rv32_sdk_ci "python3 scripts/ci_rv32_sdk_selftest.py && python3 scripts/ci_rv32_sdk.py --destination \$HOME/br-milan-rv32/host"
run gate_24_fw_compiler_sdk "python3 sw/builder/test_firmware_compiler.py --selftest && python3 sw/builder/test_firmware_compiler.py --absent --audit $RUNNER_TEMP/rv32-absent.jsonl"
run gate_25_0_builder "python3 -m pip install --quiet pyyaml && python3 scripts/ci_builder_legs.py run 0 --receipt $RUNNER_TEMP/builder-leg-0.json -- python3 sw/builder/test_builder.py --require-rv32"
run gate_25_1_builder "python3 -m pip install --quiet pyyaml && python3 scripts/ci_builder_legs.py run 1 --receipt $RUNNER_TEMP/builder-leg-1.json -- python3 sw/builder/test_builder.py --require-rv32"
;;
e_sdk)
export HOME=$VALIDATION_STORAGE/640-a720d/home
run rv32_sdk_ci "python3 scripts/ci_rv32_sdk_selftest.py && python3 scripts/ci_rv32_sdk.py --destination \$HOME/br-milan-rv32/host"
;;
e_fw)
export HOME=$VALIDATION_STORAGE/640-a720d/home
run gate_24_fw_compiler_sdk "python3 sw/builder/test_firmware_compiler.py --selftest && python3 sw/builder/test_firmware_compiler.py --absent --audit $RUNNER_TEMP/rv32-absent.jsonl"
;;
e_b0)
export HOME=$VALIDATION_STORAGE/640-a720d/home
run gate_25_0_builder "python3 -m pip install --quiet pyyaml && python3 scripts/ci_builder_legs.py run 0 --receipt $RUNNER_TEMP/builder-leg-0.json -- python3 sw/builder/test_builder.py --require-rv32"
;;
e_b1)
export HOME=$VALIDATION_STORAGE/640-a720d/home
run gate_25_1_builder "python3 -m pip install --quiet pyyaml && python3 scripts/ci_builder_legs.py run 1 --receipt $RUNNER_TEMP/builder-leg-1.json -- python3 sw/builder/test_builder.py --require-rv32"
;;
nogit)
rm -rf $G/nogit && mkdir -p $G/nogit && git -C "$WT" archive HEAD | tar -x -C $G/nogit
cd $G/nogit
run nogit_docs_check "test ! -e .git && python3 scripts/docs_check.py && python3 scripts/check_feature_status.py"
;;
esac
