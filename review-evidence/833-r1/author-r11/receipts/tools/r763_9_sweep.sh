#!/usr/bin/env bash
# R763-9's sweep.py, unchanged, from its manifest-checked copy, on one tree, one name filter per call.
# usage: r763_9_sweep.sh <tree> <filter> <receipt dir>
set -u
S=$VALIDATION_STORAGE/833-a726j
tree=$1; filter=$2; out=$3
mkdir -p "$out" "$S/sweep-scratch"
export TMPDIR=$S/tmp
grep SigIgn /proc/self/status > "$out/sweep-$filter.sigign"
cat /proc/loadavg > "$out/sweep-$filter.load"
python3 -I "$S/probes/833-r763-9/sweep.py" "$tree" "$S/sweep-scratch/$filter" 16 "$filter" > "$out/sweep-$filter.log" 2>&1
echo $? > "$out/sweep-$filter.rc"
cat /proc/loadavg >> "$out/sweep-$filter.load"
rm -rf "$S/sweep-scratch/$filter"
tail -1 "$out/sweep-$filter.log"
