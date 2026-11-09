#!/bin/sh
# Reproduce the composition checks of this round on a clean clone at the merge candidate.
# Usage: composition_check.sh <repo-dir> <python-with-html5lib-cmarkgfm-wavedrom-pyyaml> <out-dir>
set -u
REPO=$1; PY=$2; OUT=$3
DEV=ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36
SRC=06c89f1d48c73ec1977791f2a2c4f99579ae4853
mkdir -p "$OUT"; cd "$REPO" || exit 2
MB=$(git merge-base $DEV $SRC)
git diff --name-only $MB $DEV | sort > "$OUT/dev_files.txt"
git diff --name-only $MB $SRC | sort > "$OUT/src_files.txt"
comm -12 "$OUT/dev_files.txt" "$OUT/src_files.txt" > "$OUT/overlap_files.txt"
echo "merge-tree=$(git merge-tree --write-tree $DEV $SRC) head-tree=$(git rev-parse HEAD^{tree})" > "$OUT/merge_tree.txt"
run() { n=$1; shift; "$@" > "$OUT/$n.log" 2>&1; echo $? > "$OUT/$n.rc"; }
run docs_inventory_check $PY scripts/docs_inventory.py --check &
run gen_register_reference_check $PY scripts/gen_register_reference.py --check &
run gen_register_reference_selftest $PY scripts/gen_register_reference.py --selftest &
run docs_check $PY scripts/docs_check.py &
run gen_toc_anchors $PY scripts/gen_toc.py --verify-anchors &
run gen_toc_check $PY scripts/gen_toc.py --check &
run em_dash_vs_dev $PY scripts/check_em_dash.py --base $DEV &
run em_dash_vs_source $PY scripts/check_em_dash.py --base $SRC &
run doc_style $PY scripts/check_doc_style.py &
run ci_events_check $PY scripts/ci_events.py --check &
run ci_events_selftest $PY scripts/ci_events.py --selftest &
wait
for f in "$OUT"/*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f")"; done
