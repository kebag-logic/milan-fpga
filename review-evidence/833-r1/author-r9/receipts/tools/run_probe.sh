#!/usr/bin/env bash
# Run one reviewer probe at the head snapshot; its log and rc go to receipts/final/<name>.{log,rc}.
# usage: run_probe.sh <name> <command...>   (cwd: the head snapshot)
set -u
name=$1; shift
out=$MANAGEMENT/2026-09-23/833-a726i/receipts/final
export TMPDIR=$VALIDATION_STORAGE/833-a726i/tmp PYTHONDONTWRITEBYTECODE=1
cd $VALIDATION_STORAGE/833-a726i/wt-head || exit 2
cat /proc/loadavg > "$out/$name.load"
"$@" > "$out/$name.log" 2>&1
rc=$?
echo $rc > "$out/$name.rc"
cat /proc/loadavg >> "$out/$name.load"
echo "$name rc $rc: $(tail -n 2 "$out/$name.log" | cut -c1-300 | tr '\n' ' ')"
