#!/usr/bin/env bash
# Usage: gates.sh <repo> <out-dir> <md-python>
# Runs the head gates named by the round brief concurrently; one log and rc file per gate.
set -u
REPO=$1; OUT=$2; MDPY=$3
mkdir -p "$OUT"; cd "$REPO" || exit 2
DEV=5fcec84b1aa72c43048eff28bb63a982add830dd
git cat-file -e "$DEV^{commit}" 2>/dev/null || git fetch --quiet origin "$DEV"
BASE=$(git merge-base HEAD "$DEV"); echo "$BASE" > "$OUT/em_dash_base.txt"
run() { local n=$1; shift; ( "$@" > "$OUT/$n.log" 2>&1; echo $? > "$OUT/$n.rc" ) & }
run check_py_idiom          python3 -I scripts/check_py_idiom.py
run check_py_idiom_selftest python3 -I scripts/check_py_idiom.py --selftest
run suite_shards_selftest   python3 -I scripts/suite_shards.py --selftest
run ci_events_check         python3 -I scripts/ci_events.py --check
run ci_gate_workflows_check python3 -I scripts/ci_gate_workflows.py --check
run docs_check              "$MDPY" -I scripts/docs_check.py
run check_doc_style         python3 -I scripts/check_doc_style.py
run check_doc_style_selftest python3 -I scripts/check_doc_style.py --selftest
run check_em_dash           "$MDPY" -I scripts/check_em_dash.py --base "$BASE"
run gen_toc_check           "$MDPY" -I scripts/gen_toc.py --check
run gen_toc_verify_anchors  "$MDPY" -I scripts/gen_toc.py --verify-anchors
wait
for f in "$OUT"/*.rc; do printf '%s rc=%s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
