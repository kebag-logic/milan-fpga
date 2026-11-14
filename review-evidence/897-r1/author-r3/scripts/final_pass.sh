#!/bin/bash
# Lane 897 round 3's full pass, once, at the final head: a clean clone for the harness legs, the queue (gate_queue3.sh),
# its dispatcher (dispatch3.py: a range cpu_ranges.py picks, else the session pool while it is idle enough and this lane
# holds fewer than POOL units there), and the sweep's four shards, each on its own booked range (launch_sweep3.sh).
# usage: final_pass.sh HEAD
set -u
H=$1 T=/data-2/milan/tmp/897-a776 S=/data-2/milan/tmp/897-a776/scripts/r3
test "$(git -C $LANES/897-aspath rev-parse HEAD)" = "$H" || { echo "worktree not at $H"; exit 4; }
test -z "$(git -C $LANES/897-aspath status --porcelain)" || { echo "worktree dirty"; exit 4; }
O=$T/r3/gates-out/final-${H:0:8}
mkdir -p $O $T/r3/logs
[ -d $T/r3/cl-final-${H:0:8} ] || bash $T/scripts/clone.sh $T/r3/cl-final-${H:0:8} $H > $T/r3/logs/cl-final.log 2>&1
test "$(git -C $T/r3/cl-final-${H:0:8} rev-parse HEAD)" = "$H" || exit 4
bash $S/gate_queue3.sh $H $O > $T/r3/logs/queue-final-${H:0:8}.txt
echo "$(date +%T) final pass at $H: $(wc -l < $T/r3/logs/queue-final-${H:0:8}.txt) queued units" >> $T/r3/logs/final-pass.txt
cd $T && nohup python3 -I $S/dispatch3.py 8 3 20 $T/r3/logs/queue-final-${H:0:8}.txt $T/r3/logs/dispatch-final-${H:0:8}.log > $T/r3/logs/dispatch-final.out 2>&1 &
echo "$(date +%T) dispatcher pid $!" >> $T/r3/logs/final-pass.txt
nohup bash $S/launch_sweep3.sh $H > $T/r3/logs/launch-sweep.out 2>&1 &
echo "$(date +%T) sweep launcher pid $!" >> $T/r3/logs/final-pass.txt
cat $T/r3/logs/final-pass.txt
