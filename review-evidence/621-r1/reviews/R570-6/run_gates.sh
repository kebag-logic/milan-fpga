#!/usr/bin/env bash
# Runs the documentation and diagram gates named for the R570-6 delta round
# concurrently against a clean checkout of the exact head.
# Usage: run_gates.sh <checkout> <receipt-dir> [python]
# Each gate writes <name>.log and <name>.rc into <receipt-dir>.
set -u
repo=$1
out=$2
py=${3:-python3}
mkdir -p "$out"
cd "$repo" || exit 2

run() {
  local name=$1; shift
  ( "$@" >"$out/$name.log" 2>&1; echo $? >"$out/$name.rc" ) &
}

run docs_check            "$py" scripts/docs_check.py
run em_dash_base_cfadd767 "$py" scripts/check_em_dash.py --base cfadd767a7ad47aaee68de655e1066cc000fb8a0
run em_dash_base_mergebase "$py" scripts/check_em_dash.py --base "$(git merge-base cfadd767a7ad47aaee68de655e1066cc000fb8a0 HEAD)"
run em_dash_selftest      "$py" scripts/check_em_dash.py --selftest
run gen_toc_check         "$py" scripts/gen_toc.py --check
run gen_toc_anchors       "$py" scripts/gen_toc.py --verify-anchors
run gen_toc_selftest      "$py" scripts/gen_toc.py --selftest
run check_doc_paths       "$py" scripts/check_doc_paths.py
run ci_events_check       "$py" scripts/ci_events.py --check
run ci_events_selftest    "$py" scripts/ci_events.py --selftest
run mte_check             "$py" scripts/measure_test_evidence.py --check
run mte_selftest          "$py" scripts/measure_test_evidence.py --selftest
run submodule_docs        "$py" scripts/check_submodule_docs.py
run submodule_docs_selftest "$py" scripts/check_submodule_docs.py --selftest
run diagram_pngs          "$py" scripts/check_diagram_pngs.py
run diagram_pngs_selftest "$py" scripts/check_diagram_pngs.py --selftest
run gen_submodule_check   "$py" docs/diagrams/submodule_boundaries.gen.py --check
run gen_submodule_selftest "$py" docs/diagrams/submodule_boundaries.gen.py --selftest
run gen_timesync_check    "$py" docs/diagrams/timesync_chain.gen.py --check
run gen_timesync_selftest "$py" docs/diagrams/timesync_chain.gen.py --selftest
run doc_map_check         "$py" docs/DOC_MAP.gen.py --check
run doc_style             "$py" scripts/check_doc_style.py
run gptp_docs             "$py" scripts/check_gptp_docs.py
run module_matrix_check   "$py" docs/traceability/gen_module_matrix.py --check
wait
for f in "$out"/*.rc; do printf '%s %s\n' "$(cat "$f")" "$(basename "$f" .rc)"; done | sort -k2
