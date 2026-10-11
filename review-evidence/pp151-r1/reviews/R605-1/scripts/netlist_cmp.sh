#!/usr/bin/env bash
# Elaborate one top at one shape from a lowered all.v, as syn/yosys/run.sh does
# (read_verilog -defer; hierarchy -check -top; proc; opt_clean), write the
# netlist (objects named from their connectivity by `autoname`) without
# attributes, and record the sha256 of its canonical form
# (canon_netlist.py: source positions masked, auto-names renumbered by first
# appearance, line order kept), its line count and Yosys `stat` totals.
# usage: netlist_cmp.sh <allv> <romdir> <outprefix> <top> [-set K V ...]
set -u
here=$(cd "$(dirname "$0")" && pwd)
allv=$1; romdir=$2; out=$3; top=$4; shift 4
work=$(mktemp -d "${out}.work.XXXX")
cp "$allv" "$work/all.v"; cp "$romdir"/ucode.hex "$romdir"/ltn_rom.hex "$work/"
sets=""; [ $# -gt 0 ] && sets="chparam $* $top;"
( cd "$work" && yosys -q -p "read_verilog -defer all.v; $sets hierarchy -check -top $top; proc; opt_clean; tee -q -o stat.txt stat; autoname; write_verilog -noattr net.v" ) > "$out.yosys.log" 2>&1
rc=$?
echo "$rc" > "$out.rc"
if [ $rc -eq 0 ]; then
  python3 -I "$here/canon_netlist.py" "$work/net.v" > "$out.canon.v"
  sha256sum < "$out.canon.v" | cut -d' ' -f1 > "$out.canon.sha256"
  wc -l < "$work/net.v" > "$out.lines"
  grep -E '^\s+(Number of cells|Number of wires|Number of wire bits)' "$work/stat.txt" | tail -3 > "$out.stat"
fi
rm -rf "$work"
exit $rc
