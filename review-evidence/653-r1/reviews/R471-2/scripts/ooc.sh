#!/bin/bash
# OOC area of KL_crf_rx (Yosys, AX 1x1 TDM8 shape) at head and with the base engine.
. "$(dirname "$0")/env.sh"
for c in ooc_head ooc_base; do
  ( cd "$SCR/$c" && OOC_SHAPE=configs/generated/endstation_ax7101_1x1_tdm8 syn/yosys/ooc.sh KL_crf_rx ) > "$REC/$c.log" 2>&1; echo $? > "$REC/$c.rc"
done
