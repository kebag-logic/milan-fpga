#!/bin/bash
# Lint-elaborate milan_datapath with the datapath harness's own sources and flags at three shapes, concurrently:
# the split 4x4 (CTRL_SPLIT_P=1, N_STREAMS=4), the tracked all-fabric 4x4 and the split 1x1 as controls.
# usage: dp_lint.sh CLONE TREE PACKET   (the source list is read from CLONE, whose git the derivation needs;
#        the lint runs in TREE, a disposable copy of it)
CLONE=$1; TREE=$2; R=$3/receipts
export PATH=${PINNED_VERILATOR_DIR:?set PINNED_VERILATOR_DIR to the pinned Verilator 5.050 directory}:$PATH
PV=$(mktemp); printf 'pv: ; @echo $(SRCS)\npf: ; @echo $(DP_VFLAGS)\n' > "$PV"
SRCS=$(make -s -C "$CLONE/tb/verilator/milan_dp" -f Makefile -f "$PV" pv)
FL=$(make -s -C "$CLONE/tb/verilator/milan_dp" -f Makefile -f "$PV" pf | sed -e 's/--cc --exe --build -j 0//' -e 's/-CFLAGS -std=c++17 -O2 -Wall -Wextra//'); rm -f "$PV"
cd "$TREE/tb/verilator/milan_dp" || exit 2
G=../../../configs/generated
lint() { local name=$1; shift; ( verilator --lint-only "$@" $FL $SRCS > "$R/lint-$name.log" 2>&1; echo $? > "$R/lint-$name.rc" ) & }
lint split4x4 +incdir+$G/endstation_arty_split_4x4 -GN_STREAMS=4 -GCTRL_SPLIT_P=1
lint fabric4x4 +incdir+$G/endstation_arty_4x4 -GN_STREAMS=4
lint split1x1 +incdir+$G/endstation_arty_split -GN_STREAMS=1 -GCTRL_SPLIT_P=1
wait
for n in split4x4 fabric4x4 split1x1; do echo "$n rc=$(cat $R/lint-$n.rc) errors=$(grep -c '^%Error' $R/lint-$n.log) warnings=$(grep -c '^%Warning' $R/lint-$n.log)"; done | tee "$R/lint-summary.txt"
