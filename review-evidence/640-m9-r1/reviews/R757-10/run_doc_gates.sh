#!/bin/sh
# Usage: run_doc_gates.sh <python with tools/markdown/requirements.txt> <base>, from the repository root.
v=$1; base=$2
run() { n=$1; shift; o=$("$@" 2>&1); r=$?; echo "$n rc=$r : $(printf '%s\n' "$o" | tail -1 | cut -c1-200)"; }
run docs_check python3 scripts/docs_check.py
run em_dash "$v" scripts/check_em_dash.py --base "$base"
run doc_style python3 scripts/check_doc_style.py
run toc_anchors "$v" scripts/gen_toc.py --verify-anchors
run toc_check "$v" scripts/gen_toc.py --check
run doc_paths python3 scripts/check_doc_paths.py
run gptp_docs python3 scripts/check_gptp_docs.py
run solution_docs python3 scripts/check_solution_docs.py
run feature_status python3 scripts/check_feature_status.py
run diff_check git diff --check "$base" HEAD
run ci_scope_selftest python3 scripts/ci_scope.py --selftest
