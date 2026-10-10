#!/bin/sh
# Reviewer gate runs on private copies of the tree at the reviewed head.
# Usage: gates.sh <repo> <packet>   (needs verilator 5.050 on PATH)
# Each gate writes receipts/<name>.log and receipts/<name>.rc.
set -u
REPO=$1
PKT=$2
W=$PKT/scratch/gates
R=$PKT/receipts
rm -rf "$W"
mkdir -p "$W"
# one private copy of the working tree, without .git
(cd "$REPO" && tar --exclude=.git --exclude=obj_dir -cf - .) | (mkdir -p "$W/tree" && cd "$W/tree" && tar -xf -)
cp -a "$W/tree" "$W/tree_gp"
run() {
  name=$1; shift
  ( "$@" > "$R/$name.log" 2>&1; echo $? > "$R/$name.rc" ) &
}
run gp_contract make -C "$W/tree_gp/gptp-processor" contract
run gp_lint make -C "$W/tree_gp/gptp-processor" lint
run gp_engine_tb make -C "$W/tree/gptp-processor/tb/verilator/engine"
run parent_lint sh -c "cd '$W/tree' && python3 scripts/lint_rtl.py --check"
wait
