#!/bin/sh
# Run the lane-0 documentation gates at the checked-out head; each gate's own
# exit status is recorded (no pipeline masks it).
# Usage: sh run_docs_gates.sh <python-with-locked-renderer> <base> <tmpdir>
set -u
PY=$1; BASE=$2; T=$3
echo "### head $(git rev-parse HEAD)"
for cmd in "scripts/docs_check.py" "scripts/check_doc_paths.py" "scripts/check_doc_style.py" \
           "scripts/gen_toc.py --check" "scripts/check_em_dash.py --base $BASE" \
           "scripts/check_baremetal_only.py --check" "scripts/ci_scope.py --selftest"; do
  echo "### python $cmd"
  $PY $cmd > "$T/gate.out" 2>&1; rc=$?
  tail -n 3 "$T/gate.out"
  echo "### rc=$rc"
done
echo "### git diff --check"; git diff --check; echo "### rc=$?"
echo "### git diff --check $BASE HEAD"; git diff --check "$BASE" HEAD; echo "### rc=$?"
