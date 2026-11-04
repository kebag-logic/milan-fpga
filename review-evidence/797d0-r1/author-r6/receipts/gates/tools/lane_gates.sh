#!/usr/bin/env bash
# lane_gates.sh <head sha>: the lane gates of round 6, one log and one rc per gate, never piped, on a clean clone of the head.
set -u
H=$1; L=$LANES/797-d0-audit; S=$VALIDATION_STORAGE/797-a706f/gates; W=$S/lane-wt; G=$S/lane-logs
mkdir -p "$G"
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
test -z "$(git status --porcelain)" || exit 5
# origin/dev as the lane fetched it from GitHub; the merge base is read in the clone and in the lane.
git fetch -q "$L" +refs/remotes/origin/dev:refs/remotes/origin/dev || exit 6
export PATH=/usr/local/bin:/usr/bin:/bin PYTHONHASHSEED=0
run() { id=$1; shift; { echo "# head $H gate $id: $*"; bash -c "$*"; } > "$G/$id.log" 2>&1; rc=$?; echo $rc > "$G/$id.rc"; echo "$id rc=$rc"; }
run ls_remote_dev "git ls-remote https://github.com/kebag-logic/milan-fpga.git refs/heads/dev && git rev-parse origin/dev"
run merge_base_all "git merge-base --all origin/dev HEAD && test \$(git merge-base --all origin/dev HEAD | wc -l) -eq 1"
run merge_base_all_lane "git -C $L merge-base --all origin/dev $H && test \$(git -C $L merge-base --all origin/dev $H | wc -l) -eq 1"
run diffcheck "git diff --check \$(git merge-base origin/dev HEAD) HEAD"
run inventory_check "python3 scripts/docs_inventory.py --check"
run inventory_selftest "python3 scripts/docs_inventory.py --selftest"
run pp_srcs "python3 scripts/pp_srcs.py --check --selftest"
run pp_srcs_check "python3 scripts/pp_srcs.py --check"
git status --porcelain > "$G/tree-after.txt"
echo done > "$G/DONE"
