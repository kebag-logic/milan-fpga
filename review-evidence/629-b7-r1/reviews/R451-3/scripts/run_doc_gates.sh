#!/bin/sh
# Run the lane's documentation gates at the checked-out head; one log and rc line per gate.
# Usage: run_doc_gates.sh <repo> <python-with-pinned-markdown-env> <out-dir>
repo=$1; py=$2; out=$3
mkdir -p "$out"; : > "$out/rc.txt"
cd "$repo" || exit 2
echo "head $(git rev-parse HEAD)" >> "$out/rc.txt"
run() {
  name=$1; shift
  "$@" > "$out/$name.log" 2>&1
  echo "$name rc=$?" >> "$out/rc.txt"
}
run docs_check "$py" scripts/docs_check.py
run check_doc_style "$py" scripts/check_doc_style.py
run gen_toc_check "$py" scripts/gen_toc.py --check
run gen_toc_verify_anchors "$py" scripts/gen_toc.py --verify-anchors
run check_em_dash_base_bbf704ec "$py" scripts/check_em_dash.py --base bbf704ecc3ef2e9cdd4cfdb72ec085e7428d1352
run check_doc_paths "$py" scripts/check_doc_paths.py
run ci_scope_selftest "$py" scripts/ci_scope.py --selftest
run check_baremetal_only_check "$py" scripts/check_baremetal_only.py --check
run check_baremetal_only_selftest "$py" scripts/check_baremetal_only.py --selftest
run check_feature_status_selftest "$py" scripts/check_feature_status.py --self-test
run git_diff_check_base git diff --check bbf704ecc3ef2e9cdd4cfdb72ec085e7428d1352 HEAD
run git_diff_check_round3 git diff --check f4eb39d3fddbbd9e2de1947750cc1b482baff53d HEAD
cat "$out/rc.txt"
