#!/bin/bash
# gates.sh: every gate this round's changes touch, at r3/wt/gates' head, one log each; summary in r3/gates/summary
set -u
W=/data-2/milan/tmp/cicd-a839/r3/wt/gates; O=/data-2/milan/tmp/cicd-a839/r3/gates; rm -rf $O; mkdir -p $O
. /data-2/milan/tmp/cicd-a839/r3/bin/env.sh
MD=/data-2/milan/tmp/cicd-a839/r3/mdvenv/bin/python
cd $W || exit 99
echo "head $(git rev-parse HEAD)" > $O/summary
run() { n=$1; shift; s=$(date +%s); "$@" > "$O/$n.log" 2>&1; rc=$?; echo "$n rc=$rc $(( $(date +%s)-s ))s :: $(tail -n1 "$O/$n.log" | cut -c1-140)" >> $O/summary; }
run ci_gate_workflows_check python3 scripts/ci_gate_workflows.py --check
run ci_events_check python3 scripts/ci_events.py --check
for t in ci_gate_workflows_selftest ci_case_receipts_selftest ci_make_cases_selftest ci_maap_cases_selftest ci_capture_cases_selftest ci_suite_pieces_selftest ci_suite_collect_selftest ci_fail_fast_selftest ci_runtime_evidence_selftest ci_install_cache_selftest ci_workflow_plan_selftest ci_manifest_selftest; do run $t python3 scripts/$t.py; done
run generate_ci_evidence_pins python3 scripts/generate_ci_evidence_pins.py --check
run mutant_stage python3 scripts/mutant_stage.py --selftest
run suite_shards python3 scripts/suite_shards.py --selftest
run test_suite_cancellation python3 scripts/test_suite_cancellation.py
run gptp_shadow_lifecycle bash -c 'cd tb/verilator/gptp_shadow && python3 test_mutant_lifecycle.py'
run check_py_idiom python3 scripts/check_py_idiom.py
run check_sh_idiom python3 scripts/check_sh_idiom.py
run check_hygiene python3 scripts/check_hygiene.py --check
run measure_naming python3 scripts/measure_naming.py --check
run measure_fail_fast python3 scripts/measure_fail_fast.py --check
run measure_test_evidence python3 scripts/measure_test_evidence.py --check
run check_todo_ownership python3 scripts/check_todo_ownership.py
run check_doc_paths python3 scripts/check_doc_paths.py
run check_doc_style python3 scripts/check_doc_style.py
run docs_check python3 scripts/docs_check.py
run check_archive python3 scripts/check_archive.py
run docs_inventory python3 scripts/docs_inventory.py --check
run gen_toc_check $MD scripts/gen_toc.py --check
run gen_toc_anchors $MD scripts/gen_toc.py --verify-anchors
run check_em_dash $MD scripts/check_em_dash.py --base fcbc31f380
run ci_events_selftest python3 scripts/ci_events.py --selftest
echo done >> $O/summary
