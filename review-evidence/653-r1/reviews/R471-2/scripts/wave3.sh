#!/bin/bash
# Wave 3: the committed campaign driver (one process per mutant, each also
# re-running the clean control) and the Yosys OOC area at head, in the clone.
. "$(dirname "$0")/env.sh"
cd "$CLONE/tb/verilator/milan_dp"
for n in 1 2 3 4 5; do run "unbmut_$n" python3 unb_mutants.py $n; done
( cd "$CLONE" && OOC_TMP="$SCR/ooc_tmp_head" OOC_SHAPE=configs/generated/endstation_ax7101_1x1_tdm8 syn/yosys/ooc.sh KL_crf_rx > "$REC/ooc_head.log" 2>&1; echo $? > "$REC/ooc_head.rc" ) &
wait
