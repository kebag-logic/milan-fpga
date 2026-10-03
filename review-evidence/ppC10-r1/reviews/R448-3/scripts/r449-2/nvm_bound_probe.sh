#!/usr/bin/env bash
# Item 2 probes on KL_pp_nvm_port's MAX_PAYLOAD_P guard, in scratch copies.
# Usage: nvm_bound_probe.sh <head-tree> <work-dir>
# Variants: pristine; err ($fatal -> $error); warn ($fatal -> $warning);
# derived (the bound computed from dev_len_o's width and HDR_LEN_C);
# hdr10 (HDR_LEN_C widened to 10 with the guard as shipped - a drift demo).
# For each: tb/nvm_port/elab_bounds.sh (pinned Verilator) and
# sv2v + yosys `chparam` at 65527 and 65528.
set -u
src=$1 w=$2; V=${VERILATOR:-verilator}  # set VERILATOR to the pinned 5.050 binary
F=hdl/packet_engine/KL_pp_nvm_port.sv
rm -rf "$w"; mkdir -p "$w"
for v in pristine err warn derived hdr10; do
  t="$w/$v"; mkdir -p "$t"; cp -a "$src/hdl" "$src/tb" "$t/"
  case $v in
    err)  sed -i 's/\$fatal(1, "KL_pp_nvm_port: MAX_PAYLOAD_P/$error("KL_pp_nvm_port: MAX_PAYLOAD_P/' "$t/$F" ;;
    warn) sed -i 's/\$fatal(1, "KL_pp_nvm_port: MAX_PAYLOAD_P/$warning("KL_pp_nvm_port: MAX_PAYLOAD_P/' "$t/$F" ;;
    derived)
      python3 - "$t/$F" <<'PY'
import sys
f = sys.argv[1]; s = open(f).read()
old_if = "  if (MAX_PAYLOAD_P > 65527) begin : g_maxp_check\n"
old_msg = '    $fatal(1, "KL_pp_nvm_port: MAX_PAYLOAD_P=%0d is above 65527: 8 + it overflows dev_len_o",\n           MAX_PAYLOAD_P);\n'
assert old_if in s and old_msg in s
s = s.replace(old_if, "  localparam int unsigned MAXP_BOUND_C = (1 << $bits(dev_len_o)) - 1 - int'(HDR_LEN_C);\n"
                      "  if (MAX_PAYLOAD_P > MAXP_BOUND_C) begin : g_maxp_check\n")
s = s.replace(old_msg, '    $fatal(1, "KL_pp_nvm_port: MAX_PAYLOAD_P=%0d is above %0d: 8 + it overflows dev_len_o",\n'
                       '           MAX_PAYLOAD_P, MAXP_BOUND_C);\n')
open(f, 'w').write(s)
PY
      ;;
    hdr10) sed -i "s/localparam logic \[15:0\] HDR_LEN_C  = 16'd8;/localparam logic [15:0] HDR_LEN_C  = 16'd10;/" "$t/$F" ;;
  esac
  diff -u "$src/$F" "$t/$F" > "$w/$v.diff"
  ( cd "$t/tb/nvm_port" && VERILATOR=$V ./elab_bounds.sh ) > "$w/$v.elab.log" 2>&1; echo $? > "$w/$v.elab.rc"
  sv2v "$t/$F" > "$t/port.v" 2> "$w/$v.sv2v.err"; echo $? > "$w/$v.sv2v.rc"
  for p in 65527 65528; do
    yosys -q -p "read_verilog -defer $t/port.v; chparam -set MAX_PAYLOAD_P $p KL_pp_nvm_port; hierarchy -check -top KL_pp_nvm_port; proc; opt_clean" > "$w/$v.yosys.$p.log" 2>&1
    echo $? > "$w/$v.yosys.$p.rc"
  done
  echo "$v elab_bounds rc=$(cat $w/$v.elab.rc) sv2v rc=$(cat $w/$v.sv2v.rc) yosys@65527 rc=$(cat $w/$v.yosys.65527.rc) yosys@65528 rc=$(cat $w/$v.yosys.65528.rc)"
done
