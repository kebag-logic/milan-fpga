#!/bin/bash
# pass_r4.sh <head>: round 4's gates (the ruling's list) on fresh clean clones of <head>: the platform host tests
# with every planted defect, git diff --check, and every run: step of docs.yml
set -u
H=$1; S=<scratch>; T=$S/gates/tools; R=$S/gates/pass4
mkdir -p $R/phase; echo "$(date +%T) start $H" >> $R/phase/log
$T/lane_gates.sh $H $R r4fw > $R/phase/r4fw.out 2>&1 & a=$!
$T/drive.sh $H $R D docs:wire-accountability docs:docs-check-no-git docs:docs-gates-0 docs:docs-gates-1 docs:docs-gates-2 docs:docs-check > $R/phase/D.out 2>&1 & c=$!
wait $a $c
echo "ALL DONE $(date +%T)" >> $R/phase/log
