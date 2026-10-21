#!/usr/bin/env bash
# usage: run_r679_2.sh <revision> <out dir>: R679-2's probe runner (the copy
# adapted to the lane's job limits and to the moved mutants.py anchor,
# probes/r679-2/adaptation.diff) on the lane at <revision>
S=<scratch>/r3
. $S/scripts/env.sh
rev=$1; out=$2
rm -rf "$out"; mkdir -p "$out"
sh $S/probes/r679-2/run_reviewer_probes.sh <lane> "$rev" "$out" > "$out/run_reviewer_probes.out" 2>&1
echo $? > "$out/run_reviewer_probes.rc"
echo done > "$out/DONE"
