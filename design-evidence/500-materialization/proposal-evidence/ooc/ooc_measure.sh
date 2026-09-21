#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Out-of-context area of ONE top, by the recipe of
# docs/design/SAVED_STATE_FASTCONNECT.md section 8.3: sv2v, then
# `synth_xilinx -family xc7 [-nodsp] -top <top> -flatten`, then `stat`, parsed
# with the SAME accounting as syn/yosys/ooc.sh (LUT1..LUT6, distributed RAM
# converted to its LUT6 occupancy, FD*, RAMB36E1, RAMB18E1, DSP48E1, CARRY4).
# Re-implemented standalone because the tracked script accepts only its own
# list of tops, exactly as the snapshot-ownership lane did (its section 18).
#
#   ooc_measure.sh <label> <top> "<NAME=VALUE ...>" <nodsp 0|1> <src.sv>...
#
# Prints one row: label top LUT LUTRAM LUT_TOT FF RAMB36 RAMB18 DSP CARRY4.
# Exit status is non-zero when sv2v or yosys fails or no stat block is found.
set -euo pipefail
label="$1"; top="$2"; params="$3"; nodsp_flag="$4"; shift 4
out="${OOC_OUT:-/tmp/a150-ooc}"
mkdir -p "$out"
v="$out/$label.v"; log="$out/$label.yosys.log"; json="$out/$label.json"
sv2v --top="$top" "$@" > "$v" 2> "$out/$label.sv2v.err"
chp=""
for kv in $params; do chp="$chp chparam -set ${kv%%=*} ${kv#*=} $top;"; done
nodsp=""; [ "$nodsp_flag" = "1" ] && nodsp=" -nodsp"
yosys -q -l "$log" -p "read_verilog $v;$chp synth_xilinx -family xc7$nodsp -top $top -flatten; stat; write_json $json" > /dev/null
awk -v top="$top" -v label="$label" '
  function lram_luts(t) {
    if (t == "RAM256X1D" || t == "RAM512X1S" || t == "RAM32X8S" ||
        t == "RAM64X8SW" || t == "RAM32X16DR8") return 8;
    if (t == "RAM32M" || t == "RAM64M" || t == "RAM128X1D" ||
        t == "RAM32M16" || t == "RAM64M8" || t == "RAM256X1S" ||
        t == "RAM32X4S") return 4;
    if (t == "RAM32X1D" || t == "RAM32X1D_1" || t == "RAM64X1D" ||
        t == "RAM64X1D_1" || t == "RAM128X1S" || t == "RAM128X1S_1" ||
        t == "RAM32X2S" || t == "RAM64X2S") return 2;
    if (t == "RAM32X1S" || t == "RAM32X1S_1" ||
        t == "RAM64X1S" || t == "RAM64X1S_1") return 1;
    return 0;
  }
  /^=== .* ===$/ { inblk = 0 }
  $0 == "=== " top " ===" { blocks++; inblk=1; lut=0; lrm=0; ff=0; r36=0; r18=0; dsp=0; c4=0 }
  inblk && $2 ~ /^LUT[1-6]$/     { lut += $1 }
  inblk && $2 ~ /^RAM[0-9]/      { c = lram_luts($2); if (c == 0) unpriced = $2; lrm += $1 * c }
  inblk && $2 ~ /^FD[CPRS]E?$/   { ff  += $1 }
  inblk && $2 ~ /^RAMB36E1$/     { r36 += $1 }
  inblk && $2 ~ /^RAMB18E1$/     { r18 += $1 }
  inblk && $2 ~ /^DSP48E1$/      { dsp += $1 }
  inblk && $2 ~ /^CARRY4$/       { c4  += $1 }
  END {
    if (blocks == 0) { printf "no stat block for %s\n", top; exit 3 }
    if (unpriced != "") { printf "unpriced distributed RAM cell %s\n", unpriced; exit 5 }
    if (lut + lrm + ff + r36 + r18 + dsp + c4 == 0) { printf "zero cells for %s\n", top; exit 4 }
    printf "%-34s %-26s %6d %6d %7d %6d %6d %6d %4d %6d\n", label, top, lut, lrm, lut + lrm, ff, r36, r18, dsp, c4
  }' "$log"
