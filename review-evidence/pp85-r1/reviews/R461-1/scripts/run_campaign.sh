#!/bin/sh
# Usage: run_campaign.sh <label> <jobs> [--only a,b]
# Runs the head's tb/adp_engine/mutants.py from a pristine export of HEAD (never the clone's worktree).
. "$(dirname "$0")/env.sh"
set -u
label=$1; jobs=$2; shift 2
d="$SCRATCH/campaign-$label"; rm -rf "$d"; mkdir -p "$d/tree" "$d/out"
git -C "$CLONE" archive "$HEAD_SHA" hdl tb/common tb/adp_engine tb/pp_top | tar -x -C "$d/tree"
"$VERILATOR" --version > "$RCPT/campaign-$label.log"
python3 "$d/tree/tb/adp_engine/mutants.py" --output "$d/out" --jobs "$jobs" "$@" >> "$RCPT/campaign-$label.log" 2>&1
rc=$?; echo "$rc" > "$RCPT/campaign-$label.rc"; exit $rc
