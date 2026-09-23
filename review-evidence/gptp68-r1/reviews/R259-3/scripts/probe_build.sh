#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Build the R259-3 probe harness: the head's engine sim_main.cpp with the
# phases of probe_phases.cpp.inc appended after the suite, in a scratch export.
set -eu
. "$(dirname "$0")/env.sh"
dir=$SCRATCH/probe-head
rm -rf "$dir"; mkdir -p "$dir"
git -C "$CLONE" archive "$HEAD_SHA" | tar -x -C "$dir"
python3 - "$dir/tb/verilator/engine/sim_main.cpp" "$(dirname "$0")/probe_phases.cpp.inc" <<'PY'
import sys
path, inc = sys.argv[1], open(sys.argv[2]).read()
s = open(path).read()
anchor_m = "  //! One warm reset, and the settling run behind it.\n"
anchor_c = "    keep_every_addend_inside_the_consumer_envelope();\n"
assert s.count(anchor_m) == 1 and s.count(anchor_c) == 1
s = s.replace(anchor_m, inc + "\n" + anchor_m)
s = s.replace(anchor_c, anchor_c + '    printf("-- R259-3 probes --\\n");\n'
              "    r_probe_lost_response_fall_rearms();\n"
              "    r_probe_cease_resume_rearms();\n"
              "    r_probe_rise_then_mastership_before_any_pair();\n"
              "    r_probe_lost_follow_up_keeps_the_lock();\n"
              "    r_probe_locked_boundary_after_a_gap();\n")
open(path, "w").write(s)
print("probe phases inserted")
PY
cd "$dir/tb/verilator/engine"
python3 ../../../hdl/ucode/gen_gptp_ucode.py --clk-hz 2000000 --cease-ms 3000 -o gptp_ucode.hex
"$PINNED_VERILATOR" --cc --exe --build -j 8 --top-module KL_gptp_engine -Wall -Wno-fatal \
  -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
  '-GUCODE_HEX_P="gptp_ucode.hex"' -GCLK_HZ_P=2000000 \
  -CFLAGS "-std=c++17 -O2 -I$dir/tb/verilator/engine -Wall -Wextra" \
  ../../../hdl/ucpu/gptp_ucpu_pkg.sv ../../../hdl/ucpu/KL_gptp_ucpu.sv \
  ../../../hdl/wire/KL_gptp_rx_parser.sv ../../../hdl/wire/KL_gptp_tx_slot.sv \
  ../../../hdl/common/KL_gptp_timer.sv ../../../hdl/top/KL_gptp_engine.sv \
  sim_main.cpp -o Vengine_probe > build.log 2>&1 || { tail -30 build.log; exit 1; }
grep -E 'warning|error' build.log | grep -v '^-' | head -5 || true
test -x obj_dir/Vengine_probe && echo "built obj_dir/Vengine_probe"
