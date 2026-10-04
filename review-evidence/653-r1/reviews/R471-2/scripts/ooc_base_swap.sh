#!/bin/bash
# OOC area of the BASE KL_crf_rx: swap the base bytes into the clone, run the
# same instrument, restore the head bytes (trap), and verify the blob.
. "$(dirname "$0")/env.sh"
F=hdl/ieee1722/crf/KL_crf_rx.sv
cd "$CLONE"
restore() { git -C "$CLONE" checkout -- "$F"; }
trap restore EXIT
git show $BASE_SHA:$F > "$F"
OOC_TMP="$SCR/ooc_tmp_base" OOC_SHAPE=configs/generated/endstation_ax7101_1x1_tdm8 syn/yosys/ooc.sh KL_crf_rx > "$REC/ooc_base.log" 2>&1
echo $? > "$REC/ooc_base.rc"
restore; trap - EXIT
echo "restored blob: $(git hash-object $F) expected: $(git rev-parse HEAD:$F)"
