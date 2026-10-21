#!/usr/bin/env bash
# round-4 head chain: the processor gates in final-pp beside the order probes
# (one Verilator build each at a time), then the srp_top campaign at --jobs 2
# in final-pp-c, each in its own clean clone of the head
S=<scratch>/r4
h=$(cat $S/head.sha)
bash $S/scripts/order_probes.sh $S/final-pp "$h" $S/rec/order > $S/rec/order.out 2>&1 &
bash $S/scripts/run_gates.sh $S/final-pp $S/rec/gates
wait
bash $S/scripts/run_camps.sh $S/final-pp-c $S/rec/camps 2 srp_top
echo done > $S/rec/chain.done
