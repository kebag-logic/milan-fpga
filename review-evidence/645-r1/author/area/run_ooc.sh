#!/bin/bash
# One Vivado process per configuration, all under the shared lock:
#   VIVADO_BIN=<Vivado 2026.1 bin> flock $VIVADO_LOCK ./run_ooc.sh
# Run from a scratch directory holding ooc_all.tcl, settle_base.sv, the three
# settle pieces (settle_piece.svh is milan_datapath.sv:6264-6311 verbatim, and
# the two option pieces are it with optB_settle.diff / optC_settle.diff
# applied), cmc_base.sv / servo_base.sv (the tree files), cmc_rc.sv /
# servo_ph.sv (the tree files with optC_KL_chan_map_capture.diff /
# optA_KL_mmcm_drp_servo.diff applied), cdc_pulse.sv and cdc_handshake.sv.
cd "$(dirname "$0")" || exit 99
export PATH="${VIVADO_BIN:?set VIVADO_BIN to the Vivado 2026.1 bin directory}:$PATH"
for t in settle_base settle_optB settle_optC cmc_base cmc_rc servo_base servo_ph; do
  ONLY=$t vivado -mode batch -source ooc_all.tcl -nojournal -log vivado_$t.log > vivado_$t.out 2>&1
  echo "$t rc=$?" >> ooc_rcs.txt
done
