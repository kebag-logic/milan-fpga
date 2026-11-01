#!/bin/bash
# Build one isolated PHC-load probe on the MII shape.
# usage: guard_build.sh <exact-head export> <dest> <guard|keep> <packet scripts dir>
# Needs VERILATOR and python3 on PATH; run guard_sweep.sh after all three builds.
set -e
HEADSRC=$1 "$4/mk_probe.sh" "$2"; python3 "$4/guard_probe.py" "$2" "$3"; cd "$2/tb/verilator/gptp_txts"
make -s gptp_ucode.hex MILAN_LITEX_PYTHON=python3
"$VERILATOR" --cc --exe --build -j 3 --top-module gptp_txts_wrap -Wno-fatal -Wno-lint \
  -GUCODE_HEX_P='"gptp_ucode.hex"' -GCLK_HZ_P=2000000 -CFLAGS "-std=c++17 -O2 -I$PWD -DGPTP_TXTS_MII" \
  --Mdir obj_mii -DGPTP_TXTS_MII -GETH_TICK_NS_P=40 -GETH_CYC_PER_OCTET_P=2 \
  $(make -s -n run-mii MILAN_LITEX_PYTHON=python3 | grep -oE '[^ ]+\.(sv|v)\b' | sort -u | tr '\n' ' ') sim_main.cpp -o Vgptp_txts_sim
