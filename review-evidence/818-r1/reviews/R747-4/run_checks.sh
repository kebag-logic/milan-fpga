#!/bin/sh
# Re-run the R747-4 delta checks from a clean checkout of the exact head.
# Usage: run_checks.sh <checkout> <python-with-pinned-renderer> <receipt-dir>
# The python must carry tools/markdown/requirements.txt (installed --require-hashes).
set -u
C=$1; V=$2; R=$3
mkdir -p "$R"
cd "$C" || exit 2
test "$(git rev-parse HEAD)" = 81f78a81e1271185174f9c5dbbcc8469b5dab5b4 || { echo "wrong head"; exit 2; }
run() { n=$1; shift; ( "$@" >"$R/$n.log" 2>&1; echo $? >"$R/$n.rc" ) & }
run doc_style       "$V" scripts/check_doc_style.py
run toc_check       "$V" scripts/gen_toc.py --check
run toc_anchors     "$V" scripts/gen_toc.py --verify-anchors
run docs_check      "$V" scripts/docs_check.py
run doc_paths       "$V" scripts/check_doc_paths.py
run em_dash         "$V" scripts/check_em_dash.py --base 17fd6f73
run em_dash_srcbase "$V" scripts/check_em_dash.py --base 1e80128f
run check_baseline  "$V" syn/ooc/pp_resource_gate.py check-baseline
wait
echo "merge-tree $(git merge-tree --write-tree 02ca829a 50e5d08d) parent-tree $(git rev-parse 17fd6f73^{tree})" >"$R/merge_tree.txt"
git grep -n 'gate refuses' >"$R/grep_gate_refuses.txt"
git grep -n '0\.408' >"$R/grep_0408.txt"
for f in "$R"/*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f")"; done
