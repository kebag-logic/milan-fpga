#!/bin/sh
# Spot-check of docs.yml run: steps that need no apt, SDK, submodule or network.
# Usage: docs_steps.sh <clean clone at the head> <receipt dir>
C=$1; O=$2; cd "$C" || exit 2
run() { name=$1; shift; "$@" > "$O/docs_$name.log" 2>&1; echo "$name rc=$?" >> "$O/docs_steps_rc.txt"; }
: > "$O/docs_steps_rc.txt"
run docs_check python3 scripts/docs_check.py
run doc_style python3 scripts/check_doc_style.py
run doc_style_selftest python3 scripts/check_doc_style.py --selftest
run doc_map python3 docs/DOC_MAP.gen.py --check
run doc_paths python3 scripts/check_doc_paths.py
run toc_selftest python3 scripts/gen_toc.py --selftest
run toc_anchors python3 scripts/gen_toc.py --verify-anchors
run toc_check python3 scripts/gen_toc.py --check
run inventory_check python3 scripts/docs_inventory.py --check
run inventory_selftest python3 scripts/docs_inventory.py --selftest
run archive python3 scripts/check_archive.py
run hygiene python3 scripts/check_hygiene.py --check
run py_idiom python3 scripts/check_py_idiom.py
run fail_fast python3 scripts/measure_fail_fast.py --check
run test_evidence python3 scripts/measure_test_evidence.py --check
run todo python3 scripts/check_todo_ownership.py
run feature_status python3 scripts/check_feature_status.py --self-test
run ci_gate_workflows python3 scripts/ci_gate_workflows.py --check
run ci_events python3 scripts/ci_events.py --check
git status --porcelain > "$O/docs_steps_status_after.txt"
