#!/usr/bin/env bash
# Plant one gen_ucode.py patch in a scratch copy (hdl, tb/common, tb/pp_top)
# and run tb/pp_top's aecp-dispatch target. Usage:
#   own_arm.sh <head-tree> <patch|none> <work-dir>
set -u
src=$1 patch=$2 w=$3; V=${VERILATOR:-verilator}  # set VERILATOR to the pinned 5.050 binary
rm -rf "$w"; mkdir -p "$w/tree/tb"
cp -a "$src/hdl" "$w/tree/"; cp -a "$src/tb/common" "$src/tb/pp_top" "$w/tree/tb/"
rm -rf "$w/tree/tb/pp_top"/obj_* "$w/tree/tb/pp_top"/*.hex
if [ "$patch" != none ]; then ( cd "$w/tree" && git apply "$patch" ) || { echo 99 > "$w/rc"; exit 99; }; fi
make -C "$w/tree/tb/pp_top" aecp-dispatch VERILATOR="$V" > "$w/log" 2>&1; echo $? > "$w/rc"
