#!/bin/bash
# Keep an earlier leg of this round: its build.json, label, results.json.gz and table. usage: keep_old.sh NAME LABEL
set -u
T=$VALIDATION_STORAGE/665s2b-a683o
O=$MANAGEMENT/2026-09-23/665s2b-a683o/receipts/experiments/$1
mkdir -p "$O"
scrub() { sed -e "s#$T#<scratch>#g" -e "s#$WORKSPACE_HOME#\$HOME#g" -e "s#$VALIDATION_TOOLS#<tools>#g"; }
scrub < "$T/old/$1/build.json" > "$O/build.json"
printf '%s\n' "$2" > "$O/label.txt"
scrub < "$T/old/$1/results/results.json" | gzip -n > "$O/results.json.gz"
scrub < "$T/old/$1/results/table.md" > "$O/table.md"
