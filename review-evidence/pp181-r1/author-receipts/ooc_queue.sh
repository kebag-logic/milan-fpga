#!/usr/bin/env bash
# queued OOC runs, each takes the exclusive lock in turn (ooc_run.sh)
S=<data>/tmp/pp181-a635
git -C <data>/lanes/pp181-cut rev-parse HEAD > $S/ooc/queue-head.txt
$S/ooc_run.sh $S/base-tree $S/ooc/base-8x8 8 8
$S/ooc_run.sh <data>/lanes/pp181-cut $S/ooc/head-1x1 1 1
$S/ooc_run.sh <data>/lanes/pp181-cut $S/ooc/head-8x8 8 8
echo DONE > $S/ooc/queue-done.txt
