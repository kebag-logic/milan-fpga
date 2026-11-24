#!/bin/sh
# Reviewer probe: the two-interface gPTP closed loop on an unplanted firmware copy and on a copy whose
# mailbox driver writes every interface's GPTP_STATE into interface 0's block.
# usage: probe_gptp_sim.sh <checkout> <scratch-dir> <verilator> <plain|planted>
set -u
R=$1; S=$2; V=$3; K=$4; FW=$S/sim-fw-$K
rm -rf "$FW" "$S/sim-obj-$K"; cp -r "$R/sw/firmware/ctrl" "$FW"
if [ "$K" = planted ]; then
  python3 -I - "$FW/mbx/mbx.c" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
old = "mbx_bus_write32(pub_reg(interface, MBX_PUB_REG_GPTP_STATE), words[state]);"
assert s.count(old) == 1
open(p, "w").write(s.replace(old, "mbx_bus_write32(pub_reg(0u, MBX_PUB_REG_GPTP_STATE), words[state]);"))
PY
fi
make -C "$R/tb/verilator/gptp_sw" run VERILATOR="$V" FW="$FW" MDIR="$S/sim-obj-$K" -j4
