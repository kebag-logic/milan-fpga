#!/usr/bin/env bash
# Run selected documentation gates at the head concurrently, each with its own log and rc.
# Usage: run_doc_gates.sh <repo clone at head> <packet dir> <venv python>
set -u
REPO="$1"; P="$2"; VPY="$3"
R="$P/receipts/docgates"; mkdir -p "$R"
cd "$REPO" || exit 2
run() { local name="$1"; shift; ( "$@" > "$R/$name.log" 2>&1; echo $? > "$R/$name.rc" ) & }
run em_dash "$VPY" scripts/check_em_dash.py --base 9ef717727e6fdac11ee7f01672fefae948452343
run py_idiom bash -c "'$VPY' scripts/check_py_idiom.py && '$VPY' scripts/check_py_idiom.py --selftest"
run doc_paths "$VPY" scripts/check_doc_paths.py
run toc bash -c "'$VPY' scripts/gen_toc.py --verify-anchors && '$VPY' scripts/gen_toc.py --check"
run doc_style "$VPY" scripts/check_doc_style.py
run docs_check "$VPY" scripts/docs_check.py
wait
for f in "$R"/*.rc; do printf '%s %s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
