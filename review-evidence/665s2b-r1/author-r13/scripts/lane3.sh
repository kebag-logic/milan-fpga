#!/bin/bash
# After lane 2: the labelled 8x8/1if scratch point, the backlog rows, for section 14's S column.
T=$VALIDATION_STORAGE/665s2b-a683p; S=$MANAGEMENT/2026-09-23/665s2b-a683p/scripts
until grep -q done $T/logs/queue-2.txt 2>/dev/null; do sleep 30; done
$S/queue.sh 3 "P81-A8:CP:8x8-1if:backlog,backlog-adp,backlog-adp-refill,backlog-owed"
