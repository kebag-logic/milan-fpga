#!/usr/bin/env bash
# head 57fb7dd2, runner 1: the processor gates in head-pp, then the first half
# of the campaigns in head-pp-c at --jobs 2
S=<scratch>/r2
bash $S/scripts/run_gates.sh $S/head-pp $S/rec/head-gates
bash $S/scripts/run_camps.sh $S/head-pp-c $S/rec/head-camps 2 srp_top acmp notify d3 aecp
echo done > $S/rec/head-H1.done
