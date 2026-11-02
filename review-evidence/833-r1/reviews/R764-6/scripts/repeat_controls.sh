#!/bin/bash
# Repeat owner controls unmutated in parallel (review probe).
# Usage: repeat_controls.sh <repo> <jobs> <control>:<count> ...
repo=$1 jobs=$2; shift 2
for spec in "$@"; do c=${spec%%:*}; n=${spec##*:}; for i in $(seq "$n"); do echo "$c $i"; done; done |
  xargs -P "$jobs" -L1 bash -c 'out=$(cd "$0" && python3 -B scripts/test_suite_cancellation.py --control "$1" 2>&1); rc=$?; echo "$1 #$2 rc=$rc $(echo "$out" | tail -1 | cut -c1-200)"' "$repo"
