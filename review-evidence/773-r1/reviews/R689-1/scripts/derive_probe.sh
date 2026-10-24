#!/bin/bash
# Elaborate milan_datapath (lint-only) at one shape in a probe tree whose
# packetizer, CRF talker and datapath carry $info prints of the #773 terms.
# The tree is prepared by derive_probe_insert.py. VERILATOR names a Verilator 5.050.
# usage: derive_probe.sh <probe-tree> <label> <shape-incdir> <-G flags...>
T=$1; LBL=$2; SH=$3; shift 3
V=${VERILATOR:-verilator}
cd "$T/tb/verilator/milan_dp" || exit 2
SRCS=$(make -s --no-print-directory print-srcs)
VF=$(make -s --no-print-directory print-dp-vflags | sed -e 's/--cc --exe --build -j 0//' -e 's/-CFLAGS "[^"]*"//')
eval "$V --lint-only +incdir+../../../configs/generated/$SH $VF -GMILAN_CLK_FREQ_HZ=50000000 $* $SRCS" 2>&1 | grep -E "PROBE|%Error" | sed "s/^/[$LBL] /"
