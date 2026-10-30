#!/usr/bin/env bash
# md_gates.sh PY BASE : the renderer-dependent documentation gates, with interpreter PY
cd "$(git rev-parse --show-toplevel)" || exit 2
py=$1; base=$2; fail=0
run() { echo "### $*"; "$@"; rc=$?; echo "### rc=$rc :: $*"; [ $rc = 0 ] || fail=1; }
run "$py" scripts/check_em_dash.py --base "$base"
run "$py" scripts/gen_toc.py --verify-anchors
run "$py" scripts/gen_toc.py --check
echo "### overall fail=$fail"; exit $fail
