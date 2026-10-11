#!/usr/bin/env bash
# M8a-1: OOC mapping of the split placement's firmware memory, four points (scratch).
set -u
S=$VALIDATION_STORAGE/640m8a-a594/m81
export PATH=$WORKSPACE_HOME/Xilinx/2026.1/Vivado/bin:$PATH TMPDIR=$S/tmpdir
cd "$S/map" || exit 9
date -Is > "$S/map-acquired.txt"
vivado -mode batch -nojournal -log "$S/map.vivado.log" -source ctrl_memory_ooc.tcl > "$S/map.stdout" 2>&1
echo $? > "$S/map.rc"
date -Is > "$S/map-released.txt"
