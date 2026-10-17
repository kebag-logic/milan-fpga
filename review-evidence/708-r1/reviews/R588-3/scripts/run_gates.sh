#!/usr/bin/env bash
# Run the composition-relevant docs/script gates on a candidate checkout.
# usage: run_gates.sh <repo> <outdir> <em-dash-base>
set -u
repo=$1; out=$2; base=$3
mkdir -p "$out"
cd "$repo" || exit 2
run() { name=$1; shift; ( "$@" >"$out/$name.log" 2>&1; echo $? >"$out/$name.rc" ) & }
run docs_check            python3 scripts/docs_check.py
run feature_status        python3 scripts/check_feature_status.py
run feature_status_st     python3 scripts/check_feature_status.py --self-test
run em_dash               python3 scripts/check_em_dash.py --base "$base"
run doc_style             python3 scripts/check_doc_style.py
run doc_style_st          python3 scripts/check_doc_style.py --selftest
run gptp_docs             python3 scripts/check_gptp_docs.py
run solution_docs         python3 scripts/check_solution_docs.py
run submodule_docs        python3 scripts/check_submodule_docs.py
run submodule_docs_st     python3 scripts/check_submodule_docs.py --selftest
run diagram_pngs          python3 scripts/check_diagram_pngs.py
run module_matrix         python3 docs/traceability/gen_module_matrix.py --check
run baremetal             python3 scripts/check_baremetal_only.py --check
run baremetal_st          python3 scripts/check_baremetal_only.py --selftest
run port_contracts        python3 scripts/check_port_contracts.py
run naming                python3 scripts/measure_naming.py --check
run test_evidence         python3 scripts/measure_test_evidence.py --check
run test_evidence_st      python3 scripts/measure_test_evidence.py --selftest
run hygiene               python3 scripts/check_hygiene.py --check
run py_idiom              python3 scripts/check_py_idiom.py
run doc_paths             python3 scripts/check_doc_paths.py
run archive               python3 scripts/check_archive.py
run toc_anchors           python3 scripts/gen_toc.py --verify-anchors
run toc_check             python3 scripts/gen_toc.py --check
run toc_st                python3 scripts/gen_toc.py --selftest
run ci_events_check       python3 scripts/ci_events.py --check
run ci_events_st          python3 scripts/ci_events.py --selftest
run ci_gate_wf_st         python3 scripts/ci_gate_workflows_selftest.py
run ci_gate_wf_check      python3 scripts/ci_gate_workflows.py --check
run fail_fast             python3 scripts/measure_fail_fast.py --check
run todo_owner            python3 scripts/check_todo_ownership.py
run sv_idiom              python3 scripts/check_sv_idiom.py
run cpp_idiom             python3 scripts/check_cpp_idiom.py
run rom_digests_ws        git diff --check 1f6f2f57177f1dd904654c317009461b43423989 HEAD
wait
for f in "$out"/*.rc; do printf '%s %s\n' "$(cat "$f")" "$(basename "$f" .rc)"; done | sort -k2
