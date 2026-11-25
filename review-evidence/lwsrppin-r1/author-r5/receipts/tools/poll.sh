#!/bin/bash
# poll.sh SECONDS: wait up to SECONDS for the docs unit to end, stopping early when it does; then one status line.
o=/data-2/milan/tmp/lwsrppin-a834/r5/docs2; end=$(( $(date +%s) + $1 ))
while [ $(date +%s) -lt $end ] && [ ! -e $o/end ]; do sleep 15; done
echo "$(date +%H:%M) steps=$(wc -l < $o/run.log) last=$(tail -1 $o/run.log | cut -f1,2) end=$(cat $o/end 2>/dev/null || echo -)"
