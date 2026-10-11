#!/bin/bash
# Reviewer gate subset (R593-2): the repository gates the M7 diff touches.
# Usage: run_gates.sh <clone> <out dir> <py312> <md python> <verilator dir>
# Each gate gets its own log and rc file; up to 8 run at once; none is piped.
set -u
CLONE=$1; OUT=$2; PY=$3; MD=$4; VDIR=$5
BASE=e8454e2751d05b02ee8e5a571857589ab358ab86
mkdir -p "$OUT"
cd "$CLONE" || exit 2
gates=(
  "gptp_docs|$MD scripts/check_gptp_docs.py"
  "gptp_docs_sub|$MD scripts/check_gptp_docs.py --with-submodule"
  "docs_check|$MD scripts/docs_check.py"
  "module_matrix|$MD docs/traceability/gen_module_matrix.py --check"
  "toc_check|$MD scripts/gen_toc.py --check"
  "toc_anchors|$MD scripts/gen_toc.py --verify-anchors"
  "doc_style|$MD scripts/check_doc_style.py"
  "em_dash|$MD scripts/check_em_dash.py --base $BASE"
  "doc_paths|$MD scripts/check_doc_paths.py"
  "doc_map|$MD docs/DOC_MAP.gen.py --check"
  "submodule_docs|$MD scripts/check_submodule_docs.py"
  "submodule_diagram|$MD docs/diagrams/submodule_boundaries.gen.py --check"
  "timesync|$MD docs/diagrams/timesync_chain.gen.py --check"
  "diagram_pngs|$MD scripts/check_diagram_pngs.py"
  "py_idiom|$PY scripts/check_py_idiom.py"
  "cpp_idiom|$PY scripts/check_cpp_idiom.py"
  "sv_idiom|$PY scripts/check_sv_idiom.py"
  "naming|$PY scripts/measure_naming.py --check"
  "test_evidence|$PY scripts/measure_test_evidence.py --check"
  "hygiene|$PY scripts/check_hygiene.py --check"
  "rtl_source_lists|$PY scripts/check_rtl_source_lists.py"
  "port_contracts|$PY scripts/check_port_contracts.py"
  "sweep_shape|$PY scripts/check_sweep_shape.py"
  "resource_baseline|$PY syn/ooc/pp_resource_gate.py check-baseline"
  "lint|env PATH=$VDIR:$PATH $PY scripts/lint_rtl.py --check"
  "gp_contract|env PATH=$VDIR:$PATH make -C gptp-processor contract"
  "gp_lint|env PATH=$VDIR:$PATH make -C gptp-processor lint"
  "diff_check|git diff --check $BASE HEAD"
)
run_one() {
  local name=$1 cmd=$2
  echo "$cmd" > "$OUT/$name.cmd"
  bash -c "$cmd" > "$OUT/$name.log" 2>&1
  echo $? > "$OUT/$name.rc"
}
for g in "${gates[@]}"; do
  name=${g%%|*}; cmd=${g#*|}
  while [ "$(jobs -rp | wc -l)" -ge 8 ]; do wait -n; done
  run_one "$name" "$cmd" &
done
wait
for f in "$OUT"/*.rc; do printf '%s %s\n' "$(cat "$f")" "$(basename "$f" .rc)"; done
