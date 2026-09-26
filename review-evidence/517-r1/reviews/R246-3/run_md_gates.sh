#!/bin/sh
# Renderer-dependent documentation gates, with an interpreter that carries the
# pins in tools/markdown/requirements.txt. usage: run_md_gates.sh <clone> <parent-rev> <python>
C="$1"; BASE="$2"; PY="$3"
cd "$C" || exit 2
fail=0
gate() {
    out=$("$@" 2>&1); rc=$?
    printf 'GATE rc=%s %s\n' "$rc" "$*"
    printf '%s\n' "$out" | tail -n 4 | sed 's/^/    | /'
    [ "$rc" -eq 0 ] || fail=1
}
gate "$PY" scripts/check_em_dash.py --base "$BASE"
gate "$PY" scripts/check_em_dash.py --selftest
gate "$PY" scripts/gen_toc.py --selftest
gate "$PY" scripts/gen_toc.py --verify-anchors
gate "$PY" scripts/gen_toc.py --check
gate "$PY" scripts/docs_check.py
echo "ALL_MD_GATES_FAIL=$fail"
exit "$fail"
