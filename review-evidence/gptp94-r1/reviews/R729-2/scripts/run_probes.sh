#!/bin/bash
# usage: JOBS=n run_probes.sh <harness-tree> <rtl-tree> <outdir>
# Builds <harness-tree>'s engine sim_main.cpp with probes.inc inserted after
# phase 51, against <rtl-tree>'s RTL and microcode generator, and runs the
# shipping image once. Nothing is written into either tree.
set -u
H=$(realpath "$1"); T=$(realpath "$2"); O=$(realpath -m "$3")
HERE=$(dirname "$(realpath "$0")")
rm -rf "$O"; mkdir -p "$O"
# the harness includes ../../common/*, so keep its tb/ layout
cp -r "$H/tb" "$O/tb"; rm -rf "$O/tb/verilator/engine/obj_dir"
SRC="$O/tb/verilator/engine"
python3 -I - "$H/tb/verilator/engine/sim_main.cpp" "$HERE/probes.inc" "$SRC/sim_main.cpp" <<'PY'
import sys
s = open(sys.argv[1]).read(); inc = open(sys.argv[2]).read()
def once(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new)
once("    run_the_port_enable_phases();\n    hold_every",
     "    run_the_port_enable_phases();\n    run_reviewer_probes();\n    hold_every")
once("  std::vector<uint64_t> txstarts;\n",
     "  std::vector<uint64_t> txstarts;\n  std::vector<uint64_t> pr_starts;\n")
once("        txstarts.push_back(cyc);\n",
     "        txstarts.push_back(cyc);\n        pr_starts.push_back(cyc);\n")
once("  // ---- 41: #89, sync receipt ageing", inc + "\n  // ---- 41: #89, sync receipt ageing")
open(sys.argv[3], "w").write(s)
PY
R=$T/hdl
cd "$O"
python3 "$R/ucode/gen_gptp_ucode.py" --clk-hz 2000000 --cease-ms 3000 -o gptp_ucode.hex > gen.log || exit 3
verilator --cc --exe --build -j "${JOBS:-2}" --top-module KL_gptp_engine -Wall -Wno-fatal \
  -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
  -GUCODE_HEX_P='"gptp_ucode.hex"' -GCLK_HZ_P=2000000 \
  -CFLAGS "-std=c++17 -O2 -I$SRC -Wall -Wextra" \
  $R/ucpu/gptp_ucpu_pkg.sv $R/ucpu/KL_gptp_ucpu.sv $R/wire/KL_gptp_rx_parser.sv \
  $R/wire/KL_gptp_tx_slot.sv $R/common/KL_gptp_timer.sv $R/top/KL_gptp_engine.sv \
  "$SRC/sim_main.cpp" -o Vprobe > build.log 2>&1 || { echo build failed; exit 4; }
./obj_dir/Vprobe > run.log 2>&1; rc=$?
echo "rc=$rc"; grep -E "PROBE|checks:" run.log; exit $rc
