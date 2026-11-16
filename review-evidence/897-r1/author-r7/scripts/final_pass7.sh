#!/bin/bash
# Lane 897 round 7's pass, once, at the final head (round 6's final_pass6.sh): a clean clone for the
# harness legs, the queue (gate_queue7.sh) and its dispatcher. usage: final_pass6.sh HEAD
set -u
H=$1 T=/data-2/milan/tmp/897-a776 S=/data-2/milan/tmp/897-a776/scripts/r4
test "$(git -C $LANES/897-aspath rev-parse HEAD)" = "$H" || { echo "worktree not at $H"; exit 4; }
test -z "$(git -C $LANES/897-aspath status --porcelain)" || { echo "worktree dirty"; exit 4; }
O=$T/r4/gates-out/final-${H:0:8}
mkdir -p $O $T/r4/logs
[ -d $T/r4/cl-final-${H:0:8} ] || bash $T/scripts/clone.sh $T/r4/cl-final-${H:0:8} $H > $T/r4/logs/cl-final-${H:0:8}.log 2>&1
test "$(git -C $T/r4/cl-final-${H:0:8} rev-parse HEAD)" = "$H" || exit 4
bash $S/gate_queue7.sh $H $O > $T/r4/logs/queue-final-${H:0:8}.txt
echo "$(date +%T) round 6 pass at $H: $(wc -l < $T/r4/logs/queue-final-${H:0:8}.txt) queued units" >> $T/r4/logs/final-pass.txt
cd $T && setsid nohup python3 -I $S/dispatch3.py 8 3 20 $T/r4/logs/queue-final-${H:0:8}.txt $T/r4/logs/dispatch-final-${H:0:8}.log > $T/r4/logs/dispatch-final-${H:0:8}.out 2>&1 < /dev/null &
echo "$(date +%T) dispatcher pid $!" >> $T/r4/logs/final-pass.txt
tail -2 $T/r4/logs/final-pass.txt
