#!/usr/bin/env bash
# Run the static documentation and inventory gates on a checkout, in parallel,
# one log and rc file per gate. Usage: run_gates.sh REPO PYTHON OUT_DIR
# PYTHON must have the pinned Markdown renderer and pyyaml importable.
set -uo pipefail
REPO=$1 PY=$2 OUT=$3
mkdir -p "$OUT"
cd "$REPO" || exit 2
gates=(
  "check_doc_style_selftest|scripts/check_doc_style.py --selftest"
  "check_gptp_docs|scripts/check_gptp_docs.py"
  "doc_map_check|docs/DOC_MAP.gen.py --check"
  "timesync_chain_check|docs/diagrams/timesync_chain.gen.py --check"
  "check_solution_docs|scripts/check_solution_docs.py"
  "submodule_boundaries_check|docs/diagrams/submodule_boundaries.gen.py --check"
  "check_submodule_docs|scripts/check_submodule_docs.py"
  "check_diagram_pngs|scripts/check_diagram_pngs.py"
  "check_baremetal_only|scripts/check_baremetal_only.py --check"
  "check_nvm_record_space|scripts/check_nvm_record_space.py"
  "check_soc_sources|scripts/check_soc_sources.py"
  "check_rtl_source_lists|scripts/check_rtl_source_lists.py"
  "measure_naming|scripts/measure_naming.py --check"
  "check_port_contracts|scripts/check_port_contracts.py"
  "measure_fail_fast|scripts/measure_fail_fast.py --check"
  "check_todo_ownership|scripts/check_todo_ownership.py"
  "measure_test_evidence|scripts/measure_test_evidence.py --check"
  "check_hygiene|scripts/check_hygiene.py --check"
  "check_sv_idiom|scripts/check_sv_idiom.py"
  "check_cpp_idiom|scripts/check_cpp_idiom.py"
  "check_py_idiom|scripts/check_py_idiom.py"
  "check_sh_idiom|scripts/check_sh_idiom.py"
  "check_archive|scripts/check_archive.py"
  "check_feature_status|scripts/check_feature_status.py"
  "gen_toc_selftest|scripts/gen_toc.py --selftest"
)
for g in "${gates[@]}"; do printf '%s\n' "$g"; done |
  xargs -P 12 -I{} bash -c '
    n=${1%%|*}; c=${1#*|}
    timeout 580s "$2" -I $c >"$3/$n.log" 2>&1; echo $? >"$3/$n.rc"
  ' _ {} "$PY" "$OUT"
for g in "${gates[@]}"; do
  n=${g%%|*}
  printf '%s rc=%s %s\n' "$n" "$(cat "$OUT/$n.rc")" "$(tail -n 1 "$OUT/$n.log" | cut -c1-160)"
done
