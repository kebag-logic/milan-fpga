#!/usr/bin/env bash
# Run the docs.yml gates that read the files the #711 composition changes.
# Usage: run_docs_gates.sh <repo> <receipt-dir> <base-sha>
# Each gate's log and rc go to <receipt-dir>/docs-gates/<nn>.log; a summary to summary.tsv.
# act_ci.py --selftest is deliberately excluded (out of this review's authority).
set -u
repo=$1; out=$2/docs-gates; base=$3
mkdir -p "$out"; : > "$out/summary.tsv"
cd "$repo" || exit 2
n=0
gate() {
  n=$((n + 1)); local id; id=$(printf '%02d' "$n")
  ( "$@" ) > "$out/$id.log" 2>&1; local rc=$?
  printf '%s\t%s\t%s\n' "$id" "$rc" "$*" >> "$out/summary.tsv"
}
gate python3 scripts/docs_check.py
gate python3 scripts/docs_check.py --selftest
gate python3 scripts/check_em_dash.py --base "$base"
gate python3 scripts/check_em_dash.py --selftest
gate python3 scripts/check_doc_style.py
gate python3 scripts/check_doc_style.py --selftest
gate python3 docs/DOC_MAP.gen.py --check
gate python3 scripts/check_solution_docs.py
gate python3 docs/diagrams/submodule_boundaries.gen.py --check
gate python3 docs/diagrams/submodule_boundaries.gen.py --selftest
gate python3 scripts/check_submodule_docs.py
gate python3 scripts/check_submodule_docs.py --selftest
gate python3 scripts/check_diagram_pngs.py
gate python3 scripts/check_diagram_pngs.py --selftest
gate python3 scripts/check_nvm_capture.py
gate python3 scripts/measure_test_evidence.py --check
gate python3 scripts/check_hygiene.py --check
gate python3 scripts/check_cpp_idiom.py
gate python3 scripts/check_py_idiom.py
gate python3 scripts/ci_events.py --check
gate python3 scripts/ci_events.py --selftest
gate python3 scripts/check_doc_paths.py
gate python3 scripts/check_archive.py
gate python3 scripts/gen_toc.py --selftest
gate python3 scripts/gen_toc.py --verify-anchors
gate python3 scripts/gen_toc.py --check
gate git diff --check "$base" HEAD
cat "$out/summary.tsv"
