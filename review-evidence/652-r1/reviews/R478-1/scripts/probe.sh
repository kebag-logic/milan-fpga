#!/bin/sh
# One disposable probe: a fresh worktree of the scratch head repo, one planted
# defect, then the named gate functions. Prints PROBE <name> rc=<rc>.
# Usage: probe.sh <packet> <name> <rel file> <old> <new> <fn> [<fn> ...]
P=$1; name=$2; file=$3; old=$4; new=$5; shift 5
W=$P/scratch/probe-$name
git -C "$P/scratch/head" worktree remove --force "$W" 2>/dev/null; rm -rf "$W"
git -C "$P/scratch/head" worktree add -q --detach "$W" HEAD
python3 "$P/scripts/plant.py" "$W/$file" "$old" "$new" || { echo "PROBE $name rc=PLANT-FAILED"; exit 3; }
(cd "$W" && PATH=$P/scratch/bin:$PATH timeout 1200 python3 "$P/scripts/run_focused.py" "$W" "$@")
rc=$?
echo "PROBE $name rc=$rc"
