#!/usr/bin/env bash
# [R558] R558-7 F1 demonstration: a scratch copy of the MAAP unit harness with ONE
# added check in [4b] (the PROBE starts below this station's block, so the PROBE's
# requested_start differs from the overlap start). Built against the clean RTL and
# against probe q1 (echo the overlap start). No checkout file is edited.
# usage: echo_gap_demo.sh <clone> <workdir>
set -u
C=$1; W=$2
rm -rf "$W"; mkdir -p "$W/tb/verilator/maap"
ln -s "$C/tb/common" "$W/tb/common"
python3 -I - "$C/tb/verilator/maap/sim_main.cpp" "$W/tb/verilator/maap/sim_main.cpp" <<'PY'
import sys
s = open(sys.argv[1]).read()
a = '    check_defend(f, "below", kPeerBelow, off0, 4);\n'
assert s.count(a) == 1
s = s.replace(a, a + '    ck("R558 probe: requested start echoes a PROBE starting below", f.at(26,6),\n'
                     '       static_cast<long>(0x91E0F0000000ULL | (off0-4)));\n')
open(sys.argv[2], "w").write(s)
PY
python3 -I - "$C/hdl/ieee1722/maap/KL_maap.sv" "$W/q1.sv" <<'PY'
import sys
s = open(sys.argv[1]).read(); a = "tx_defend_off_r <= rx_start_r;"
assert s.count(a) == 1
open(sys.argv[2], "w").write(s.replace(a, "tx_defend_off_r <= conf_start_w;"))
PY
VF="--cc --exe --build -j 2 --top-module KL_maap -GCLK_FREQ_HZ_P=10000 --public-flat-rw -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-IMPORTSTAR -Wno-CASEINCOMPLETE -Wno-EOFNEWLINE"
for v in clean q1; do
  rtl=$C/hdl/ieee1722/maap/KL_maap.sv; [ $v = q1 ] && rtl=$W/q1.sv
  ( cd "$W/tb/verilator/maap" && $VERILATOR $VF -CFLAGS "-std=c++17 -O2" -Mdir obj_$v "$rtl" sim_main.cpp -o sim > build_$v.log 2>&1 ) || { echo "$v build failed"; continue; }
  ( cd "$W/tb/verilator/maap/obj_$v" && ./sim > ../run_$v.log 2>&1; echo "$v rc=$?" )
  grep -E 'R558 probe|M2 B.3.6.6|checks, ' "$W/tb/verilator/maap/run_$v.log"
done
