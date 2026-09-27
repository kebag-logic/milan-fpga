#!/usr/bin/env bash
# Run the round's documentation gates at the checked-out head.
# Usage: run_doc_gates.sh <repo> <python-with-markdown-lock> <out-dir>
set -u
repo=$1; py=$2; out=$3
base=2a2a7bb655e528edc3087c88033cd3a47546feb4
mkdir -p "$out"
cd "$repo" || exit 2
run() {
  name=$1; shift
  { echo "\$ $*"; timeout 1800 "$@"; echo "rc=$?"; } > "$out/$name.txt" 2>&1
  tail -1 "$out/$name.txt" | sed "s/^/$name /"
}
echo "head $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')"
run docs_check        "$py" scripts/docs_check.py
run check_doc_style   "$py" scripts/check_doc_style.py
run gen_toc_check     "$py" scripts/gen_toc.py --check
run check_em_dash     "$py" scripts/check_em_dash.py --base "$base"
run check_doc_paths   "$py" scripts/check_doc_paths.py
run ci_scope_selftest "$py" scripts/ci_scope.py --selftest
run baremetal_only    "$py" scripts/check_baremetal_only.py --check
run diff_check        git diff --check "$base" HEAD
