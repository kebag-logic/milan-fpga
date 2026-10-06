#!/bin/sh
# run_diff_probe.sh TREE OUT [IF2]
# Builds diff_probe.cpp against the mailbox RTL of an extracted head tree TREE
# (tb_mbx_top, Wishbone host) and the host model, into OUT, and runs it.
# With IF2=1 the contract is the two-interface variant the generator writes.
# VERILATOR must name the pinned Verilator 5.050.
set -eu
TREE=$(cd "$1" && pwd)
OUT=$2
IF2=${3:-0}
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$OUT"
OUT=$(cd "$OUT" && pwd)
RTL_DIR=$TREE/hdl/milan/mailbox
MBX=$TREE/tb/verilator/mbx
FW=$TREE/sw/firmware/ctrl
INC=$FW/mbx
PKG=$RTL_DIR/KL_mbx_pkg.sv
TOPSV=$RTL_DIR/KL_mbx.sv
if [ "$IF2" = 1 ]; then
  python3 -B "$TREE/sw/mailbox/gen_mailbox.py" --variant-interfaces 2 --out "$OUT/gen"
  INC=$OUT/gen
  PKG=$OUT/gen/KL_mbx_pkg.sv
  TOPSV=$OUT/gen/KL_mbx.sv
fi
FW_INC="-I$INC -I$FW/wire -I$FW/host -I$FW/port -I$FW/loop -I$FW/mbx"
cc -std=c11 -O2 -Wall -Wextra -Werror -pedantic $FW_INC -c "$FW/host/mbx_model.c" -o "$OUT/mbx_model.o"
cp "$HERE/diff_probe.cpp" "$MBX/diff_probe_r522.cpp"
cd "$MBX"
"$VERILATOR" --cc --exe --build -j 0 --top-module tb_mbx_top -Wall -Wno-fatal -Werror-USERERROR \
  -Wno-DECLFILENAME -Wno-UNUSEDPARAM -Wno-UNUSEDSIGNAL -GHOST_P=0 --Mdir "$OUT/obj" \
  -CFLAGS "-std=c++17 -O2 -I$INC -I$MBX -I$FW/host" -LDFLAGS "$OUT/mbx_model.o" \
  "$PKG" "$RTL_DIR/KL_mbx_ring.sv" "$RTL_DIR/KL_mbx_rx.sv" "$RTL_DIR/KL_mbx_tx.sv" "$RTL_DIR/KL_mbx_evt.sv" \
  "$TOPSV" "$RTL_DIR/KL_mbx_wb.sv" "$RTL_DIR/KL_mbx_axil.sv" tb_mbx_top.sv diff_probe_r522.cpp -o Vprobe \
  > "$OUT/build.log" 2>&1
rm -f "$MBX/diff_probe_r522.cpp"
"$OUT/obj/Vprobe" "${N:-20000}" "${SEED:-522}"
