#!/bin/sh
# Run the docs.yml gates whose inputs this PR changes, on one clean clone, each in sbx.sh.
# Usage: gates.sh <clone> <out-dir> <sbx.sh> <base-sha>
c=$1; o=$2; sbx=$3; base=$4; mkdir -p "$o"
run() { n=$1; shift; "$sbx" "$o/$n" "$c" sh -c "$*" & }
run docs_check 'python3 scripts/docs_check.py'
run em_dash "python3 scripts/check_em_dash.py --base $base"
run doc_style 'python3 scripts/check_doc_style.py'
run doc_paths 'python3 scripts/check_doc_paths.py'
run toc 'python3 scripts/gen_toc.py --verify-anchors'
run docs_inventory 'python3 scripts/docs_inventory.py --check'
run py_idiom 'python3 scripts/check_py_idiom.py'
run hygiene 'python3 scripts/check_hygiene.py --check'
run fail_fast 'python3 scripts/measure_fail_fast.py --check'
run test_evidence 'python3 scripts/measure_test_evidence.py --check'
run naming 'python3 scripts/measure_naming.py --check'
run todo 'python3 scripts/check_todo_ownership.py'
run ci_gate_workflows 'python3 scripts/ci_gate_workflows.py --check'
run ci_events 'python3 scripts/ci_events.py --check'
run diff_check "git diff --check $base HEAD"
wait
for f in "$o"/*.rc; do printf '%s rc=%s | %s\n' "$(basename "$f" .rc)" "$(cat "$f")" "$(tail -1 "${f%.rc}.log" | cut -c1-150)"; done
