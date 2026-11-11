#!/bin/sh
# Reproduces this round's checks at the 791 sync-merge head.
# Usage: probe.sh <clone at 77e1efa0, submodules initialized> <out dir> <python with migen+litex> <dir holding a Verilator 5.050 binary>
set -eu
clone=$1 out=$2 litexpy=$3 vdir=$4
head=77e1efa0f328f560656c049a923930509f196998
mkdir -p "$out/receipts" "$out/scratch/rd"
cd "$clone"
test "$(git rev-parse HEAD)" = "$head"
test -z "$(git status --porcelain)"
# (1) the merge's only hand change, two ways
git show --remerge-diff --format='%H%n%P' "$head" > "$out/remerge-diff.txt"
git merge-tree --write-tree --name-only "$head^1" "$head^2" > "$out/merge-tree.txt" || true
auto=$(head -1 "$out/merge-tree.txt")
git diff --stat "$auto" "$head^{tree}" > "$out/tree-compare.txt"
# (2)+(3) the ctrl-memory suite and the region-decode self-test, concurrently
PATH=$vdir:$PATH; export PATH
( "$litexpy" sw/litex/test_ctrl_memory.py > "$out/receipts/test_ctrl_memory.log" 2>&1; echo $? > "$out/receipts/test_ctrl_memory.rc" ) &
( "$litexpy" tb/verilator/ctrl_region_decode/run.py --self-test --build-dir "$out/scratch/rd" \
    > "$out/receipts/region_decode_selftest.log" 2>&1; echo $? > "$out/receipts/region_decode_selftest.rc" ) &
wait
# the Python idiom gate (hosted docs job, step gate_39) at the head and at each parent;
# the parents share the head's submodule gitlinks, so a detached checkout is enough
for c in "$head^1" "$head^2" "$head"; do
  git checkout -q --detach "$c"
  echo "== $(git rev-parse HEAD) test_ctrl_memory.py $(wc -l < sw/litex/test_ctrl_memory.py) lines"
  python3 -I scripts/check_py_idiom.py 2>&1 | tail -1 || true
done > "$out/receipts/py_idiom-per-commit.txt"
git checkout -q --detach "$head"
test "$(git write-tree)" = "$(git rev-parse "$head^{tree}")"
cat "$out/receipts/"*.rc
