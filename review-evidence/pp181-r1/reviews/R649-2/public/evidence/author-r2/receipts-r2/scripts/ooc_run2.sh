#!/usr/bin/env bash
# usage: ooc_run.sh <tree> <outdir> <n_in> <n_out>   (exclusive Vivado lock)
tree=$1; out=$2; ni=$3; no=$4
mkdir -p "$out"; cd "$out" || exit 9
. <home>/Xilinx/2026.1/Vivado/settings64.sh >/dev/null 2>&1 || true
t0=$SECONDS
flock -x $VIVADO_LOCK <home>/Xilinx/2026.1/Vivado/bin/vivado -mode batch -nojournal -log ooc.log \
  -source <data>/tmp/pp181-a635/ooc_cone2.tcl -tclargs "$tree" "$ni" "$no" > vivado.out 2>&1
echo "rc=$? ($((SECONDS - t0))s)" > rc.txt
