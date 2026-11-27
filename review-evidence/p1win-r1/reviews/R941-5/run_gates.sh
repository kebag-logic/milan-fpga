#!/usr/bin/env bash
# Run the composition-relevant gates on the candidate tree, concurrently, one
# log and one rc file per gate. Usage: run_gates.sh <clone> <outdir> <parent-sha>
set -u
clone=$1; out=$2; parent=$3
mkdir -p "$out"
export PYTHONDONTWRITEBYTECODE=1
cd "$clone" || exit 2
gates=(
  "docs_check|python3 scripts/docs_check.py"
  "toc_check|python3 scripts/gen_toc.py --check"
  "toc_anchors|python3 scripts/gen_toc.py --verify-anchors"
  "em_dash|python3 scripts/check_em_dash.py --base $parent"
  "ci_events_check|python3 scripts/ci_events.py --check"
  "ci_events_selftest|python3 scripts/ci_events.py --selftest"
  "ci_gate_workflows|python3 scripts/ci_gate_workflows.py --check"
  "ci_evidence_pins|python3 scripts/generate_ci_evidence_pins.py --check"
  "docs_inventory|python3 scripts/docs_inventory.py --check"
  "doc_map|python3 docs/DOC_MAP.gen.py --check"
  "doc_paths|python3 scripts/check_doc_paths.py"
  "doc_style|python3 scripts/check_doc_style.py"
  "hygiene|python3 scripts/check_hygiene.py --check"
  "submodule_docs|python3 scripts/check_submodule_docs.py"
  "gptp_docs|python3 scripts/check_gptp_docs.py"
  "feature_status|python3 scripts/check_feature_status.py"
  "solution_docs|python3 scripts/check_solution_docs.py"
  "todo_ownership|python3 scripts/check_todo_ownership.py"
  "py_idiom|python3 scripts/check_py_idiom.py"
  "cpp_idiom|python3 scripts/check_cpp_idiom.py"
  "baremetal_only|python3 scripts/check_baremetal_only.py --check"
  "port_contracts|python3 scripts/check_port_contracts.py"
  "nvm_record_space|python3 scripts/check_nvm_record_space.py"
  "nvm_klj3|python3 scripts/check_nvm_klj3.py"
  "nvm_capture|python3 scripts/check_nvm_capture.py"
  "nvm_format_32x32|python3 scripts/check_nvm_format_32x32.py"
  "measure_test_evidence|python3 scripts/measure_test_evidence.py --check"
  "measure_naming|python3 scripts/measure_naming.py --check"
  "measure_fail_fast|python3 scripts/measure_fail_fast.py --check"
  "module_matrix|python3 docs/traceability/gen_module_matrix.py --check"
  "submodule_diagram|python3 docs/diagrams/submodule_boundaries.gen.py --check"
  "timesync_diagram|python3 docs/diagrams/timesync_chain.gen.py --check"
  "diagram_pngs|python3 scripts/check_diagram_pngs.py"
)
pids=()
for g in "${gates[@]}"; do
  name=${g%%|*}; cmd=${g#*|}
  ( start=$(date +%s); bash -c "$cmd" >"$out/$name.log" 2>&1; rc=$?
    echo "$rc" >"$out/$name.rc"; echo "$name rc=$rc $(( $(date +%s)-start ))s :: $cmd" >>"$out/summary.txt" ) &
  pids+=($!)
  while [ "$(jobs -rp | wc -l)" -ge 16 ]; do sleep 1; done
done
wait
sort "$out/summary.txt" -o "$out/summary.txt"
cat "$out/summary.txt"
