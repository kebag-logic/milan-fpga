#!/usr/bin/env bash
# R763-10's sweep.py, unchanged, from its manifest-checked copy, on the head clone, one name filter per chunk.
set -u
S=$VALIDATION_STORAGE/833-a726k; O=$MANAGEMENT/2026-09-23/833-a726k/receipts/final/sweep
mkdir -p "$O" "$S/sweep-scratch"
export TMPDIR=$S/tmp
for filter in r2- r3- r4- r5- r6- r7- r8-; do
  grep SigIgn /proc/self/status > "$O/sweep-$filter.sigign"
  { date +%T; cat /proc/loadavg; } > "$O/sweep-$filter.load"
  python3 -I "$S/probes/833-r763-10/scripts/sweep.py" "$S/wt-head" "$S/sweep-scratch/$filter" 10 "$filter" > "$O/sweep-$filter.log" 2>&1
  echo $? > "$O/sweep-$filter.rc"
  { date +%T; cat /proc/loadavg; } >> "$O/sweep-$filter.load"
  rm -rf "$S/sweep-scratch/$filter"
done
cat "$O"/sweep-r*-.log > "$S/sweep-full.log"
python3 -I "$S/probes/833-r763-10/scripts/classify10.py" "$S/sweep-full.log" > "$O/classified10.txt" 2>&1; echo $? > "$O/classified10.rc"
echo done > "$S/sweep.DONE"
