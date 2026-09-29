#!/usr/bin/env bash
# Run the round-3 docs gate set at the clone's HEAD, foreground, one
# receipt per gate. Usage: run_gates.sh <clone> <pinned-md-python> <receipt-dir>
set -u
clone=$1; mdpy=$2; out=$3
cd "$clone" || exit 2
{ echo "head $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree}) status-lines $(git status --porcelain | wc -l)"
  echo "pinned env:"; "$mdpy" -m pip freeze
  echo "requirements pins:"; grep -E '^[a-z0-9_.-]+==' tools/markdown/requirements.txt; } > "$out/env.txt" 2>&1
run() { name=$1; shift
  "$@" > "$out/$name.txt" 2>&1; rc=$?
  echo "$name rc=$rc :: $(tail -n 1 "$out/$name.txt")" >> "$out/summary.txt"; }
: > "$out/summary.txt"
run docs_check           "$mdpy" scripts/docs_check.py
run check_doc_style      "$mdpy" scripts/check_doc_style.py
run gen_toc_check        "$mdpy" scripts/gen_toc.py --check
run check_em_dash        "$mdpy" scripts/check_em_dash.py --base 13eda870d1a6cf3f946fc228a98862366b08d102
run check_em_dash_r3     "$mdpy" scripts/check_em_dash.py --base d76763733e088cd21bbdd587927c8cf2f26cc8b3
run check_doc_paths      "$mdpy" scripts/check_doc_paths.py
run ci_scope_selftest    python3 scripts/ci_scope.py --selftest
run baremetal_only       python3 scripts/check_baremetal_only.py --check
run feature_status       python3 scripts/check_feature_status.py --self-test
run diff_check_base      git diff --check 13eda870d1a6cf3f946fc228a98862366b08d102 HEAD
run diff_check_r3        git diff --check d76763733e088cd21bbdd587927c8cf2f26cc8b3 HEAD
echo "post-run status-lines $(git status --porcelain | wc -l)" >> "$out/summary.txt"
