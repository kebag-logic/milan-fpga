#!/bin/bash
# The ledgered 8x8/2if arm A image of the lane's working firmware, in clone Q: sync, build, print its rom bytes.
# usage: qimage.sh TAG
set -eu
T=<scratch> L=<lane> Q=$T/Q B=$T/builds/QA8 TAG=$1
rsync -a --delete $L/sw/firmware/ctrl/ $Q/sw/firmware/ctrl/
. $T/scripts/env.sh
O=$T/qimg/$TAG; rm -rf $O; mkdir -p $O
<home>/litex-milan/venv/bin/python3 -B $Q/sw/firmware/ctrl/test/ctrl_srp_image.py --config $Q/configs/endstation_ax7101_8x8.yaml --interfaces 2 --with-aecp --layout split --output $O/image --ledgered-point 8x8-two-interfaces --flash-map $B/split-soc/flash-map --libc $B/runtime/libc.a --compiler-runtime $B/runtime/libcompiler_rt.a > $O/image.log 2>&1 || { echo "rc=$?"; tail -5 $O/image.log; }
grep -A1 '"rom"' $O/image.log | tail -1
NM=<home>/br-milan-rv32/host/bin/riscv32-buildroot-linux-gnu-nm
$NM -S $O/image/ctrl_app.elf | awk '$4 ~ /^(fan|fan_end|mbx_tx_begin|mbx_tx_commit|transmit|bin_take|ctrl_pool_free|same|reclaim|build_mrpdu)$/ {print $4, strtonum("0x"$2)}' | sort | tr '\n' ' '; echo
