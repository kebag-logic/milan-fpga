#!/bin/bash
# The final gates at a glance: the lane gates' and docs.yml's rc lines, the firmware shards' last line, the sweep's
# shard logs and completion, and the harness gate legs' finished groups (a log whose tail holds the testbench's
# SUMMARY). usage: gstatus.sh
T=$VALIDATION_STORAGE/665s2b-a683u
H=$(cat $T/final-head.txt)
date +%T
tr '\n' ' ' < $T/lane-logs-final2/summary.txt; echo
tr '\n' ' ' < $T/docs-$H/jobs.txt 2>/dev/null; echo
for k in 0 1 2 3; do echo -n "fw$k $(tail -n 1 $T/logs/fwshard-$k.log | cut -c1-12) | "; done; echo
for k in 0 1 2 3; do
    echo -n "sweep$k $(ls $T/sweep-final/shard-$k/logs/*.log 2>/dev/null | wc -l) logs $([ -f $T/sweep-final/shard-$k/complete.json ] && echo complete) | "
done; echo
for l in G-A8 G-A1; do
    n=0; for f in $T/builds/$l/results/*.log; do tail -c 20000 "$f" | grep -q 'SUMMARY ' && n=$((n+1)); done
    echo "$l $n finished, $(tail -n 1 $T/logs/$l.log | cut -c1-40)"
done
