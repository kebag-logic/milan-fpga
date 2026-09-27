#!/bin/sh
# Differential: the milan_dp 4x4 sim_nxn leg (dynamic-map T66/DMAP coverage)
# built and run on a disposable tree. Usage: r329_nxn_diff.sh <tree> <log>
set -u
cd "$1/tb/verilator/milan_dp" || exit 2
make -s ltn_rom.hex ucode.hex gptp_ucode.hex > /dev/null
cmd=$(make -n run 2>/dev/null | grep -- '--Mdir obj_nxn ')
[ -n "$cmd" ] || { echo "no nxn build line"; exit 2; }
echo "### tree HEAD $(git -C "$1" rev-parse HEAD)" > "$2"
sh -c "$cmd" > "$2.build" 2>&1 || { echo "BUILD FAILED"; tail -20 "$2.build"; exit 3; }
./obj_nxn/Vmilan_dp_nxn >> "$2" 2>&1; echo "### rc=$?" >> "$2"
