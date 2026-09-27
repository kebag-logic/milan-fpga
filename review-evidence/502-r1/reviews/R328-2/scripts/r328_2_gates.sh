#!/bin/bash
# R328-2 repository gates at the exact head, run in a disposable clone.
# Usage: r328_2_gates.sh <tree> <receipt-dir> <python-with-markdown-deps>
set -u
T=$1; R=$2; PY=$3
BASE=831f94f4146cc45ec476f8c8dcf5afac7cd8eacf
HEAD_SHA=5d4cf33e3709c35d4f5bc90d3c5a2334ef3bfd8e
mkdir -p "$R/gates"
SUM="$R/gates_summary.txt"; : > "$SUM"
cd "$T" || exit 2
gate() {
  local name=$1; shift
  local s; s=$(date +%s)
  "$@" > "$R/gates/$name.log" 2>&1
  local rc=$?
  echo "$name rc=$rc ($(( $(date +%s) - s ))s) :: $*" | sed "s|$T|<tree>|g" >> "$SUM"
}
gate diff_check_base_head git diff --check $BASE $HEAD_SHA
gate diff_check_delta git diff --check 104c8a54b183cd9215ed1e3a2e1be1634f48d33d $HEAD_SHA
gate lint_rtl python3 scripts/lint_rtl.py --check
gate em_dash "$PY" scripts/check_em_dash.py --base $BASE
gate doc_style "$PY" scripts/check_doc_style.py
gate gen_toc_check "$PY" scripts/gen_toc.py --check
gate gen_toc_anchors "$PY" scripts/gen_toc.py --verify-anchors
gate doc_paths "$PY" scripts/check_doc_paths.py
gate submodule_docs "$PY" scripts/check_submodule_docs.py
gate diagram_gen "$PY" docs/diagrams/submodule_boundaries.gen.py --check
gate diagram_pngs "$PY" scripts/check_diagram_pngs.py
gate test_evidence "$PY" scripts/measure_test_evidence.py --check
gate port_contracts "$PY" scripts/check_port_contracts.py
gate sv_idiom "$PY" scripts/check_sv_idiom.py
gate cpp_idiom "$PY" scripts/check_cpp_idiom.py
gate py_idiom "$PY" scripts/check_py_idiom.py
gate rtl_source_lists "$PY" scripts/check_rtl_source_lists.py
gate naming "$PY" scripts/measure_naming.py --check
gate docs_check "$PY" -B scripts/docs_check.py
gate wire_acct "$PY" scripts/check_wire_accountability.py
gate feature_status "$PY" scripts/check_feature_status.py
gate module_matrix "$PY" docs/traceability/gen_module_matrix.py --check
gate xvlog_gate "$PY" scripts/xvlog_gate.py --check
gate ci_events "$PY" scripts/ci_events.py --check
gate nvm_capture "$PY" scripts/check_nvm_capture.py
gate baremetal_only "$PY" scripts/check_baremetal_only.py --check
gate nvm_fw_selftest "$PY" sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
gate nvm_backend make -C tb/verilator/nvm_backend
# no-git documentation mode, as the hosted docs-check-no-git job runs it
NG="$T/../tree_nogit"; rm -rf "$NG"; cp -a "$T" "$NG"; rm -rf "$NG/.git"
( cd "$NG" && gate_ng() { :; } )
s=$(date +%s); ( cd "$NG" && "$PY" scripts/docs_check.py && "$PY" scripts/check_feature_status.py ) > "$R/gates/docs_check_nogit.log" 2>&1
echo "docs_check_nogit rc=$? ($(( $(date +%s) - s ))s) :: rm -rf .git; docs_check.py; check_feature_status.py" >> "$SUM"
rm -rf "$NG"
cat "$SUM"
