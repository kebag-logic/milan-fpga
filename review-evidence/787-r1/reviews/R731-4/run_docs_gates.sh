#!/usr/bin/env bash
# Run the docs-workflow gates that read the reviewed delta, in parallel.
# Usage: run_docs_gates.sh <repo-checkout> <out-dir> <em-dash-base-sha>
set -u
REPO=$1; OUT=$2; BASE=$3
mkdir -p "$OUT"
cd "$REPO" || exit 2
cat > "$OUT/gates.list" <<EOF
docs_check|python3 scripts/docs_check.py
em_dash|python3 scripts/check_em_dash.py --base $BASE
doc_style|python3 scripts/check_doc_style.py
doc_style_selftest|python3 scripts/check_doc_style.py --selftest
gptp_docs|python3 scripts/check_gptp_docs.py
doc_map_check|python3 docs/DOC_MAP.gen.py --check
timesync_check|python3 docs/diagrams/timesync_chain.gen.py --check
solution_docs|python3 scripts/check_solution_docs.py
submodule_boundaries_check|python3 docs/diagrams/submodule_boundaries.gen.py --check
submodule_docs|python3 scripts/check_submodule_docs.py
submodule_docs_selftest|python3 scripts/check_submodule_docs.py --selftest
diagram_pngs|python3 scripts/check_diagram_pngs.py
diagram_pngs_selftest|python3 scripts/check_diagram_pngs.py --selftest
feature_status|python3 scripts/check_feature_status.py
traceability|python3 docs/traceability/gen_module_matrix.py --check
resource_gate_selftest|python3 syn/ooc/pp_resource_gate_selftest.py
EOF
run_one() {
  name=${1%%|*}; cmd=${1#*|}
  bash -c "$cmd" > "$OUT/$name.log" 2>&1
  echo $? > "$OUT/$name.rc"
}
export -f run_one; export OUT
xargs -P 16 -I{} -d '\n' bash -c 'run_one "$@"' _ {} < "$OUT/gates.list"
for f in "$OUT"/*.rc; do printf '%s rc=%s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done | tee "$OUT/SUMMARY.txt"
