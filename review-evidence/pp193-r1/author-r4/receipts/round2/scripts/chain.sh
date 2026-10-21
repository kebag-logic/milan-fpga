#!/usr/bin/env bash
# usage: chain.sh <base|head>: the processor gates in <which>-pp, then every
# campaign that builds the listener FSM in <which>-pp-c at --jobs 2
S=<scratch>/r2
w=$1
bash $S/scripts/run_gates.sh $S/$w-pp $S/rec/$w-gates
bash $S/scripts/run_camps.sh $S/$w-pp-c $S/rec/$w-camps 2
echo done > $S/rec/$w-CHAIN.done
