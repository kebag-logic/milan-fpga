#!/usr/bin/env bash
# Base/head netlist identity for passing shapes.
# Usage: netlists.sh <tree> <outdir> <jobs>   (sv2v, yosys on PATH)
# Lowers the tree's hdl/ once (as syn/yosys/run.sh does), generates the ROMs,
# then per case: read_verilog -defer; chparam; hierarchy -check -top; proc;
# opt_clean; stat; write_verilog -noattr. Canonical form: all.v line numbers
# and Yosys auto-index numbers masked, lines sorted; sha256 per case.
set -euo pipefail
T=$(cd "$1" && pwd); O=$2; J=$3; mkdir -p "$O"; O=$(cd "$O" && pwd)
cd "$T"
sv2v $(find hdl -name '*_pkg.sv' | sort) $(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort) > "$O/all.v"
( cd hdl/aecp/ucode && python3 gen_ucode.py -o "$O/ucode.hex" >/dev/null )
( cd hdl/acmp/rom && python3 gen_ltn_rom.py -o "$O/ltn_rom.hex" >/dev/null )
sha256sum "$O/ucode.hex" "$O/ltn_rom.hex" | sed "s#$O/##" > "$O/roms.sha256"
tops=$(sed -n '/^tops=(/,/)/p' syn/yosys/run.sh | tr -d '()' | sed 's/tops=//' | tr -s ' \n' '\n' | grep -v '^$')
{
  for t in $tops; do echo "$t|$t|"; done
  for s in 1x1 2x2 4x4 8x8 16x16 1x8 8x1; do i=${s%x*}; o=${s#*x}
    echo "protocol_processor_top@$s|protocol_processor_top|-set N_STREAM_IN_P $i -set N_STREAM_OUT_P $o"; done
  echo "protocol_processor_top@if2|protocol_processor_top|-set N_AVB_IF_P 2"
} > "$O/cases.txt"
one() {
  IFS='|' read -r name top sets <<<"$1"; cd "$O"
  local cp=""; [ -n "$sets" ] && cp="chparam $sets $top; "
  if yosys -q -p "read_verilog -defer all.v; ${cp}hierarchy -check -top $top; proc; opt_clean; tee -q -o $name.stat stat; write_verilog -noattr $name.raw.v" > "$name.log" 2>&1; then
    sed -E 's/all\.v:[0-9]+(\.[0-9]+-[0-9]+\.[0-9]+)?/all.v:L/g; s/\$[0-9]+/$N/g' "$name.raw.v" | sort > "$name.canon"
    grep -vE '^\s*$|Yosys|Printing statistics|Executing' "$name.stat" | sort > "$name.statc"
    echo "$name $(sha256sum < "$name.canon" | cut -c1-64) $(sha256sum < "$name.statc" | cut -c1-64) $(wc -l < "$name.canon")"
    rm -f "$name.raw.v"
  else echo "$name ELAB-FAIL $(grep -m1 ERROR "$name.log")"; fi
}
export -f one; export O
xargs -a "$O/cases.txt" -d '\n' -P "$J" -I{} bash -c 'one "$@"' _ {} | sort > "$O/summary.txt"
wc -l < "$O/summary.txt"
