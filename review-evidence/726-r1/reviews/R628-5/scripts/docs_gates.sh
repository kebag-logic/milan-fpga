#!/bin/bash
# Reviewer replay of the docs workflow gates relevant to the #726 diff.
# usage: docs_gates.sh <repo> <out.tsv>; each gate's rc is recorded.
repo=$1; out=$2
cd "$repo" || exit 2
export PYTHONDONTWRITEBYTECODE=1
# MDLOCK_SITE: site-packages holding the hash-locked cmarkgfm/html5lib
export PYTHONPATH=${MDLOCK_SITE:?set MDLOCK_SITE}
base=c6bd08c6f52632c6d33d834ce842ac3cf63f29cc
: > "$out"
run() { local log; log=$(mktemp); "$@" >"$log" 2>&1; rc=$?; printf '%s\t%s\t%s\n' "$rc" "$*" "$(tail -1 "$log" | cut -c1-160)" >> "$out"; rm -f "$log"; }
run python3 scripts/docs_check.py
run python3 scripts/check_em_dash.py --base "$base"
run python3 scripts/check_em_dash.py --selftest
run python3 scripts/check_doc_style.py
run python3 scripts/check_doc_style.py --selftest
run python3 docs/DOC_MAP.gen.py --check
run python3 scripts/check_solution_docs.py
run python3 scripts/check_rtl_source_lists.py
run python3 scripts/measure_naming.py --check
run python3 scripts/measure_naming.py --selftest
run python3 scripts/check_port_contracts.py
run python3 scripts/measure_fail_fast.py --check
run python3 scripts/check_todo_ownership.py
run python3 scripts/measure_test_evidence.py --check
run python3 scripts/measure_test_evidence.py --selftest
run python3 scripts/check_hygiene.py --check
run python3 scripts/check_sv_idiom.py
run python3 scripts/check_cpp_idiom.py
run python3 scripts/check_cpp_idiom.py --selftest
run python3 scripts/check_py_idiom.py
run python3 scripts/check_py_idiom.py --selftest
run python3 scripts/check_sh_idiom.py
run python3 scripts/ci_events.py --check
run python3 scripts/check_archive.py
run python3 scripts/gen_toc.py --verify-anchors
run python3 scripts/gen_toc.py --check
run python3 scripts/check_feature_status.py
run python3 scripts/check_wire_accountability.py --self-test
run python3 scripts/lint_rtl.py --check
