#!/usr/bin/env bash
# Local replica of .github/workflows/docs.yml (jobs docs-check,
# wire-accountability and docs-check-no-git) at the checked-out head, one rc
# line per command, every python3 call under the given interpreter (CPython
# 3.12.3 with the workflow's pinned pip requirements). Install steps are
# omitted. Not run here, each with its reason in the lane handoff:
# `make -C gptp-processor docs` (it writes into the submodule checkout),
# `scripts/act_ci.py --selftest` (the candidate's runner may self-test only
# inside the disposable CI job) and `scripts/ci_rv32_sdk.py --destination`
# (it installs the SDK; the pinned SDK is already present and its self-test
# runs).
# Usage: docs_check_replica.sh <repo> <python> <base> <logdir> <scratch>
set -u
repo=$1; py=$2; base=$3; logs=$4; scratch=$5
mkdir -p "$logs" "$scratch"
cd "$repo" || exit 2
n=0; fails=0
step() {
  n=$((n + 1))
  local log; log=$(printf '%s/%02d.log' "$logs" "$n")
  "$@" > "$log" 2>&1
  local rc=$?
  [ "$rc" -eq 0 ] || fails=$((fails + 1))
  printf 'rc=%d  %s\n' "$rc" "$*"
}
step "$py" scripts/gen_hdl_reference.py --selftest
step "$py" scripts/gen_hdl_reference.py --output "$scratch/milan-hdl-reference"
step "$py" scripts/docs_check.py
step "$py" scripts/check_em_dash.py --base "$base"
step "$py" scripts/check_doc_style.py
step "$py" scripts/check_doc_style.py --selftest
step "$py" scripts/check_gptp_docs.py
step "$py" scripts/check_gptp_docs.py --selftest
step "$py" docs/DOC_MAP.gen.py --check
step "$py" docs/DOC_MAP.gen.py --selftest
step "$py" docs/diagrams/timesync_chain.gen.py --check
step "$py" docs/diagrams/timesync_chain.gen.py --selftest
step "$py" scripts/check_solution_docs.py
step "$py" scripts/check_solution_docs.py --selftest
step "$py" docs/diagrams/submodule_boundaries.gen.py --check
step "$py" docs/diagrams/submodule_boundaries.gen.py --selftest
step "$py" scripts/check_submodule_docs.py
step "$py" scripts/check_submodule_docs.py --selftest
step "$py" scripts/gen_wavedrom.py --selftest
step "$py" scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check
step "$py" scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check
step "$py" scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check
step "$py" scripts/check_diagram_pngs.py
step "$py" scripts/check_diagram_pngs.py --selftest
step "$py" scripts/check_feature_status.py --self-test
step "$py" docs/traceability/gen_module_matrix.py --check
step "$py" scripts/check_gptp_docs.py --with-submodule
step "$py" scripts/measure_control_flow.py --selftest
step "$py" scripts/measure_cohesion.py --selftest
step "$py" scripts/check_baremetal_only.py --check
step "$py" scripts/check_baremetal_only.py --selftest
step "$py" scripts/ci_rv32_sdk_selftest.py
step "$py" sw/builder/test_firmware_compiler.py --selftest
step "$py" sw/builder/test_firmware_compiler.py --absent --audit "$scratch/rv32-absent.jsonl"
step "$py" sw/builder/test_builder.py --require-rv32
step "$py" scripts/check_nvm_record_space.py
step "$py" scripts/check_nvm_record_space.py --self-test
step "$py" scripts/check_nvm_capture.py
step "$py" sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
step "$py" scripts/check_soc_sources.py
step "$py" scripts/check_soc_sources.py --selftest
step "$py" sw/litex/iob_pack_selftest.py
step "$py" scripts/check_rtl_source_lists.py
step "$py" scripts/check_rtl_source_lists.py --selftest
step "$py" scripts/measure_naming.py --check
step "$py" scripts/measure_naming.py --selftest
step "$py" scripts/check_port_contracts.py
step "$py" scripts/check_port_contracts.py --selftest
step "$py" scripts/measure_fail_fast.py --check
step "$py" scripts/measure_fail_fast.py --selftest
step "$py" scripts/check_todo_ownership.py
step "$py" scripts/check_todo_ownership.py --selftest
step "$py" scripts/measure_test_evidence.py --check
step "$py" scripts/measure_test_evidence.py --selftest
step "$py" scripts/check_hygiene.py --check
step "$py" scripts/check_hygiene.py --selftest
step "$py" scripts/check_sv_idiom.py
step "$py" scripts/check_sv_idiom.py --selftest
step "$py" scripts/check_cpp_idiom.py
step "$py" scripts/check_cpp_idiom.py --selftest
step "$py" scripts/check_py_idiom.py
step "$py" scripts/check_py_idiom.py --selftest
step "$py" scripts/check_sh_idiom.py
step "$py" scripts/check_sh_idiom.py --selftest
step "$py" scripts/ci_events.py --check
step "$py" scripts/ci_events.py --selftest
step "$py" scripts/check_doc_paths.py
step "$py" scripts/check_archive.py
step "$py" scripts/check_archive.py --selftest
step "$py" scripts/gen_toc.py --selftest
step "$py" scripts/gen_toc.py --verify-anchors
step "$py" scripts/gen_toc.py --check
step "$py" avdecc/gen_aem_store.py --self-test
step "$py" scripts/check_sweep_shape.py --self-test
step "$py" scripts/check_deploy_shape.py --self-test
step "$py" scripts/check_entity_shape.py --self-test
step "$py" scripts/check_wire_accountability.py --self-test
# docs-check-no-git: the same tree with no git metadata
rm -rf "$scratch/nogit" && mkdir -p "$scratch/nogit"
git archive HEAD | tar -x -C "$scratch/nogit"
pushd "$scratch/nogit" > /dev/null || exit 2
step "$py" scripts/docs_check.py
step "$py" scripts/check_feature_status.py
popd > /dev/null || exit 2
step git diff --check
step git diff --check "$base" HEAD
echo "steps: $n  failing: $fails"
[ "$fails" -eq 0 ]
