#!/usr/bin/env bash
# Runs the documentation gates that read the files PR #828 changes, concurrently, one log and rc per gate.
# usage: run_gates.sh <clone> <out_dir> <base_rev>
clone=$1; out=$2; base=$3
cd "$clone" || exit 2
export PYTHONDONTWRITEBYTECODE=1
run() { local n=$1; shift; ( "$@" >"$out/$n.log" 2>&1; echo $? >"$out/$n.rc" ) & }
run docs_check            python3 scripts/docs_check.py
run feature_status        python3 scripts/check_feature_status.py
run feature_status_self   python3 scripts/check_feature_status.py --self-test
run em_dash_parent        python3 scripts/check_em_dash.py --base "$base"
run em_dash_self          python3 scripts/check_em_dash.py --selftest
run doc_style             python3 scripts/check_doc_style.py
run doc_style_self        python3 scripts/check_doc_style.py --selftest
run gptp_docs             python3 scripts/check_gptp_docs.py
run doc_map               python3 docs/DOC_MAP.gen.py --check
run solution_docs         python3 scripts/check_solution_docs.py
run submodule_docs        python3 scripts/check_submodule_docs.py
run diagram_pngs          python3 scripts/check_diagram_pngs.py
run traceability          python3 docs/traceability/gen_module_matrix.py --check
run doc_paths             python3 scripts/check_doc_paths.py
run archive               python3 scripts/check_archive.py
run toc_check             python3 scripts/gen_toc.py --check
run toc_anchors           python3 scripts/gen_toc.py --verify-anchors
run toc_self              python3 scripts/gen_toc.py --selftest
run ci_events_check       python3 scripts/ci_events.py --check
run ci_events_self        python3 scripts/ci_events.py --selftest
run wire_accountability   python3 scripts/check_wire_accountability.py
run todo_ownership        python3 scripts/check_todo_ownership.py
run hygiene               python3 scripts/check_hygiene.py --check
wait
