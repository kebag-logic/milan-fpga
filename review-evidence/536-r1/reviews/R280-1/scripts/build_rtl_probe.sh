#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Disposable RTL probe: a COPY of the pinned protocol-processor tb/pp_top,
# run up to and including its MVU phase (M1..M9) and then the review's extra
# MVU cases (r280_mvu_probe.inc), against the pinned hdl/ read in place.
# Nothing in the checkout is written.
#
# usage: build_rtl_probe.sh <milan-fpga checkout> <scratch dir> <verilator>
set -eu
repo=$(cd "$1" && pwd)
scratch=$2
vl=$3
here=$(cd "$(dirname "$0")" && pwd)
pp=$repo/protocol-processor
hdl=$pp/hdl

rm -rf "$scratch/ppprobe"
mkdir -p "$scratch/ppprobe/tb"
cp -R "$pp/tb/pp_top" "$scratch/ppprobe/tb/pp_top"
cp -R "$pp/tb/common" "$scratch/ppprobe/tb/common"
cp "$here/r280_mvu_probe.inc" "$scratch/ppprobe/tb/pp_top/"
cd "$scratch/ppprobe/tb/pp_top"

# splice: the probe struct ahead of Suite, and the probe right after the
# pinned MVU phase, returning before the later phases run
python3 -B - <<'EOF'
from pathlib import Path
p = Path("sim_main.cpp")
s = p.read_text(encoding="utf-8")
anchor_struct = "\nstruct Suite {\n"
anchor_phase = "    MilanInfoPhase{h, d, image_entity}.run();\n"
assert s.count(anchor_struct) == 1 and s.count(anchor_phase) == 1
s = s.replace(anchor_struct, '\n#include "r280_mvu_probe.inc"\n' + anchor_struct)
s = s.replace(anchor_phase, anchor_phase
              + "    R280MvuProbe{h}.run();\n    return;\n")
p.write_text(s, encoding="utf-8")
EOF

PYTHONDONTWRITEBYTECODE=1 python3 -B "$hdl/acmp/rom/gen_ltn_rom.py" -o ltn_rom.hex
PYTHONDONTWRITEBYTECODE=1 python3 -B "$hdl/aecp/ucode/gen_ucode.py" -o ucode.hex

srcs=$(sed -n '/^SRCS *=/,/pp_top_wrap.sv/p' Makefile \
       | sed -e 's/^SRCS *=//' -e 's/\\$//' -e "s#\$(HDL)#$hdl#g")
# shellcheck disable=SC2086
"$vl" --cc --exe --build -j 8 --top-module pp_top_wrap \
  -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
  -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
  -CFLAGS "-std=c++17 -O2 -I$(pwd) -Wall -Wextra" \
  $srcs sim_main.cpp -o Vpp_top_sim >build.log 2>&1 \
  || { tail -40 build.log; exit 2; }
./obj_dir/Vpp_top_sim
