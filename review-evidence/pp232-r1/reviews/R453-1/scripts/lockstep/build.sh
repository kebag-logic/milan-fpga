#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# build.sh OUTDIR CANDIDATE.sv REFERENCE.sv PKG.sv N_CTRL N_SI N_SO IDENT
# Builds the reviewer lockstep bench (lk_top: reference beside candidate) into OUTDIR.
# VERILATOR (default: verilator on PATH) selects the simulator.
set -eu
out=$1; cand=$2; ref=$3; pkg=$4; nc=$5; nsi=$6; nso=$7; idn=$8
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$out"
cp "$cand" "$out/dut.sv"
cp "$ref" "$out/ref.sv"
cp "$pkg" "$out/pp_pkg.sv"
python3 "$here/gen_wrapper.py" "$out/dut.sv" "$out/lk_top.sv"
cd "$out"
${VERILATOR:-verilator} --cc --exe --build -j 2 --top-module lk_top \
  -GN_CTRL_P="$nc" -GN_STREAM_IN_P="$nsi" -GN_STREAM_OUT_P="$nso" -GEN_IDENTIFY_NOTIF_P="$idn" \
  -Wno-fatal -Wno-lint -Wno-style -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC \
  -CFLAGS "-std=c++17 -O2" -Mdir obj pp_pkg.sv ref.sv dut.sv lk_top.sv "$here/lk_main.cpp" -o Vlk_top \
  > build.log 2>&1
echo "built $out"
