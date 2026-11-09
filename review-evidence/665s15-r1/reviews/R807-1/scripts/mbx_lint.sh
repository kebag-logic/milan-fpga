#!/bin/bash
# Verilator -Wall lint of the mailbox top on a generated variant directory. usage: mbx_lint.sh TREE VARIANT_DIR
T=$1 V=$2
VL=${VERILATOR:-$DATA/tools/pinned-verilator-5.050/verilator}
"$VL" --version
"$VL" --lint-only -Wall --top-module KL_mbx "$V/KL_mbx_pkg.sv" "$T/hdl/milan/mailbox/KL_mbx_ring.sv" "$T/hdl/milan/mailbox/KL_mbx_rx.sv" \
  "$T/hdl/milan/mailbox/KL_mbx_tx.sv" "$T/hdl/milan/mailbox/KL_mbx_evt.sv" "$V/KL_mbx.sv" 2>&1
echo "lint-rc=$?"
