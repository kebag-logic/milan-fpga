#!/usr/bin/env bash
# reproduce.sh: this review's probes at a16899b1, from a clean detached clone at C with its submodules.
# Each writes receipts/NAME.log and receipts/NAME.rc. The clone is only read; builds go under scratch/.
set -u
P=$REVIEWS/943-r871-2-packet
C=${C:-$REVIEWS/r871-2-943}
S=$P/scripts
# the declaring-outputs arm at 1x1/1if, its two groups (aecp-fanout's completed SET_STREAM_INFO, aecp-outputs)
$S/run_bg.sh budget-1x1-declaring python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 \
  --build-dir $P/scratch/b-1x1-decl --jobs 5 --variant declaring-outputs --groups aecp-fanout,aecp-outputs \
  --record-budget-findings --record-share-findings &
# the completion-unexecuted plant at 8x8/1if on the exact head
$S/run_bg.sh budget-8x8-unexecuted python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if \
  --build-dir $P/scratch/b-8x8-unexec --jobs 5 --variant declaring-outputs --mutation completion-unexecuted &
# every output row planted alone at 1x1, two interfaces (the campaign's arm); four interface/flag rows at 8x8, two
$S/run_bg.sh fw-plants-1x1-if2 python3 -I $S/plant_output_rows.py "$C" $P/scratch/fw-1x1-if2 endstation_ax7101_1x1_tdm8 2
$S/run_bg.sh fw-plants-8x8-if2 python3 -I $S/plant_output_rows.py "$C" $P/scratch/fw-8x8-if2 endstation_ax7101_8x8 2 \
  output-registering-failed-msrp-failure-valid output-listener-any-interface output-listener-on-interface-zero \
  output-listener-of-output-zero
wait
# grade the reproduced declaring leg alone (completeness refusals for the absent formal legs are expected)
(cd "$C" && . $S/env.sh && python3 -I tb/verilator/ctrl_service_budget/record_classes.py $P/scratch/b-1x1-decl/results)
