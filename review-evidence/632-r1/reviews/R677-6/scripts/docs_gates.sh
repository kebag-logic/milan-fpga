#!/usr/bin/env bash
# Run the docs gates touched by the round-6 delta at the checked-out head.
# Usage: docs_gates.sh <clone> <outdir> <python-with-html5lib> <em-dash-base>
set -u
C=$1; O=$2; PYH=$3; BASE=$4
cd "$C" || exit 2
run() { n=$1; shift; "$@" >"$O/$n.log" 2>&1; echo "$n rc=$?" | tee -a "$O/summary.txt"; }
: > "$O/summary.txt"
echo "head $(git rev-parse HEAD)" >> "$O/summary.txt"
run docs_check            python3 scripts/docs_check.py
run check_doc_paths       python3 scripts/check_doc_paths.py
run check_doc_style       python3 scripts/check_doc_style.py
run check_doc_style_self  python3 scripts/check_doc_style.py --selftest
run check_gptp_docs       python3 scripts/check_gptp_docs.py
run check_gptp_docs_sub   python3 scripts/check_gptp_docs.py --with-submodule
run check_submodule_docs  python3 scripts/check_submodule_docs.py
run gen_toc_anchors       python3 scripts/gen_toc.py --verify-anchors
run gen_toc_check         python3 scripts/gen_toc.py --check
run check_em_dash         "$PYH" scripts/check_em_dash.py --base "$BASE"
git status --porcelain >> "$O/summary.txt"; echo "status-end" >> "$O/summary.txt"
