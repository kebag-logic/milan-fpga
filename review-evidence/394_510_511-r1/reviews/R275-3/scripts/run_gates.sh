#!/usr/bin/env bash
# Run the documentation-scope gates that read the files this PR composes
# with its predecessors, on one candidate tree. Portable: pass the clone
# root, the output directory and the candidate's first parent.
#   run_gates.sh <repo> <outdir> <parent-rev>
set -u
repo=$1; out=$2; parent=$3
mkdir -p "$out"
cd "$repo" || exit 2
summary="$out/SUMMARY.tsv"
printf 'rc\tgate\n' > "$summary"
run() {
    local name=$1; shift
    local log="$out/$name.log"
    { printf '$ %s\n' "$*"; "$@"; } > "$log" 2>&1
    local rc=$?
    printf '%s\t%s\n' "$rc" "$name" >> "$summary"
}
run docs_check                python3 scripts/docs_check.py
run em_dash_base_parent       python3 scripts/check_em_dash.py --base "$parent"
run em_dash_selftest          python3 scripts/check_em_dash.py --selftest
run doc_style                 python3 scripts/check_doc_style.py
run doc_style_selftest        python3 scripts/check_doc_style.py --selftest
run gptp_docs                 python3 scripts/check_gptp_docs.py
run gptp_docs_with_submodule  python3 scripts/check_gptp_docs.py --with-submodule
run gptp_docs_selftest        python3 scripts/check_gptp_docs.py --selftest
run doc_map_check             python3 docs/DOC_MAP.gen.py --check
run doc_map_selftest          python3 docs/DOC_MAP.gen.py --selftest
run timesync_chain_check      python3 docs/diagrams/timesync_chain.gen.py --check
run solution_docs             python3 scripts/check_solution_docs.py
run solution_docs_selftest    python3 scripts/check_solution_docs.py --selftest
run submodule_boundaries      python3 docs/diagrams/submodule_boundaries.gen.py --check
run submodule_docs            python3 scripts/check_submodule_docs.py
run submodule_docs_selftest   python3 scripts/check_submodule_docs.py --selftest
run diagram_pngs              python3 scripts/check_diagram_pngs.py
run feature_status            python3 scripts/check_feature_status.py
run feature_status_selftest   python3 scripts/check_feature_status.py --self-test
run module_matrix_check       python3 docs/traceability/gen_module_matrix.py --check
run ci_events_check           python3 scripts/ci_events.py --check
run ci_events_selftest        python3 scripts/ci_events.py --selftest
run doc_paths                 python3 scripts/check_doc_paths.py
run archive                   python3 scripts/check_archive.py
run toc_selftest              python3 scripts/gen_toc.py --selftest
run toc_verify_anchors        python3 scripts/gen_toc.py --verify-anchors
run toc_check                 python3 scripts/gen_toc.py --check
run hygiene_check             python3 scripts/check_hygiene.py --check
run baremetal_only_check      python3 scripts/check_baremetal_only.py --check
run port_contracts            python3 scripts/check_port_contracts.py
run test_evidence_check       python3 scripts/measure_test_evidence.py --check
run todo_ownership            python3 scripts/check_todo_ownership.py
cat "$summary"
