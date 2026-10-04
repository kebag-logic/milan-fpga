#!/bin/sh
# Reviewer probe: tb/pp_top `run` (the integration suite that also builds the ADP
# engine) on a scratch copy of the exact head with probe q2 of r461_probes.py
# (the fresh branch notes the maximum index). Scratch only.
# usage: pptop_q2.sh PACKET_DIR
K=$1
S=$K/scratch
export PATH="$S/bin:$PATH"
export TMPDIR="$S/tmp"
W=$S/pptop-q2
rm -rf "$W"
cp -a "$S/head" "$W"
python3 - "$W/hdl/adp/KL_adp_engine.sv" <<'EOF'
import sys
p = sys.argv[1]
a = "            rec_wr_en_w = 1'b1;               // fresh cycle: store + re-arm\n"
b = "            rec_wr_en_w = 1'b1;\n            rec_wr_data_w = {rx_ifx_r, 32'hFFFF_FFFF};\n"
t = open(p).read()
assert t.count(a) == 1
open(p, "w").write(t.replace(a, b))
EOF
make -C "$W/tb/pp_top" run > "$K/receipts/pptop-q2-run.log" 2>&1
echo $? > "$K/receipts/pptop-q2-run.rc"
