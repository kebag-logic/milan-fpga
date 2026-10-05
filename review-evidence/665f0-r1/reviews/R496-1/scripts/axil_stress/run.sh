#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# run.sh - build and run axil_stress.cpp against a tree's mailbox RTL, both adapters.
# usage: run.sh <tree> <builddir> [verilator]
set -u
T=$(cd "$1" && pwd); B=$2; V=${3:-${VERILATOR:?set VERILATOR or pass it as the third argument}}
HERE=$(cd "$(dirname "$0")" && pwd)
R=$T/hdl/milan/mailbox
RTL="$R/KL_mbx_pkg.sv $R/KL_mbx_ring.sv $R/KL_mbx_rx.sv $R/KL_mbx_tx.sv $R/KL_mbx_evt.sv $R/KL_mbx.sv $R/KL_mbx_wb.sv $R/KL_mbx_axil.sv $T/tb/verilator/mbx/tb_mbx_top.sv"
mkdir -p "$B"
rc=0
for h in 1 0; do
    "$V" --cc --exe --build -j 4 --top-module tb_mbx_top -Wno-fatal -Wno-lint -Wno-style -GHOST_P=$h \
        --Mdir "$B/obj_$h" $RTL "$HERE/axil_stress.cpp" -o Vstress > "$B.build_$h.log" 2>&1 || { echo "build $h failed"; tail "$B.build_$h.log"; exit 2; }
    "$B/obj_$h/Vstress" $h || rc=1
done
exit $rc
