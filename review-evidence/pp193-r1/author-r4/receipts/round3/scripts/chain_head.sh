#!/usr/bin/env bash
# head 65d39b0c: the processor gates in head-pp, then every campaign that
# builds the listener FSM in head-pp-c at --jobs 2 (srp_top first, for the
# README counts)
S=<scratch>/r3
bash $S/scripts/run_gates.sh $S/head-pp $S/rec/head-gates
bash $S/scripts/run_camps.sh $S/head-pp-c $S/rec/head-camps 2 srp_top d3 acmp notify dispatch aecp gsi ctr elab_mutants name_state name_wr
echo done > $S/rec/head-CHAIN.done
