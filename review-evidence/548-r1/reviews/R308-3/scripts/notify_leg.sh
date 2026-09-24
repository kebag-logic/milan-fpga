#!/bin/bash
# Build and run the milan_dp timed notification leg on an extracted candidate
# tree, positive and with the CTLR_DIAG tie mutated to a nonzero value.
# Usage: notify_leg.sh <extracted-tree> <packet-dir> <verilator-bin-dir>
set -u
tree=$1
pkt=$2
vbin=$3
dp="$tree/tb/verilator/milan_dp"
mk="$pkt/scripts/notify_probe.mk"
out="$pkt/receipts/notify"
mut="$pkt/scratch/mutants"
mkdir -p "$out" "$mut"
export PATH="$vbin:$PATH"
verilator --version > "$out/verilator_version.txt"

# mutant: the only change is the diagnostic tie, 0 -> the value the author used
src="$tree/hdl/milan/milan_datapath.sv"
tie="assign aecp_ctlr_diag = 32'd0;"
[ "$(grep -cF "$tie" "$src")" = 1 ] || { echo "tie not unique" >&2; exit 2; }
sed "s/assign aecp_ctlr_diag = 32'd0;/assign aecp_ctlr_diag = 32'h01001001;/" "$src" > "$mut/milan_datapath_ctlr_nonzero.sv"
diff "$src" "$mut/milan_datapath_ctlr_nonzero.sv" > "$out/mutant.diff"
sha256sum "$src" "$mut/milan_datapath_ctlr_nonzero.sv" > "$out/mutant_inputs.sha256"

cd "$dp" || exit 2
make -f Makefile -f "$mk" ltn_rom.hex ucode.hex gptp_ucode.hex > "$out/hex.log" 2>&1 || { echo "hex generation failed" >&2; exit 2; }
( make -f Makefile -f "$mk" notify-probe VERILATOR_JOBS=4 NOTIFY_MDIR=obj_notify \
    > "$out/build_positive.log" 2>&1; echo $? > "$out/build_positive.rc" ) &
( make -f Makefile -f "$mk" notify-probe VERILATOR_JOBS=4 NOTIFY_MDIR=obj_notify_mut \
    DP_SRC="$mut/milan_datapath_ctlr_nonzero.sv" \
    > "$out/build_mutant.log" 2>&1; echo $? > "$out/build_mutant.rc" ) &
wait
echo "build positive rc=$(cat "$out/build_positive.rc") mutant rc=$(cat "$out/build_mutant.rc")"
( ./obj_notify/Vmilan_dp_notify > "$out/run_positive.log" 2>&1; echo $? > "$out/run_positive.rc" ) &
( ./obj_notify_mut/Vmilan_dp_notify > "$out/run_mutant.log" 2>&1; echo $? > "$out/run_mutant.rc" ) &
wait
echo "run positive rc=$(cat "$out/run_positive.rc") mutant rc=$(cat "$out/run_mutant.rc")"
