#!/usr/bin/env bash
# Composition gates for the merge-train candidate. Usage: run_gates.sh <clone> <packet> <base-rev>
# Each gate runs in parallel (at most 16), writing receipts/<name>.log and receipts/<name>.rc.
set -u
CLONE=$1; PKT=$2; BASE=$3
R="$PKT/receipts"; mkdir -p "$R" "$PKT/scratch/tmp"
export TMPDIR="$PKT/scratch/tmp"
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export MILAN_RV32_CC=riscv64-elf-gcc
cd "$CLONE" || exit 2
gates=(
  "docs_check|python3 scripts/docs_check.py"
  "em_dash_base|python3 scripts/check_em_dash.py --base $BASE"
  "em_dash_selftest|python3 scripts/check_em_dash.py --selftest"
  "doc_style|python3 scripts/check_doc_style.py"
  "doc_map|python3 docs/DOC_MAP.gen.py --check"
  "solution_docs|python3 scripts/check_solution_docs.py"
  "submodule_diagram|python3 docs/diagrams/submodule_boundaries.gen.py --check"
  "submodule_docs|python3 scripts/check_submodule_docs.py"
  "submodule_docs_selftest|python3 scripts/check_submodule_docs.py --selftest"
  "diagram_pngs|python3 scripts/check_diagram_pngs.py"
  "feature_status|python3 scripts/check_feature_status.py"
  "module_matrix|python3 docs/traceability/gen_module_matrix.py --check"
  "baremetal_only|python3 scripts/check_baremetal_only.py --check"
  "naming|python3 scripts/measure_naming.py --check"
  "port_contracts|python3 scripts/check_port_contracts.py"
  "fail_fast|python3 scripts/measure_fail_fast.py --check"
  "todo_ownership|python3 scripts/check_todo_ownership.py"
  "test_evidence|python3 scripts/measure_test_evidence.py --check"
  "test_evidence_selftest|python3 scripts/measure_test_evidence.py --selftest"
  "hygiene|python3 scripts/check_hygiene.py --check"
  "cpp_idiom|python3 scripts/check_cpp_idiom.py"
  "py_idiom|python3 scripts/check_py_idiom.py"
  "sh_idiom|python3 scripts/check_sh_idiom.py"
  "ci_events_check|python3 scripts/ci_events.py --check"
  "ci_events_selftest|python3 scripts/ci_events.py --selftest"
  "doc_paths|python3 scripts/check_doc_paths.py"
  "toc_anchors|python3 scripts/gen_toc.py --verify-anchors"
  "toc_check|python3 scripts/gen_toc.py --check"
  "maap_differential_selftest|python3 sw/firmware/ctrl/test/maap_differential.py --self-test"
  "ctrl_suite|python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --jobs 4"
  "fw_coverage_check|python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4"
)
run_one() {
  local name=${1%%|*} cmd=${1#*|}
  local start; start=$(date +%s)
  ( echo "\$ $cmd"; timeout 3000 bash -c "$cmd" ) > "$R/$name.log" 2>&1
  local rc=$?
  echo "$rc" > "$R/$name.rc"
  echo "$name rc=$rc $(( $(date +%s) - start ))s"
}
export -f run_one; export R
printf '%s\n' "${gates[@]}" | xargs -P 16 -I{} bash -c 'run_one "$@"' _ {}
