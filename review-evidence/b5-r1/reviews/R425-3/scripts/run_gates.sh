#!/usr/bin/env bash
# Docs gates at the exact head.  Usage: run_gates.sh <repo> <python-with-pinned-markdown-lock> <base> <outdir>
set -u
repo=$1; py=$2; base=$3; out=$4; mkdir -p "$out"; cd "$repo" || exit 2
echo "head $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree})" > "$out/gates.txt"
run() { name=$1; shift; "$@" > "$out/$name.txt" 2>&1; rc=$?; echo "rc=$rc  $name: $*" | sed "s#$py#<pinned-python>#" >> "$out/gates.txt"; }
run docs_check          "$py" scripts/docs_check.py
run check_doc_style     "$py" scripts/check_doc_style.py
run gen_toc_check       "$py" scripts/gen_toc.py --check
run gen_toc_anchors     "$py" scripts/gen_toc.py --verify-anchors
run em_dash             "$py" scripts/check_em_dash.py --base "$base"
run em_dash_selftest    "$py" scripts/check_em_dash.py --selftest
run doc_paths           "$py" scripts/check_doc_paths.py
run ci_scope_selftest   python3 scripts/ci_scope.py --selftest
run baremetal_only      python3 scripts/check_baremetal_only.py --check
run feature_status      python3 scripts/check_feature_status.py --self-test
run diff_check_base     git diff --check "$base" HEAD
run diff_check_r2       git diff --check e29d12b1d5ee858eaf4684aaa8dc6647f6309857 HEAD
run status_after        git status --porcelain=v1 --untracked-files=all
cat "$out/gates.txt"
