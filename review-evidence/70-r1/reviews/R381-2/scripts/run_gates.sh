#!/usr/bin/env bash
# Run the lane-0 documentation gates at the clone's HEAD, foreground, no pipelines.
# Usage: run_gates.sh <clone> <python-with-locked-markdown-deps> <base-sha>
set -u
C="$1"; PY="$2"; BASE="$3"
export PYTHONDONTWRITEBYTECODE=1
cd "$C" || exit 2
echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree})"
fail=0
run() { echo "## $*"; "$@"; rc=$?; echo "exit $rc"; [ $rc -eq 0 ] || fail=1; }
run "$PY" scripts/docs_check.py
run "$PY" scripts/check_doc_paths.py
run "$PY" scripts/check_doc_style.py
run "$PY" scripts/gen_toc.py --check
run "$PY" scripts/check_em_dash.py --base "$BASE"
run "$PY" scripts/check_baremetal_only.py --check
run "$PY" scripts/ci_scope.py --selftest
run "$PY" scripts/check_feature_status.py
run git diff --check
run git diff --check "$BASE" HEAD
echo "overall $fail"
exit $fail
