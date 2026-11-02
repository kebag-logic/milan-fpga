#!/bin/sh
# Run every docs-workflow job on its own fresh clone of the lane head, three chains
# at a time, through round 2's runner. Usage: run_all_gates.sh <lane> <scratch> <logs>
L=$1; S=$2; O=$3
R=$MANAGEMENT/2026-09-23/797-a711b/tools/run_docs_workflow.py
PY=/tmp/797-a711-wd/bin/python3
HEAD=$(git -C "$L" rev-parse HEAD)
rm -rf "$S"; mkdir -p "$S" "$O"
for j in wire docs0 docs1 docs2 nogit nogit-export; do
  git clone -q --no-hardlinks "$L" "$S/$j" && git -C "$S/$j" checkout -q "$HEAD" || exit 2
done
run() { # <clone> <export> <job>
  GATE_SCRATCH="$S/scratch-$3" GATE_HOME=/tmp/797-a711-home GATE_VENV=/tmp/797-a711-wd \
    "$PY" -B "$R" "$S/$1" "$S/$2" "$O" "$3" > "$O/$3.runner.txt" 2>&1
  echo $? > "$O/$3.runner.rc"
}
( run docs1 nogit-export docs-gates-1 ) &
( run wire nogit-export wire-accountability; run nogit nogit-export docs-check-no-git; run docs2 nogit-export docs-gates-2 ) &
( run docs0 nogit-export docs-gates-0 ) &
wait
for j in wire docs0 docs1 docs2; do
  echo "$j $(git -C "$S/$j" rev-parse HEAD) $(git -C "$S/$j" status --short | wc -l)"
done > "$O/clones_after.txt"
echo ALL_DONE > "$O/ALL_DONE"
