#!/bin/sh
# Focused gates for the R250-4 delta review.
# Usage: run_gates.sh <clone> <export-with-submodules> <plain-export> <receipts>
# Git-mode gates run in the clone (read-only checks). test_declarations runs in
# a git-archive export of the same head with the submodules linked in; the
# no-git docs inventory runs in a plain git-archive export (no .git, no
# submodule content, no build products).
clone=$1; export=$2; plain=$3; out=$4
mkdir -p "$out"
run() {
    name=$1; dir=$2; shift 2
    start=$(date +%s)
    (cd "$dir" && "$@") > "$out/gate-$name.log" 2>&1
    rc=$?
    echo "$name rc=$rc seconds=$(( $(date +%s) - start )) cmd=$*" | tee -a "$out/gates-summary.txt"
}
: > "$out/gates-summary.txt"
run test_declarations "$export" python3 -B sw/builder/test_declarations.py
run py_idiom "$clone" python3 -B scripts/check_py_idiom.py
run docs_check_git "$clone" python3 -B scripts/docs_check.py
run docs_check_nogit "$plain" python3 -B scripts/docs_check.py
run doc_style "$clone" python3 -B scripts/check_doc_style.py
run toc_check "$clone" python3 -B scripts/gen_toc.py --check
run toc_anchors "$clone" python3 -B scripts/gen_toc.py --verify-anchors
run doc_paths "$clone" python3 -B scripts/check_doc_paths.py
run em_dash_pr_base "$clone" python3 -B scripts/check_em_dash.py --base 864b36f5e9450ef64f75ca3f0d68c44330e447d7
run test_evidence "$clone" python3 -B scripts/measure_test_evidence.py --check
run diff_check_delta "$clone" git diff --check e122f3302cf8a8e89de960233a8638b9dd1387dc c6c65e803f9eb270a11dfd65fda5814fb0b0ea55
run stale_text "$clone" sh -c '! git grep -n "let it be pruned\|what both boards ship\|RX_ADDRESS_FILTERS\|stream_dmac_alloc" c6c65e803f9eb270a11dfd65fda5814fb0b0ea55'
