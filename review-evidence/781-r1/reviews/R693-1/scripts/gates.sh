#!/bin/bash
# usage: gates.sh <repo> <outdir> <python>   runs the docs/CI gate commands that read this diff, each concurrently, rc per gate
repo=$1; out=$2; PY=$3; mkdir -p "$out"; cd "$repo" || exit 2
run() { name=$1; shift; ( "$@" > "$out/$name.log" 2>&1; echo $? > "$out/$name.rc" ) & }
run docs_check $PY scripts/docs_check.py
run em_dash $PY scripts/check_em_dash.py --base a032c6d6e3775f145349d5a495c1e1ad12294936
run doc_style $PY scripts/check_doc_style.py
run doc_style_self $PY scripts/check_doc_style.py --selftest
run doc_map $PY docs/DOC_MAP.gen.py --check
run feature_status $PY scripts/check_feature_status.py --self-test
run test_evidence $PY scripts/measure_test_evidence.py --check
run test_evidence_self $PY scripts/measure_test_evidence.py --selftest
run hygiene $PY scripts/check_hygiene.py --check
run py_idiom $PY scripts/check_py_idiom.py
run sh_idiom $PY scripts/check_sh_idiom.py
run doc_paths $PY scripts/check_doc_paths.py
run archive $PY scripts/check_archive.py
run toc_anchors $PY scripts/gen_toc.py --verify-anchors
run toc_check $PY scripts/gen_toc.py --check
run gate_workflows $PY scripts/ci_gate_workflows.py --check
run gate_workflows_self $PY scripts/ci_gate_workflows_selftest.py
run suite_pieces_self $PY scripts/ci_suite_pieces_selftest.py
run suite_collect_self $PY scripts/ci_suite_collect_selftest.py
run fail_fast_self $PY scripts/ci_fail_fast_selftest.py
run evidence_pins $PY scripts/generate_ci_evidence_pins.py --check
run workflow_plan_self $PY scripts/ci_workflow_plan_selftest.py
run manifest_self $PY scripts/ci_manifest_selftest.py
run runtime_evidence_self $PY scripts/ci_runtime_evidence_selftest.py
run ci_events $PY scripts/ci_events.py --check
run ci_events_self $PY scripts/ci_events.py --selftest
wait
for f in "$out"/*.rc; do printf '%s %s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
