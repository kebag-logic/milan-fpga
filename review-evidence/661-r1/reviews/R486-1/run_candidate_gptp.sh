#!/bin/bash
# Build the disposable candidate (reviewed head merged with live dev) as a
# detached worktree with its pinned submodules as worktrees, then run the
# physical gPTP integration exactly as tb/verilator/milan_dp_gptp/Makefile does.
# Usage: run_candidate_gptp.sh <clone> <worktree dir> <log> <head> <dev>
# Needs the pinned Verilator first on PATH (VERILATOR exported).
set -u
clone=$1; wt=$2; log=$3; head=$4; dev=$5
tree=$(git -C "$clone" merge-tree --write-tree "$head" "$dev") || { echo "merge conflicts"; exit 2; }
commit=$(git -C "$clone" commit-tree "$tree" -p "$head" -p "$dev" -m "disposable candidate")
echo "candidate tree $tree commit $commit"
git -C "$clone" worktree add -q --detach "$wt" "$commit"
for sm in protocol-processor gptp-processor third_party/verilog-axis; do
  git -C "$clone/$sm" worktree add -q --detach "$wt/$sm" "$(git -C "$wt" rev-parse HEAD:$sm)"
done
cd "$wt" && make -C tb/verilator/milan_dp_gptp VERILATOR_JOBS=4 > "$log" 2>&1
rc=$?; echo "rc $rc"; exit $rc
