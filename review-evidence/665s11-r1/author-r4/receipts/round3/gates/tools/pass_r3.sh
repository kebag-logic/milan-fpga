#!/bin/bash
# pass_r3.sh <head>: round 3's gates (the ruling's list) on fresh clean clones of <head>: the firmware lane (the
# host arms and every planted defect, the AECP driver, git diff --check), the REBOOT simulation's self-test, and
# every run: step of docs.yml
set -u
H=$1; S=<scratch>; T=$S/gates/tools; R=$S/gates/pass3
mkdir -p $R/phase; echo "$(date +%T) start $H" >> $R/phase/log
$T/lane_gates.sh $H $R r3fw > $R/phase/r3fw.out 2>&1 & a=$!
$T/lane_gates.sh $H $R r3cpu > $R/phase/r3cpu.out 2>&1 & b=$!
$T/drive.sh $H $R D docs:wire-accountability docs:docs-check-no-git docs:docs-gates-0 docs:docs-gates-1 docs:docs-gates-2 docs:docs-check > $R/phase/D.out 2>&1 & c=$!
wait $a $b $c
echo "ALL DONE $(date +%T)" >> $R/phase/log
