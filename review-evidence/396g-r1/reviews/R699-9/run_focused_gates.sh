#!/bin/sh
# Usage: run_focused_gates.sh <repo> <out dir>
# Runs the cross-file documentation and workflow-consistency gates the merge could affect, concurrently, one log and rc per gate.
cd "$1"; O=$2
run(){ n=$1; shift; ( "$@" > "$O/$n.log" 2>&1; echo $? > "$O/$n.rc" ) & }
run docs_check python3 scripts/docs_check.py
run gen_toc_anchors python3 scripts/gen_toc.py --verify-anchors
run gen_toc_check python3 scripts/gen_toc.py --check
run doc_paths python3 scripts/check_doc_paths.py
run doc_style python3 scripts/check_doc_style.py
run ci_gate_workflows python3 scripts/ci_gate_workflows.py --check
run ci_events python3 scripts/ci_events.py --check
run hygiene python3 scripts/check_hygiene.py --check
run py_idiom python3 scripts/check_py_idiom.py
wait
for f in "$O"/*.rc; do printf '%s rc=%s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
