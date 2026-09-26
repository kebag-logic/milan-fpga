#!/usr/bin/env bash
# Run the docs-check job's gate commands (.github/workflows/docs.yml) locally,
# one line per command with its exit status. Installation steps are replaced by
# an existing interpreter (PYVENV) holding the locked Markdown/diagram packages.
# Excluded: the HDL reference build (parser wheel not installed here), the SDK
# install step (the SDK is used read-only from SDK_BIN) and the local act runner
# self-test (reserved to the manager).
# Usage: docs_check_steps.sh <repo> <em-dash base> <out-dir>
set -uo pipefail
repo=$1 base=$2 out=$3
: "${PYVENV:=$VALIDATION_TOOLS/md-venv-40cdefe08ebd}"
: "${SDK_BIN:=$HOME/br-milan-rv32/host/bin}"
mkdir -p "$out/logs"
export PATH="$PYVENV/bin:$PATH:$SDK_BIN"
cd "$repo" || exit 2
summary="$out/summary.txt"
: > "$summary"
n=0
run() {
  n=$((n + 1))
  local log; log=$(printf '%s/logs/%02d.log' "$out" "$n")
  { echo "STEP $1"; echo "CMD ${*:2}"; } > "$log"
  bash -c "${*:2}" >> "$log" 2>&1
  local rc=$?
  printf '%02d rc=%d | %s | %s\n' "$n" "$rc" "$1" "${*:2}" | tee -a "$summary"
}
run links 'python3 scripts/docs_check.py'
run emdash "python3 scripts/check_em_dash.py --base $base"
run style 'python3 scripts/check_doc_style.py'
run style 'python3 scripts/check_doc_style.py --selftest'
run style 'python3 scripts/check_gptp_docs.py'
run style 'python3 scripts/check_gptp_docs.py --selftest'
run diagrams 'python3 docs/DOC_MAP.gen.py --check'
run diagrams 'python3 docs/DOC_MAP.gen.py --selftest'
run diagrams 'python3 docs/diagrams/timesync_chain.gen.py --check'
run diagrams 'python3 docs/diagrams/timesync_chain.gen.py --selftest'
run solution 'python3 scripts/check_solution_docs.py'
run solution 'python3 scripts/check_solution_docs.py --selftest'
run submodule 'python3 docs/diagrams/submodule_boundaries.gen.py --check'
run submodule 'python3 docs/diagrams/submodule_boundaries.gen.py --selftest'
run submodule 'python3 scripts/check_submodule_docs.py'
run submodule 'python3 scripts/check_submodule_docs.py --selftest'
run wavedrom 'python3 scripts/gen_wavedrom.py --selftest'
run wavedrom 'python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check'
run wavedrom 'python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check'
run wavedrom 'python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check'
run png 'python3 scripts/check_diagram_pngs.py'
run png 'python3 scripts/check_diagram_pngs.py --selftest'
run feature 'python3 scripts/check_feature_status.py --self-test'
run trace 'python3 docs/traceability/gen_module_matrix.py --check'
run gptp-sub 'python3 scripts/check_gptp_docs.py --with-submodule'
run gptp-sub 'make -C gptp-processor docs'
run quality 'python3 scripts/measure_control_flow.py --selftest'
run quality 'python3 scripts/measure_cohesion.py --selftest'
run baremetal 'python3 scripts/check_baremetal_only.py --check'
run baremetal 'python3 scripts/check_baremetal_only.py --selftest'
run fw-absent 'python3 sw/builder/test_firmware_compiler.py --selftest'
run fw-absent "python3 sw/builder/test_firmware_compiler.py --absent --audit $out/rv32-absent.jsonl"
run builder 'python3 sw/builder/test_builder.py --require-rv32'
run nvm-space 'python3 scripts/check_nvm_record_space.py'
run nvm-space 'python3 scripts/check_nvm_record_space.py --self-test'
run capture 'python3 scripts/check_nvm_capture.py'
# --- the steps after the capture gate ---
run writer 'python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test'
run soc-src 'python3 scripts/check_soc_sources.py'
run soc-src 'python3 scripts/check_soc_sources.py --selftest'
run soc-src 'python3 sw/litex/iob_pack_selftest.py'
run rtl-src 'python3 scripts/check_rtl_source_lists.py'
run rtl-src 'python3 scripts/check_rtl_source_lists.py --selftest'
run naming 'python3 scripts/measure_naming.py --check'
run naming 'python3 scripts/measure_naming.py --selftest'
run ports 'python3 scripts/check_port_contracts.py'
run ports 'python3 scripts/check_port_contracts.py --selftest'
run failfast 'python3 scripts/measure_fail_fast.py --check'
run failfast 'python3 scripts/measure_fail_fast.py --selftest'
run todo 'python3 scripts/check_todo_ownership.py'
run todo 'python3 scripts/check_todo_ownership.py --selftest'
run evidence 'python3 scripts/measure_test_evidence.py --check'
run evidence 'python3 scripts/measure_test_evidence.py --selftest'
run hygiene 'python3 scripts/check_hygiene.py --check'
run hygiene 'python3 scripts/check_hygiene.py --selftest'
run sv 'python3 scripts/check_sv_idiom.py'
run sv 'python3 scripts/check_sv_idiom.py --selftest'
run cpp 'python3 scripts/check_cpp_idiom.py'
run cpp 'python3 scripts/check_cpp_idiom.py --selftest'
run py 'python3 scripts/check_py_idiom.py'
run py 'python3 scripts/check_py_idiom.py --selftest'
run sh 'python3 scripts/check_sh_idiom.py'
run sh 'python3 scripts/check_sh_idiom.py --selftest'
run ci-events 'python3 scripts/ci_events.py --check'
run ci-events 'python3 scripts/ci_events.py --selftest'
# Local act runner contract gate: NOT RUN here (reserved to the manager).
run doc-paths 'python3 scripts/check_doc_paths.py'
run archive 'python3 scripts/check_archive.py'
run archive 'python3 scripts/check_archive.py --selftest'
run toc 'python3 scripts/gen_toc.py --selftest'
run toc 'python3 scripts/gen_toc.py --verify-anchors'
run toc 'python3 scripts/gen_toc.py --check'
run aem 'python3 avdecc/gen_aem_store.py --self-test'
run sweep 'python3 scripts/check_sweep_shape.py --self-test'
run deploy 'python3 scripts/check_deploy_shape.py --self-test'
run entity 'python3 scripts/check_entity_shape.py --self-test'
run wire 'python3 scripts/check_wire_accountability.py --self-test'
echo "FAILED $(grep -vc ' rc=0 ' "$summary") of $(wc -l < "$summary")" | tee -a "$summary"
